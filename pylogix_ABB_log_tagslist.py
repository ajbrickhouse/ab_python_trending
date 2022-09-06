import time
import datetime
import os
import sys
import csv

sys.path.append('..')
from pylogix import PLC

# Settings
device_number = "Blend B" # part of filename
trend_desc = "Phase 1" # part of filename
cycles = 99999 # number of samples to take
cycle_time = 1 # time between cycles (Seconds)  
buffer_size = 10 # collect this many rows before saving
plc_ip = '192.168.1.1'

# # Blend A
# tags = ['BLD01_PT90_00.SMTH',
#         'BLD01_PT90_01.SMTH',
#         'BLD01_AT90_00.SMTH',
#         'BLD01_FT90_00.SMTH',
#         'BLD01_PT90_02.SMTH',
#         'BLD01_TT90_00.SMTH',
#         'BLD01_FT90_01.SMTH',
#         'BLD01_AT90_01.SMTH',
#         'BLD01_TT90_01.SMTH',
#         'BLD01_TT90_02.SMTH',
#         'BLD01_AT90_02.SMTH',
#         'BLD01_FCV90_00_PID.SO',
#         'BLD01_FCV90_01_PID.SO']

#Blend B
tags = ['BLD01_PT91_00.SMTH',
        'BLD01_PT91_01.SMTH',
        'BLD01_AT91_00.SMTH',
        'BLD01_FT91_00.SMTH',
        'BLD01_PT91_02.SMTH',
        'BLD01_TT91_00.SMTH',
        'BLD01_FT91_01.SMTH',
        'BLD01_AT91_01.SMTH',
        'BLD01_TT91_01.SMTH',
        'BLD01_TT91_02.SMTH',
        'BLD01_AT91_02.SMTH',
        'BLD01_FCV91_00_PID.SO',
        'BLD01_FCV91_01_PID.SO']

# Building first row of CSV (Header)
col_tags = []
col_tags = tags.copy()  # copy the tags list and append two columns in the beginning for datetime and index
col_tags.insert(0,'DateTime')
col_tags.insert(0,'Index')

trend_start_time = time.time() # get the epoch time when the trend program starts.
todays_date = datetime.datetime.today().strftime('%Y-%m-%d')
full_path = f'{todays_date}/{device_number}/'

print(f'Maximum number of cycles: {cycles}')
print(f'Time between cycles: {cycle_time}')
print(f'Estimated trend time: {(cycle_time*cycles)/60} minutes / {((cycle_time*cycles)/60)/60} hours')
print(f'PLC IP address: {plc_ip}')

if not os.path.exists(full_path): # check if a folder with todays date as the name exist
    os.makedirs(full_path) # if it does not, make it.
    print(f"'{full_path}' dir created.")

# create a new filename using the epoch time and trend file name var
rel_path = f"{todays_date}/{device_number}/{device_number}__{trend_desc}__{trend_start_time}.csv" 
with open(rel_path, 'w') as csv_file: 
    csv_file = csv.writer(csv_file, delimiter=',', lineterminator='\n', quotechar='/', quoting=csv.QUOTE_MINIMAL)
    csv_file.writerow(col_tags) # write header row with tag names to the CSV
    print(f"'{rel_path}' created.")

# Print CSV header
print(f'\n{col_tags}')

# data buffer
data_buffer = []

# exception handling
with PLC() as comm: 
    # connect
    comm.IPAddress = plc_ip 

    for cycle in range(cycles):
        ret = comm.Read(tags) # get info on all tags in the list
        row = [x.Value for x in ret] # Get the tag values from the info
        row.insert(0, str(datetime.datetime.now())) # Insert the current DateTime into the begining of the list
        row.insert(0, cycle) # Insert the current Index into the begining of the list
        data_buffer.append(row) # append row data into buffer
        try:
            if len(data_buffer) >= buffer_size: # if the buffer has reached the buffer_size, start saving.
                with open(f"{todays_date}/{device_number}/{device_number}__{trend_desc}__{trend_start_time}.csv", 'a') as csv_file: # append CSV file with data
                    csv_file = csv.writer(csv_file, delimiter=',', lineterminator='\n', quotechar='/', quoting=csv.QUOTE_MINIMAL)
                    # write the data_buffer to file
                    for row_in_buffer in data_buffer:
                        csv_file.writerow(row_in_buffer)
                        print(row_in_buffer)

                    data_buffer = [] # reset list so len goes to 0
        except:
            print("Failed to write to file...")
            pass

        time.sleep(cycle_time) # pause the loop for the desired time


