import flet as ft
import pandas as pd
import time
import logging
import os
from datetime import datetime, timedelta

DEFAULT_DATE_FILTER = '01 JAN 2024' # TEST DATE REMOVE FOR PROD
# DEFAULT_DATE_FILTER = datetime.today().strftime("%A %B %d %Y")
ISO_DATE_FILTER = pd.to_datetime(DEFAULT_DATE_FILTER)
UPDATE_TIME = 3600 # One Hour = 3600 secconds.
LOG_DATE = datetime.now().strftime("%Y-%m-%d")

os.makedirs('./logs', exist_ok=True)

logging.basicConfig(
    filename=f'logs/service_log_{LOG_DATE}.txt',
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%m-%d-%Y %I:%M:%S %p'
)

def log_function(func_name, duration_ms):
    log_message = f'{func_name}: Completed in {duration_ms}ms'
    logging.info(log_message)

def log_generic(generic_msg:str):
    log_msg = f'[GENERIC] {generic_msg}'
    logging.info(log_msg)

def main(page: ft.page):
    # Format Window
    page.title = 'CSV Filter Service for PowerApps'
    page.bgcolor = ft.colors.CYAN_100
    page.padding = ft.padding.all(5)
    page.window.height = 550
    page.window.min_height = 550
    page.window.width = 1100
    page.window.min_width = 1100
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.ControlState.HOVERED: ft.colors.AMBER,
                ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
            },
            track_visibility=False,
            track_border_color=ft.colors.AMBER,
            thumb_visibility=False,
            thumb_color={
                ft.ControlState.HOVERED: ft.colors.BLUE_700,
                ft.ControlState.DEFAULT: ft.colors.GREY_700,
            },
            thickness=8,
            radius=8,
            main_axis_margin=8,
            cross_axis_margin=8,
        )
    )

    # Init Variables
    service_running=False
    service_sleeping=False
    
    # Log Flet Control
    log_text = ft.Text(value='', color=ft.colors.AMBER_400)

    # Lottie Flet Control, local files broken in flet, must use lottie.host
    lottie_sleep = ft.Lottie(
        src='https://lottie.host/cb5a5101-3607-465f-ab76-a98a33aaaed4/ba1gXPDyl2.json',
        background_loading=True,
        fit=ft.ImageFit.CONTAIN,
        height=100,
    )
    lottie_run = ft.Lottie(
        src='https://lottie.host/3acebf42-a085-441e-97b8-b4a37c178ede/XhmfvlNwQQ.json',
        background_loading=True,
        fit=ft.ImageFit.CONTAIN,
        height=100,
    )
    lottie_stopped = ft.Lottie(
        src='https://lottie.host/be52cd2e-c0c7-47c0-adaa-43e15f5a4696/KzdSRVd2Vi.json',
        background_loading=True,
        fit=ft.ImageFit.CONTAIN,
        height=100,
    )
    
    lottie = ft.Lottie(
        src='https://lottie.host/be52cd2e-c0c7-47c0-adaa-43e15f5a4696/KzdSRVd2Vi.json',
        background_loading=True,
        fit=ft.ImageFit.CONTAIN,
        height=75,
    )
    
    def lottie_update():
        nonlocal lottie
        if service_running:
            if service_sleeping:
                lottie.src = lottie_sleep.src
            else:
                lottie.src = lottie_run.src
        else:
            lottie.src = lottie_stopped.src
        lottie.update()

    # Select Input File
    selected_files = ft.Text()
    selected_file_paths = []
    def pick_file_result(e: ft.FilePickerResultEvent):
        nonlocal selected_files
        nonlocal selected_file_paths
        if e.files == None:    
            selected_files = None
            selected_file_paths = None

        selected_files.value = (
            ', '.join(map(lambda f: f.name, e.files)) if e.files else 'Cancelled!'
        )
        
        if e.files is not None:
            for i in e.files:
                selected_file_paths.append(i.path)
        
        selected_files.update()
    
    pick_file_dialog = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(pick_file_dialog)

    # Select Output Folder
    selected_folder = ft.Text()
    selected_folder_path = None
    def pick_folder_result(e: ft.FilePickerResultEvent):
        nonlocal selected_folder
        nonlocal selected_folder_path
        split_path = e.path.split('\\')
        small_path = split_path[-1]
        selected_folder.value = (
            small_path if e.path else 'Cancelled!'
        )
        if e.path is not None:
            selected_folder_path = e.path
        selected_folder.update()
    pick_folder_dialog = ft.FilePicker(on_result=pick_folder_result)
    page.overlay.append(pick_folder_dialog)

    # Process the csv files
    def process_file(e=None):
        nonlocal service_sleeping
        service_sleeping = False
        lottie_update()
        csv_file = None
        
        execute_time_start = time.time()
        
        # Pull all data from each selected csv
        dataframes = []
        for i in selected_file_paths:
            temp_read = pd.read_csv(i,
                dtype={
                    'ID': str,
                    ' DateTime': str,
                    ' Shift': str,
                    ' Downtime': float,
                    ' Downtime Reason': str,
                    ' Comments': str
                }
            )
            
            # Check row validity through ID column
            temp_read['ID_is_numeric'] = pd.to_numeric(temp_read['ID'], errors='coerce').notnull() # Add bool column to check validity
            temp_read = temp_read[temp_read['ID_is_numeric']] # Return a dataframe where validity column is true
            temp_read = temp_read.drop('ID_is_numeric', axis=1) # Remove the extra column

            # Check row validity though datetime column
            temp_read['Datetime_is_datetime'] = pd.to_datetime(temp_read[' DateTime'], errors='coerce').notnull()
            temp_read = temp_read[temp_read['Datetime_is_datetime']]
            temp_read = temp_read.drop('Datetime_is_datetime', axis=1)
            
            # Capture pleater line from csv file name
            split_path = i.split('\\')
            small_path = split_path[-1]
            split_file = small_path.split('_')
            pleater = split_file[0]
            
            # Add Pleater line to output
            temp_read['Pleater'] = pleater
            dataframes.append(temp_read)
        
        # Create single file from all dataframes
        csv_file = pd.concat(dataframes, ignore_index=True)
   
        # Try: applying the datetime type to the ' Datetime' column
        try:
            csv_file[' DateTime'] = pd.to_datetime(csv_file[' DateTime'])
        except:
            log_generic('INVALID DATE FOUND') # Convert DateTime column to iso datetime format
        
        # Try: Filtering dates by the date filter
        try:
            datefilter = ISO_DATE_FILTER # Specify a datetime to start the filter
            filtered_file = csv_file[csv_file[' DateTime'] >= datefilter] # Filter the input csv by dates later than the datefiter
        except:
            log_generic('INVALID DATE FORMAT FOUND IN DATETIME COLUMN. PROCESS ABORTED')

        try:
            filtered_file.to_csv(selected_folder_path + '\\output.csv', index=False) # Return the filtered file content
        except:
            log_generic('File could not be written! Is the output file opened?')
        
        execute_time_end = time.time()
        execute_time = int((execute_time_end - execute_time_start)*1000)
        log_function('CSV File Processing', execute_time)
        service_sleeping=True
        lottie_update()
        update_logs()
        
    def update_logs():
        nonlocal log_text
        log_text.value = open(f'logs/service_log_{LOG_DATE}.txt', 'r').read()
        log_text.update()
    
    def close_service(e):
        nonlocal service_running
        nonlocal service_sleeping
        service_running = False
        service_sleeping = False
        log_function('Service Closed', 0)
        lottie_update()
        button_controls.update()
        update_logs()

    def find_sleep_time():
        start_time = datetime.now()
        end_time = (start_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        sleep_time = (end_time-start_time).total_seconds()
        log_generic(f'Next runtime in: {round(sleep_time/60, 0)} minutes')
        update_logs()
        return sleep_time if start_time.minute != 0 else 3600
    
    def main_service(e=None):
        nonlocal service_running
        
        if selected_file_paths == None:
            log_generic('No file selected, service not started')
            update_logs()
            service_running = False
        else:
            service_running = True
        
        while service_running:
            process_file()
            sleep_time = find_sleep_time()
            time.sleep(sleep_time)
        
        button_controls.update()

    # Button Controls
    button_controls = ft.Container(
        content=ft.Column(
            controls=[
                lottie,
                #ft.TextField(
                #    value=DEFAULT_DATE_FILTER,label='Date Filter',
                #    read_only=True,
                #    text_size=12,
                #    dense=True,
                #),
                ft.ElevatedButton(
                    text='Input files',
                    icon=ft.icons.FILE_OPEN,
                    icon_color=ft.colors.BLUE_400,
                    on_click=lambda _: pick_file_dialog.pick_files(allow_multiple=True, allowed_extensions=['csv'])
                ),
                # selected_files,
                ft.ElevatedButton(
                    text='Output Location',
                    icon=ft.icons.FOLDER,
                    icon_color=ft.colors.AMBER_300,
                    on_click=lambda _: pick_folder_dialog.get_directory_path(),
                ),
                # selected_folder,
                ft.ElevatedButton(
                    text='Start Service',
                    icon=ft.icons.PLAY_ARROW,
                    icon_color=ft.colors.GREEN_400,
                    on_click=main_service
                ),
                ft.ElevatedButton(
                    text='Stop Service',
                    icon=ft.icons.STOP,
                    icon_color=ft.colors.RED_400,
                    on_click=close_service
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        expand=1,
        padding=ft.padding.all(10)
    )

    # Log file Control
    log_controls = ft.Container(
        content=ft.Column(
            controls=[
                log_text
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            auto_scroll=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.MainAxisAlignment.CENTER
        ),
        alignment=ft.alignment.top_left,
        bgcolor=ft.colors.BLACK,
        expand=4,
        border_radius=5,
        padding=ft.padding.all(10)
    )
    
    # Main Row
    main_row = ft.Container(
        content=ft.Row(
            controls=[
                button_controls,
                log_controls
            ],
            expand=True
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        bgcolor= ft.colors.WHITE,
        border_radius= 5,
        padding= ft.padding.all(5),
    )
    
    # Main Container
    main_window = ft.Container(
        content=ft.Column(
            controls=[
                main_row,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        padding= ft.padding.all(1)
    )
    
    page.add(main_window)

if __name__ == '__main__':
    ft.app(main, assets_dir='assets')
