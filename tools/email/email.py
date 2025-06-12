from datetime import datetime
import os
import pandas as pd # install pandas and openpyxl
import sqlite3 as sql
import warnings
import win32com.client as client # install pywin32

# ignore openpyxl warnings
warnings.filterwarnings("ignore", category=UserWarning ,module="openpyxl")

# clear terminal
os.system('cls' if os.name == 'nt' else 'clear')

print("--- STARTING ---")

# init vars here because pylance is stupid
received_time = None
iso_week = None
excel_file = pd.DataFrame()
completed_qty = None
trx_value = None
xl_filter = None
xl_completed_qty = None
xl_trx_value = None
xlt_filter = None
xlt_completed_qty = None
xlt_trx_value = None
ssc_filter = None
ssc_completed_qty = None
ssc_trx_value = None
v_filter = None
v_completed_qty = None
v_trx_value = None

# Init Save locations
input_save_location = "C:\\Users\\M268816\\OneDrive - MerckGroup\\Desktop\\python_inputs"
input_save_as = "INPUT.xlsx"
input_path = os.path.join(input_save_location,input_save_as)
output_save_location = "C:\\Users\\M268816\\OneDrive - MerckGroup\\Desktop\\python_outputs"
output_save_as = "OUTPUT.csv"
output_path = os.path.join(output_save_location,output_save_as)
database_location = "C:\\Users\\M268816\\OneDrive - MerckGroup\\Desktop\\python_db"
database_name = "DATABASE.sqlite"
database_path = os.path.join(database_location,database_name)

# Create sql cursor
SQL_CONNECTION = sql.connect(database_path)
SQL_CURSOR = SQL_CONNECTION.cursor()

# Create Summary SQL Database if none exists
SQL_CURSOR.execute("""--sql
CREATE TABLE IF NOT EXISTS summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT NOT NULL,
    date DATETIME NOT NULL,
    week REAL NOT NULL,
    quantity REAL NOT NULL,
    transactions REAL NOT NULL
    )
""")
SQL_CONNECTION.commit()

# Get Outlook Client
outlook = client.Dispatch("Outlook.Application")
namespace = outlook.getNameSpace("MAPI") # MAPI = email type
inbox = namespace.GetDefaultFolder(6)
emails = inbox.Items

# Sort emails by time, descending order = True
emails.Sort("[ReceivedTime]", True)

# supply email filter
sender_filter = "j-supplychainreports@milliporesimga.com"
print(f"Looking for: {sender_filter}")
print("----------")

# catch newest email from sender_filter and pull attachment
for email in emails:
    try:
        if email.SenderEmailAddress == sender_filter:
            print(f"Found: {email.Subject}")
            received_time = datetime.date(email.ReceivedTime).strftime("%Y-%b-%d")
            iso_week = datetime.date(email.ReceivedTime).isocalendar().week
            print(f"Received on: {received_time}")
            print("----------")
            
            # Check if the email has attachments
            if email.Attachments.Count > 0:
                for i in range(1, email.Attachments.Count+1):
                    attachment = email.Attachments.Item(i)
                    attachment_name = attachment.FileName
                    # Save the attachment
                    print(f"Attachment pulled: {attachment_name}")
                    print(f"Saving to: {input_path}")
                    print("----------")
                    attachment.SaveAsFile(f"{input_path}")
            break
    # Throw any exceptions    
    except Exception as e:
        print(f"Exception: {e}")

# Open excel file with pandas
try:
    excel_file = pd.read_excel(input_path)
    print("--- EXCEL FILE LOADED ---")
except Exception as e:
    print(f"Excel File Load Exception: {e}")

# Summarize
try:
    working_file = excel_file.copy()
    print("--- WORKING FILE CREATED ---")
    
    # Total
    completed_qty = working_file["Qty Completed"].sum()
    trx_value = working_file["TRX_VALUE"].sum()
    
    # XL
    xl_filter = working_file[working_file["Department"] == "Opti XL"].copy()
    xl_completed_qty = xl_filter["Qty Completed"].sum()
    xl_trx_value = xl_filter["TRX_VALUE"].sum()
    
    # XLT
    xlt_filter = working_file[working_file["Department"] == "Opti XLT"].copy()
    xlt_completed_qty = xlt_filter["Qty Completed"].sum()
    xlt_trx_value = xlt_filter["TRX_VALUE"].sum()
    
    # SSC
    ssc_filter = working_file[working_file["Department"] == "Small Scale Capsule"].copy()
    ssc_completed_qty = ssc_filter["Qty Completed"].sum()
    ssc_trx_value = ssc_filter["TRX_VALUE"].sum()
    
    # SSC Pleating
    v_filter = working_file[working_file["Department"] == "Opti XL Subs"].copy()
    v_completed_qty = v_filter["Qty Completed"].sum()
    v_trx_value = v_filter["TRX_VALUE"].sum()
    
    # Round Summaries
    trx_value = round(trx_value, 2)
    xl_trx_value = round(xl_trx_value, 2)
    xlt_trx_value = round(xlt_trx_value, 2)
    ssc_trx_value = round(ssc_trx_value, 2)
    v_trx_value = round(v_trx_value, 2)
    
    print("--- SUMMARIES CREATED ---")
except Exception as e:
    print(f"Could not create summaries: {e}")

# Create new dataframe for sql transfer
summary = pd.DataFrame(
    {
        "Department": [
            "XL",
            "XLT",
            "SSC",
            "SSC Pleating",
            "Total"
        ],
        "Date": [received_time] * 5,
        "Week": [iso_week] * 5,
        "Quantity": [
            xl_completed_qty,
            xlt_completed_qty,
            ssc_completed_qty,
            v_completed_qty,
            completed_qty
        ],
        "Transactions": [
            xl_trx_value,
            xlt_trx_value,
            ssc_trx_value,
            v_trx_value,
            trx_value
        ]
    }
)
print("--- NEW DATAFRAME CREATED ---")

# Export dataframe to csv
### TODO: transfer csv to sharepoint list through power automate
try:
    summary.to_csv(output_path,index=False,lineterminator="")
    print("--- DATAFRAME CSV SAVED ---")
except Exception as e:
    print(f"Could not save file: {e}")

# Add New Rows to SQL Database from summary dataframe
for index, row in summary.iterrows():
    SQL_CURSOR.execute("""--sql
        SELECT COUNT(*) from summary
        WHERE date = ? and department = ?
        """,
        (row["Date"],row["Department"])
    )
    department = row["Department"]
    count = SQL_CURSOR.fetchone()[0]
    if count == 0:
        SQL_CURSOR.execute("""
            INSERT INTO summary (department, date, week, quantity, transactions)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                row["Department"],
                row["Date"],
                row["Week"],
                row["Quantity"],
                row["Transactions"]
            )
        )
    else:
        print(f"Entry already exists for {department} on {row["Date"]}. Data not added.")
    
SQL_CONNECTION.commit()
print("--- NEW SUMMARY SAVED TO DATABASE ---")
SQL_CONNECTION.close()

print("--- COMPLETE ---")
exit()