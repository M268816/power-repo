import pandas as pd
import datetime as dt
import time
import msvcrt

def main():
    while True: 
        print('Sleeping...')
        time.sleep(5)
        print('Processing...')

        read = pd.read_csv('big_input.csv')
        # read = pd.read_csv('input.csv')

        read[' DateTime'] = pd.to_datetime(read[' DateTime'])

        # datefilter = dt.datetime.today()
        datefilter = pd.to_datetime('01 01 2024 12:00AM')

        filtered = read[read[' DateTime'] > datefilter]

        print(filtered)
        filtered.to_csv('output.csv', index=False)
    
        if msvcrt.kbhit():
            msvcrt.getch()
            print('PROGRAM ENDED')
            break
            
main()