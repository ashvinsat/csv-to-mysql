import sys
import mysql.connector
import os
import csv
import configparser as cfg
import linecache as lr

parser = cfg.RawConfigParser()
file = "info.ini"
parser.read(file)
hostname = parser.get("Info", "hostname")
username = parser.get("Info", "username")
passwordname = parser.get("Info", "password")
databasename = parser.get("Info", "database")

mydb = mysql.connector.connect(
  host=hostname,
  user=username,
  password= passwordname,
  database=databasename,
  auth_plugin = "mysql_native_password"
)
cx = mydb.cursor()

csvname = input("Enter file name: ")

if os.path.isfile(csvname):
  if not csvname.endswith('.csv'):
    print("File is not a csv file. Run the program again.")
    sys.exit()
  else:
    pass
else:
  print("File does not exist. Try running the file in the right directory.")
  sys.exit()

tnl = os.path.splitext(csvname)
tablename = str(tnl[0]).replace(" ", "_").replace("-", "")

import csv
with open(csvname, 'r') as file:
    reader = csv.reader(file)
    columns = (next(reader))
columns = str(columns)
columnames = columns.replace('[', '').replace(']', '').replace("'", "`")
columns = columns.replace('[', '').replace(']', '').replace("',","' VARCHAR(255),").replace("'", "`")
columns = columns + " VARCHAR(255)"
file.close()
cx.execute("CREATE TABLE IF NOT EXISTS " + tablename + "(" + columns + ")")

with open(csvname, 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
        # Iterate over each row after the header in the csv
        for row in csv_reader:
            row = str(row).replace('[', '').replace(']', '')
            cx.execute("INSERT INTO " + tablename + " (" + columnames + ") " + "VALUES (" + row + ") ")
            mydb.commit()
print("Success.")