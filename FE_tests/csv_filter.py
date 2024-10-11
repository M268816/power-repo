import flet as ft
import pandas as pd

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
    def close_service(e):
        page.window.destroy()

    def main_service(e=None):
        # Start the main csv filter service
        pass

    def update_logs():
        # Update a log file with data when the service runs
        pass

    def process_file(e=None):
        # Get CSV from input.
        csv_file = pd.read_csv('input.csv')
        # Convert DateTime column to iso datetime format
        csv_file[' DateTime'] = pd.to_datetime(csv_file[' DateTime'])
        # Specify a datetime to start the filter
        datefilter = pd.to_datetime('01 01 2024 12:00AM')
        # Filter the input csv by dates later than the datefiter
        filtered_file = csv_file[csv_file[' DateTime'] <= datefilter]
        filtered_file.to_csv('output.csv', index=False)
        # Return the filtered file content
        print(filtered_file)
        return filtered_file
    # REMOVE THIS TEST INIT BEFORE PROD
    csv = process_file()
    
    # File Selection Control
    selected_files = ft.Text()
    def pick_file_resut(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ', '.join(map(lambda f: f.name, e.files)) if e.files else 'Cancelled!'
        )
        if selected_files.value != None:
            service_running = True
        selected_files.update()
    pick_file_dialog = ft.FilePicker(on_result=pick_file_resut)
    page.overlay.append(pick_file_dialog)
    
    # Lottie Control
    lottie_sleep = ft.Lottie(
        src='https://lottie.host/cb5a5101-3607-465f-ab76-a98a33aaaed4/ba1gXPDyl2.json',
        background_loading=True,
        fit=ft.ImageFit.CONTAIN,
        height=100,
    )
    lottie_run = ft.Lottie(
        src='https://lottie.host/c73c5b70-9054-4afd-b4f7-083dd99a5688/ulBgMv7UDS.json',
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
    
    def lottie_update(e=None):
        if service_running:
            if service_sleeping:
                return lottie_sleep
            else:
                return lottie_run
        else:
            return lottie_stopped
            
    lottie_display = lottie_update()

    # Button Controls
    button_controls = ft.Container(
        content=ft.Column(
            controls=[
                lottie_display,
                ft.ElevatedButton('Pick the input file.', disabled=service_running, on_click=lambda _: pick_file_dialog.pick_files(allow_multiple=False)),
                selected_files,
                ft.ElevatedButton('Start Service', disabled=service_running, on_click=main_service),
                ft.ElevatedButton('Close Service', on_click=close_service),
                ft.ElevatedButton('Manual Run', on_click=process_file),
                ft.Text(f'Next Update scheduled for: '),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        expand=1,
        bgcolor=ft.colors.AMBER,
        padding=ft.padding.all(10)
    )

    # Log File
    log_controls = ft.Container(
        content=ft.Column(
            controls=[
                # Change this to display the log file for prod
                ft.Text(csv)
            ],
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
        ),
        bgcolor=ft.colors.BLUE_GREY_50,
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
            ]

        ),
        expand=True,
        bgcolor= ft.colors.WHITE,
        border_radius= 5,
        padding= ft.padding.all(5),
    )
    
    # Main Container
    main_window = ft.Container(
        content=ft.Column(
            controls=[
                main_row,
            ]
        ),
        expand=True,
        padding= ft.padding.all(5)
    )
    page.add(main_window)

if __name__ == '__main__':
    ft.app(flet)