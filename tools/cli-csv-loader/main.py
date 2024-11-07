from datetime import datetime, timedelta
import msvcrt
import os
import pandas as pd
from sys import exit
import time
import threading
from tqdm import tqdm

UPDATE_TIME = 3600 # One Hour = 3600 seconds.

def clear_terminal():
    return os.system('cls' if os.name == 'nt' else 'clear')

try:
    FILES = pd.read_csv('./file_locations.csv')
except:
    print(
'''Could not find file_locations.csv.
Please create a csv of file locations to load into the program.

Note: the last location must be a folder location for the output file.

Press Any Key to Exit.'''
    )
    msvcrt.getch()
    exit()
    
# CLI
def main():
    clear_terminal()
    # Init Variables
    exit_flag = False
    date_filter = pd.to_datetime(datetime.today().strftime('%A %B %d %Y'))

    input_files = FILES['Location'][:-1].tolist()
    
    output_folder = FILES['Location'].iloc[-1]
    
    # Init date for data filter
    def update_date_filter():
        nonlocal date_filter
        # date_filter = pd.to_datetime(datetime.today().strftime('%A %B %d %Y'))
        date_filter = pd.to_datetime('2024-10-01 00:00:00') # test date
    
    def find_sleep_time():
        nonlocal date_filter
        start_time = datetime.now()
        end_time = (start_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        sleep_time = (end_time-start_time).total_seconds()
        # print(f'Next runtime in: {round(sleep_time/60, 0)} minutes')
        return int(sleep_time if start_time.minute != 0 else 3600)
      
    def validity_check():
        data_frames = []
        print()
        for i in tqdm(input_files, desc='Validity Check', dynamic_ncols=False, ncols=75):
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
        print('Creating Working File')
        file = pd.concat(data_frames, ignore_index=True)

        # Try: applying the datetime type to the ' Datetime' column
        print('Formatting DateTime to Datetime')
        try:
            file[' DateTime'] = pd.to_datetime(file[' DateTime'])
        except:
            print('INVALID DATE FOUND') # Convert DateTime column to iso datetime format
        
        return file
    
    def filter_by_date(file):
        # Try: Filter by date
        print(f'Filtering records >= {date_filter.strftime('%Y %B %d')}')
        try:
            filtered_file = file[file[' DateTime'] >= date_filter]
            filtered_file = sum_short_stops(filtered_file) # Combine 'Short Stop' records
            filtered_file = sum_not_entered(filtered_file) # Combine 'Not Entered' and Blank records
        except:
            print('INVALID DATE FORMAT FOUND IN DATETIME COLUMN. PROCESS ABORTED')
        
        return filtered_file
    
    def sum_short_stops(file):
        print('Combining Short Stop Records')
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
    
    def sum_not_entered(file):
        print('Combining Not Entered Records')
        not_entered = file.copy()
        not_entered[' Downtime Minutes'] = pd.to_numeric(not_entered[' Downtime Minutes'], errors='coerce')
        
        not_entered[' DateTime'] = not_entered[' DateTime'].dt.date
        not_entered = not_entered[
            (not_entered[' Downtime Reason'] == 'Not Entered') |
            (not_entered[' Downtime Reason'] == '') |
            (not_entered[' Downtime Reason'].isnull())
        ]
        
        not_entered = not_entered.groupby([' DateTime', 'Pleater', ' Shift'])[' Downtime Minutes'].sum()
        not_entered = not_entered.reset_index()
        not_entered['ID'] = 0
        not_entered[' Downtime Reason'] = 'Not Entered'
        not_entered[' Comments'] = 'MERGED RECORDS'
        
        not_entered = not_entered[['ID', ' DateTime', ' Shift', ' Downtime Minutes', ' Downtime Reason', ' Comments', 'Pleater']]

        # Reformat csv file
        file = file[
            ~(
                (file[' Downtime Reason'] == 'Not Entered') |
                (file[' Downtime Reason'] == '') |
                (file[' Downtime Reason'].isnull())
            )
        ]
        file = pd.concat([file, not_entered], ignore_index=True)
        file[' DateTime'] = pd.to_datetime(file[' DateTime'])
        
        return file
    
    def duplicate_check(file):
        print('Dropping possible duplicates')
        filtered_file = file.drop_duplicates(subset=['ID', ' Shift', 'Pleater'])

        return filtered_file
        
    def process_file(e=None):

        update_date_filter()

        execute_time_start = time.time() # Start recording execution time
        csv_file = validity_check() # Correct invalid records
        csv_file = duplicate_check(csv_file)
        csv_file = filter_by_date(csv_file)
        
        # Try: Output to csv
        try:
            csv_file.to_csv(output_folder + '\\! - output.csv', index=False) # Return the filtered file content
        except:
            print('File could not be written! Process Aborted. Is the output file opened?')
        
        # Capture execution time
        execute_time_end = time.time()
        execute_time = int((execute_time_end - execute_time_start)*1000)
        print()
        print(f'CSV File Processed in {execute_time}ms')
            
    def close_service_listener():
        nonlocal exit_flag
        msvcrt.getch()
        exit_flag = True
    
    def main_service(e=None):
        nonlocal exit_flag
        
        if len(input_files) == 0:
            print('No file(s) selected, service not started, import from file_locations.csv. Press any key to exit.')
            msvcrt.getch()
            # service_running = False
            return
        
        listener = threading.Thread(target=close_service_listener, daemon=True)
        listener.start()
        
        bar_format = '{desc}: {remaining}'

        while not exit_flag:
            print('Processing Files:')
            for i in input_files:
                print(i)
            process_file()
            print(f'CSV Saved into: {output_folder}')
            print('You may press any key to exit this service.')
            sleep_time = find_sleep_time()
            for _ in tqdm(range(sleep_time), desc='Next execution in', dynamic_ncols=True, bar_format=bar_format):
                if exit_flag:
                    break
                time.sleep(1)
        print('Service stopped by user.')
    main_service()
    

if __name__ == '__main__':
    main()