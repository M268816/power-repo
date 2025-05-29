import datetime as dt

START_DATE = dt.datetime(2032,1,1,0,0)
END_DATE = dt.datetime(2032,12,31,0,0)
DATE_CHANGE_STEP = dt.timedelta(days=1)

file = open("test_dst.txt",'a')

def is_dst(day:int, month:int, day_of_week:int) -> bool:
    # checked date - day of week number, sunday = 0
    previous_sunday = day - day_of_week
    
    # month is outside of DST
    if month < 3 or month > 11:
        return False
    # month is within DST
    if month >=4 and month <=10:
        return True
    # month is march
    if month == 3:
        # sunday is not in march
        if previous_sunday <= 0:
            return False
        # checked date is greater than sunday
        # sunday is within the first 2 weeks
        return 8 <= previous_sunday <= day
    # month is november
    if month == 11:
        # sunday is not within november
        if previous_sunday <= 0:
            return True
        # checked date is less than sunday
        # and sunday is within the first week
        return day <= previous_sunday <= 7
    
def test_days():
    
    date_is_dst = False
    test_date = START_DATE
    
    
    while test_date <= END_DATE:
        day_of_week = (test_date.weekday() + 1) % 7 # sunday = 0
        date_is_dst = is_dst(test_date.day, test_date.month, day_of_week)
        str = f'{test_date} is dst? {date_is_dst}'
        # file.write(str + "\n")
        print(str)
        test_date = test_date + DATE_CHANGE_STEP
        
    file.close()
    
if __name__ == "__main__":
    test_days()