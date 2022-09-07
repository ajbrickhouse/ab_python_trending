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
plc_ip = '33.7.0.1'

tags = ["BLD01_PIT01_00.SMTH",
        "BLD01_PIT04_00.SMTH",
        "BLD01_PIT05_00.SMTH",
        "BLD01_PT21_00.SMTH",
        "BLD01_PT21_02.SMTH",
        "BLD01_PT22_00.SMTH",
        "BLD01_PT22_02.SMTH",
        "BLD01_PIT00_00.SMTH",
        "BLD01_P21_00_PV.SMTH",
        "BLD01_P22_00_PV.SMTH",
        "BLD01_TT21_00.SMTH",
        "BLD01_TT21_01.SMTH",
        "BLD01_TT22_00.SMTH",
        "BLD01_TT22_01.SMTH",
        "BLD01_TT40_00.SMTH",
        "BLD01_TT41_00.SMTH",
        "BLD01_TT42_00.SMTH",
        "BLD01_TT43_00.SMTH",
        "BLD01_TT44_00.SMTH",
        "BLD01_PT80_00.SMTH",
        "BLD01_PT80_01.SMTH",
        "BLD01_FT80_00.SMTH",
        "BLD01_FT80_01.SMTH",
        "BLD01_PT40_00.SMTH",
        "BLD01_PT40_01.SMTH",
        "BLD01_FT40_00.SMTH",
        "BLD01_FT40_01.SMTH",
        "BLD01_PT41_00.SMTH",
        "BLD01_PT41_01.SMTH",
        "BLD01_FT41_00.SMTH",
        "BLD01_FT41_01.SMTH",
        "BLD01_PT42_00.SMTH",
        "BLD01_PT42_01.SMTH",
        "BLD01_FT42_00.SMTH",
        "BLD01_FT42_01.SMTH",
        "BLD01_PT43_00.SMTH",
        "BLD01_PT43_01.SMTH",
        "BLD01_FT43_00.SMTH",
        "BLD01_FT43_01.SMTH",
        "BLD01_PT44_00.SMTH",
        "BLD01_PT44_01.SMTH",
        "BLD01_FT44_00.SMTH",
        "BLD01_FT44_01.SMTH",
        "BLD01_AT21_01.SMTH",
        "BLD01_AT22_01.SMTH",
        "BLD01_AT62_00.SMTH",
        "BLD01_AT63_00.SMTH",
        "BLD01_AT62_01.SMTH",
        "BLD01_AT63_01.SMTH",
        "BLD01_WT21_00.SMTH",
        "BLD01_WT22_00.SMTH",
        "BLD01_AT21_00.SMTH",
        "BLD01_AT22_00.SMTH",
        "BLD01_AT40_00.SMTH",
        "BLD01_AT41_00.SMTH",
        "BLD01_AT42_00.SMTH",
        "BLD01_AT43_00.SMTH",
        "BLD01_AT44_00.SMTH"]

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
        # print(row)
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
        except KeyboardInterrupt:
            sys.exit()
        except:
            print("Failed to write to file...")
            pass

        time.sleep(cycle_time) # pause the loop for the desired time