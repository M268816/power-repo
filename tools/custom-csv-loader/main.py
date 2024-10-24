import flet as ft
import pandas as pd
import time
import logging
import os
from datetime import datetime, timedelta

UPDATE_TIME = 3600 # One Hour = 3600 seconds.
LOG_DATE = datetime.now().strftime("%Y-%m-%d")

# Custom Logging
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

def log_custom(msg:str, info:str='GENERIC'):
    log_msg = f'[{info}] {msg}'
    logging.info(log_msg)

# Flet
def main(page: ft.page):
    page.title = 'CSV Filter Service for PowerApps'
    page.bgcolor = ft.colors.CYAN_100
    page.padding = ft.padding.all(5)
    page.window.height = 425
    page.window.min_height = 425
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
    selected_files = ft.Text()
    selected_file_paths = []
    selected_folder = ft.Text()
    selected_folder_path = None
    date_filter = None

    # Init date for data filter
    def update_date_filter():
        nonlocal date_filter
        date_filter = pd.to_datetime(datetime.today().strftime('%A %B %d %Y'))
    update_date_filter()

    def update_logs():
        nonlocal log_text
        log_text.value = open(f'logs/service_log_{LOG_DATE}.txt', 'r').read()
        log_text.update()
    
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
    def pick_file_result(e: ft.FilePickerResultEvent):
        nonlocal selected_files
        nonlocal selected_file_paths
        if e.files == None:
            selected_file_paths = []
        else:
            for i in e.files:
                selected_file_paths.append(i.path)

        selected_files.value = (
            ', '.join(map(lambda f: f.name, e.files)) if e.files else 'Cancelled!'
        )
    # Create file picker dialog
    pick_file_dialog = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(pick_file_dialog)

    # Select Output Folder
    def pick_folder_result(e: ft.FilePickerResultEvent):
        nonlocal selected_folder
        nonlocal selected_folder_path
        if e.path == None:
            selected_folder_path = None
        else:
            split_path = e.path.split('\\')
            small_path = split_path[-1]
            selected_folder_path = e.path
        
        selected_folder.value = (
            small_path if e.path else 'Cancelled!'
        )
    # Create folder picker dialog
    pick_folder_dialog = ft.FilePicker(on_result=pick_folder_result)
    page.overlay.append(pick_folder_dialog)

    def close_service(e):
        nonlocal service_running
        nonlocal service_sleeping
        service_running = False
        service_sleeping = False
        log_custom('Service Closed', 'Processing Service')
        lottie_update()
        button_controls.update()
        update_logs()
    
    def find_sleep_time():
        nonlocal date_filter
        start_time = datetime.now()
        end_time = (start_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        sleep_time = (end_time-start_time).total_seconds()
        log_custom(f'Next runtime in: {round(sleep_time/60, 0)} minutes')
        update_logs()
        return sleep_time if start_time.minute != 0 else 3600
     
    def sum_short_stops(file):
        short_stops = file.copy()
        short_stops[' Downtime Minutes'] = pd.to_numeric(short_stops[' Downtime Minutes'], errors='coerce')
        
        short_stops[' DateTime'] = short_stops[' DateTime'].dt.date
        short_stops = short_stops[short_stops[' Downtime Reason'] == 'Short Stop']
        
        short_stops = short_stops.groupby([' DateTime', 'Pleater', ' Shift'])[' Downtime Minutes'].sum()
        short_stops = short_stops.reset_index()
        short_stops['ID'] = 0
        short_stops[' Downtime Reason'] = 'Short Stop'
        short_stops[' Comments'] = 'MERGED RECORDS'
        
        short_stops = short_stops[['ID', ' DateTime', ' Shift', ' Downtime Minutes', ' Downtime Reason', ' Comments', 'Pleater']]

        # Reformat csv file
        file = file[file[' Downtime Reason'] != 'Short Stop']
        file = pd.concat([file, short_stops], ignore_index=True)
        file[' DateTime'] = pd.to_datetime(file[' DateTime'])
        
        return file
    
    def filter_by_date(file):
        # Try: Filter by date
        try:
            filtered_file = file[file[' DateTime'] >= date_filter]
            filtered_file = sum_short_stops(filtered_file) # Combine 'Short Stop' records
        except:
            log_custom('INVALID DATE FORMAT FOUND IN DATETIME COLUMN. PROCESS ABORTED', 'ERROR')
        
        return filtered_file
    
    def validity_check():
        data_frames = []
        for i in selected_file_paths:
            temp_read = pd.read_csv(i,
                dtype={
                    'ID': str,
                    ' DateTime': str,
                    ' Shift': str,
                    ' Downtime Minutes': str,
                    ' Downtime Reason': str,
                    ' Comments': str
                }
            )
            
            # Check row validity through ID column
            temp_read['ID_is_numeric'] = pd.to_numeric(temp_read['ID'], errors='coerce').notnull()  # Add bool column to check validity
            temp_read = temp_read[temp_read['ID_is_numeric']]                                       # Return a data frame where validity column is true
            temp_read = temp_read.drop('ID_is_numeric', axis=1)                                     # Remove the extra column

            # Check row validity though datetime column
            temp_read['DateTime_is_datetime'] = pd.to_datetime(temp_read[' DateTime'], format='%a %b %d %Y %H:%M:%S', errors='coerce').notnull()
            temp_read = temp_read[temp_read['DateTime_is_datetime']]
            temp_read = temp_read.drop('DateTime_is_datetime', axis=1)

            # Check row validity through downtime minutes column
            temp_read['Downtime_is_numeric'] = pd.to_numeric(temp_read[' Downtime Minutes'], errors='coerce').notnull()
            temp_read = temp_read[temp_read['Downtime_is_numeric']]
            temp_read = temp_read.drop('Downtime_is_numeric', axis=1)
            
            # Capture pleater line from csv file name
            split_path = i.split('\\')          # Create path array delimited by '\\'
            small_path = split_path[-1]         # Return last str to capture file name
            split_file = small_path.split('_')  # Create file name array delimited by '_'
            pleater = split_file[0]             # Return first str to capture pleater line
            
            # Add Pleater line to output
            temp_read['Pleater'] = pleater
            data_frames.append(temp_read)
        
        # Create single file from all data frames
        file = pd.concat(data_frames, ignore_index=True)

        # Try: applying the datetime type to the ' Datetime' column
        try:
            file[' DateTime'] = pd.to_datetime(file[' DateTime'])
        except:
            log_custom('INVALID DATE FOUND', 'ERROR') # Convert DateTime column to iso datetime format
        
        return file
        
    def process_file(e=None):
        nonlocal service_sleeping
        service_sleeping = False # Service is now active
        lottie_update()

        update_date_filter()



        execute_time_start = time.time() # Start recording execution time
        csv_file = validity_check() # Correct invalid records
        csv_file = filter_by_date(csv_file)
        
        # Try: Output to csv
        try:
            csv_file.to_csv(selected_folder_path + '\\! - output.csv', index=False) # Return the filtered file content
        except:
            log_custom('File could not be written! Process Aborted. Is the output file opened?', 'ERROR/WARNING')
        
        # Capture execution time
        execute_time_end = time.time()
        execute_time = int((execute_time_end - execute_time_start)*1000)
        log_function('CSV File Processing', execute_time)
        
        update_logs()
        service_sleeping=True # Service is now Sleeping
        lottie_update()
            
    def main_service(e=None):
        nonlocal service_running
        
        if len(selected_file_paths) == 0:
            log_custom('No file selected, service not started', 'WARNING')
            update_logs()
            service_running = False
        else:
            service_running = True
        
        while service_running:
            log_custom(f'Processing files: {selected_files.value}', 'File System')
            process_file()
            log_custom(f'Processed csv into: {selected_folder_path}', 'File System')
            sleep_time = find_sleep_time()
            time.sleep(sleep_time)
        
        button_controls.update()

    # Lottie Flet Control
    lottie = ft.Lottie(
        src='https://lottie.host/be52cd2e-c0c7-47c0-adaa-43e15f5a4696/KzdSRVd2Vi.json',
        background_loading=True,
        fit=ft.ImageFit.CONTAIN,
        height=128,
    )

    # Lottie Flet Control src templates
        # Local lottie file system broken, hosting required -> https://github.com/flet-dev/flet/issues/3083, https://github.com/flet-dev/flet/issues/3082
        # Switching src with a string also broken
        # Must use template lottie control and pull from ft.Lottie.src
    lottie_sleep = ft.Lottie(src='https://lottie.host/cb5a5101-3607-465f-ab76-a98a33aaaed4/ba1gXPDyl2.json')
    lottie_run = ft.Lottie(src='https://lottie.host/3acebf42-a085-441e-97b8-b4a37c178ede/XhmfvlNwQQ.json')
    lottie_stopped = ft.Lottie(src='https://lottie.host/be52cd2e-c0c7-47c0-adaa-43e15f5a4696/KzdSRVd2Vi.json')
    
    # Input File Flet Button
    input_file_button = ft.ElevatedButton(
        text='Input files',
        icon=ft.icons.FILE_OPEN,
        icon_color=ft.colors.BLUE_400,
        on_click=lambda _: pick_file_dialog.pick_files(allow_multiple=True, allowed_extensions=['csv'])
    )

    # Export Folder Flet Button
    output_folder_button = ft.ElevatedButton(
        text='Output Location',
        icon=ft.icons.FOLDER,
        icon_color=ft.colors.AMBER_300,
        on_click=lambda _: pick_folder_dialog.get_directory_path(),
    )

    # Start Service Flet Button
    start_service_button = ft.ElevatedButton(
        text='Start Service',
        icon=ft.icons.PLAY_ARROW,
        icon_color=ft.colors.GREEN_400,
        on_click=main_service
    )

    # Stop Service Flet Button
    stop_service_button = ft.ElevatedButton(
        text='Stop Service',
        icon=ft.icons.STOP,
        icon_color=ft.colors.RED_400,
        on_click=close_service
    )

    # Button Controls Flet Container
    button_controls = ft.Container(
        content=ft.Column(
            controls=[
                lottie,
                input_file_button,
                output_folder_button,
                start_service_button,
                stop_service_button,
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        expand=1,
        padding=ft.padding.all(10)
    )

    # Log text Flet Control
    log_text = ft.Text(value='', color=ft.colors.AMBER_400)

    # Log Flet Container
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
    
    # Main Column
    main_column = ft.Container(
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
    
    page.add(main_column)
    update_logs()

if __name__ == '__main__':
    ft.app(main, assets_dir='assets')