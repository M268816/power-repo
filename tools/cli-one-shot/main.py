from datetime import datetime, timedelta, date, timezone, time
from sys import exit

import os
import pandas as pd

# Collects timestamp of the start of the process.
SERVICE_START = datetime.strftime(datetime.now(), '%d-%m-%Y, %H:%M:%S')

# Try: Open or create the error log.
try:
    ERROR_LOG = open('./error_log.txt', 'at')
except Exception as e:
    print(str(e))

# Try: Open or create the run log. Write the start time.
try:
    RUN_LOG = open('./run_log.txt', 'at')
    RUN_LOG.write(f'\n[ NEW OPERATION ] Operation Started at: {SERVICE_START}.\n')
except Exception as e:
    ERROR_LOG.write(f'[ERROR] Could not open or write the run_log.txt file.\n')
    ERROR_LOG.write(str(e)+'\n')
    exit()

# Try: Read the csv file paths located from file_locations.csv
try:
    FILES = pd.read_csv('./file_locations.csv')
except Exception as e:
    ERROR_LOG.write(f'[ERROR] Could not read the file_locations.csv file.\n')
    ERROR_LOG.write(str(e) + '\n')
    exit()

def clear_terminal():
    return os.system('cls' if os.name == 'nt' else 'clear')
    
def main():    
    # Init Variables
    date_filter = pd.to_datetime(datetime.combine(date=date.today(),time=time(0))) - timedelta(hours=1)
    # date_filter = pd.to_datetime('2024-10-01 00:00:00') # test date
    input_files = FILES['Location'][:-1].tolist()
    output_folder = FILES['Location'].iloc[-1]
      
    def clean_csvs():
        data_frames = []
        print()
        for i in input_files:
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
            
            # New Pleater Capture
            #   Split i(path) by '\',
            #   return last string [-1](file name),
            #   split file name by '_',
            #   return first string [0]
            pleater = i.split('\\')[-1].split('_')[0]
            
            # Add Pleater line to output
            temp_read['Pleater'] = pleater
            data_frames.append(temp_read)
        
        # Create single file from all data frames
        print('Creating Working File')
        cleaned_file = pd.concat(data_frames, ignore_index=True)

        # Try: applying the datetime type to the ' Datetime' column
        print('Formatting DateTime to Datetime')
        try:
            cleaned_file[' DateTime'] = pd.to_datetime(cleaned_file[' DateTime'])
        except Exception as e:
            ERROR_LOG.write(str(e) + 'INVALID DATE FOUND\n') # Convert DateTime column to iso datetime format
        
        return cleaned_file
    
    def sum_short_stops(input_file):
        print('Combining Short Stop Records')
        short_stops = input_file.copy()
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
        summed_file = summed_file[summed_file[' Downtime Reason'] != 'Short Stop']
        summed_file = pd.concat([summed_file, short_stops], ignore_index=True)
        summed_file[' DateTime'] = pd.to_datetime(summed_file[' DateTime'])
        
        return summed_file
    
    def sum_not_entered(input_file):
        print('Combining Not Entered Records')
        not_entered = input_file.copy()
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
        summed_file = summed_file[
            ~(
                (summed_file[' Downtime Reason'] == 'Not Entered') |
                (summed_file[' Downtime Reason'] == '') |
                (summed_file[' Downtime Reason'].isnull())
            )
        ]
        summed_file = pd.concat([summed_file, not_entered], ignore_index=True)
        summed_file[' DateTime'] = pd.to_datetime(summed_file[' DateTime'])
        
        return summed_file
    
    def filter_by_date(input_file):
        # Try: Filter by date
        print(f'Filtering records >= {date_filter}')
        filtered_file = input_file
        try:
            filtered_file = input_file[input_file[' DateTime'] >= date_filter]
            filtered_file = sum_short_stops(filtered_file) # Combine 'Short Stop' records
            filtered_file = sum_not_entered(filtered_file) # Combine 'Not Entered' and Blank records
        except Exception as e:
            ERROR_LOG.write(str(e) + ' INVALID DATE FORMAT FOUND IN DATETIME COLUMN. PROCESS ABORTED\n')
        
        return filtered_file
    
    def duplicate_check(input_file):
        print('Dropping possible duplicates')
        filtered_file = input_file.drop_duplicates(subset=['ID', ' Shift', 'Pleater'])
        return filtered_file
        
    def process_files():
        execute_time_start = datetime.now(timezone.utc)
        csv_file = clean_csvs()
        csv_file = filter_by_date(csv_file)
        csv_file = duplicate_check(csv_file)
        
        # Try: Output to csv
        try:
            csv_file.to_csv(output_folder + '\\! - output.csv', index=False) # Return the filtered file content
        except Exception as e:
            ERROR_LOG.write(str(e) + 'Output file could not be written! Process Aborted. Is the output file opened?')
        
        # Capture execution time
        execute_time_end = datetime.now(timezone.utc)
        execute_time = execute_time_end - execute_time_start
        execute_time = round(execute_time.total_seconds()*1000,0)
        RUN_LOG.write(f'CSV Files Processed in {execute_time}ms.\n')
        RUN_LOG.write(f'CSV Saved into: {output_folder}\n')
        print(f'CSV Files Processed in {execute_time}ms')
        print(f'CSV Saved into: {output_folder}')
    
    def main_service():
        if len(input_files) == 0:
            RUN_LOG.write('No file(s) selected, service not started, import from file_locations.csv.\n')
            return

        clear_terminal()
        
        print(f'[{datetime.now()}] Processing Files:')
        for i in input_files:
            print(i)
        process_files()

        SERVICE_STOP = datetime.strftime(datetime.now(), '%d-%m-%Y, %H:%M:%S')
        RUN_LOG.write(f'Service Ended: {SERVICE_STOP}\n')
        RUN_LOG.close()
        ERROR_LOG.close()

    main_service()
    

if __name__ == '__main__':
    main()