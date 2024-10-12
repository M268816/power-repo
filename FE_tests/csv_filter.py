import flet as ft
import pandas as pd
import time
import logging
import os
from datetime import datetime

# Update This to be able to pick the start date to full from.
DEFAULT_DATE_FILTER = pd.to_datetime('01 01 2020 12:00AM')

UPDATE_TIME = 3600 # One Hour = 3600 secconds.
LOG_DATE = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename=f'logs/service_log_{LOG_DATE}.txt',
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%m-%d-%Y %I:%M:%S %p'
)

def log_function(func_name, duration_ms):
    log_message = f'{func_name}: Completed in {duration_ms}ms'
    logging.info(log_message)

def flet(page: ft.page):
    # Format Window
    page.title = 'CSV Filter Service for PowerApps'
    page.bgcolor = ft.colors.CYAN_100
    page.padding = ft.padding.all(5)
    page.window.height = 420
    page.window.min_height = 420
    page.window.width = 1100
    page.window.min_width = 1100

    # Init Variables
    service_running=False
    service_sleeping=False
    
    # Main Methods
    # Log Control
    log_text = ft.Text(value='', color=ft.colors.AMBER_400)

    # Lottie Control
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
        height=100,
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

    # File Selection Control
    selected_files = ft.Text()
    selected_file_path = None
    def pick_file_result(e: ft.FilePickerResultEvent):
        nonlocal selected_files
        nonlocal selected_file_path
        selected_files.value = (
            ', '.join(map(lambda f: f.name, e.files)) if e.files else 'Cancelled!'
        )
        selected_file_path = e.files[0].path
        selected_files.update()
    pick_file_dialog = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(pick_file_dialog)
    
    def process_file(e=None):
        nonlocal service_sleeping
                
        service_sleeping = False
        lottie_update()
        
        execute_time_start = time.time()
        
        # Get CSV from input.
        csv_file = pd.read_csv(selected_file_path)
        # Convert DateTime column to iso datetime format
        csv_file[' DateTime'] = pd.to_datetime(csv_file[' DateTime'])
        # Specify a datetime to start the filter
        datefilter = DEFAULT_DATE_FILTER
        # Filter the input csv by dates later than the datefiter
        filtered_file = csv_file[csv_file[' DateTime'] >= datefilter]
        filtered_file.to_csv('output.csv', index=False)
        # Return the filtered file content
        
        execute_time_end = time.time()
        execute_time = int((execute_time_end - execute_time_start)*1000)
        log_function('csv process', execute_time)
        
        service_sleeping=True
        lottie_update()
        update_logs()
        
    def update_logs():
        nonlocal log_text
        log_text.value = open(f'logs/service_log_{LOG_DATE}.txt', 'r').read()
        log_text.update()
    
    def close_service(e):
        nonlocal service_running
        service_running = False
        log_function('Service Closed', 0)
        update_logs()

    def main_service(e=None):
        nonlocal service_running
        if selected_file_path == None:
            log_function('No file selected, service not started', 0)
            update_logs()
        else:
            service_running = True
        button_controls.update()
        while service_running:
            process_file()
            time.sleep(UPDATE_TIME)

    # Button Controls
    button_controls = ft.Container(
        content=ft.Column(
            controls=[
                lottie,
                ft.ElevatedButton('Pick the input file.', on_click=lambda _: pick_file_dialog.pick_files(allow_multiple=False, allowed_extensions=['csv'])),
                selected_files,
                ft.ElevatedButton('Start Service', on_click=main_service),
                ft.ElevatedButton('Stop Service', on_click=close_service),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        expand=1,
        padding=ft.padding.all(10)
    )

    # Log File
    log_controls = ft.Container(
        content=ft.Column(
            controls=[
                log_text
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
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
    ft.app(flet, assets_dir='assets')
