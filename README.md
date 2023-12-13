# PLC Trend Data Collection Utility

This Python script logs trend data from a Programmable Logic Controller (PLC) using the `pylogix` library and saves the collected data into a CSV file.

## Features

- Collects data for a predefined list of tags from the PLC.
- Data collection cycles and intervals can be adjusted as needed.
- Writes data to a CSV file with timestamp and index, appending new data at predefined buffer size intervals.
- Creates new directories and files based on the current date for organized data storage.

## Prerequisites

- Python environment with necessary packages installed (`pylogix`, `datetime`, `csv`, etc.).
- Network access to the target PLC with the specified IP address.
- Proper configuration of tags to be logged.

## Installation

Before running the script, ensure that the `pylogix` library is installed and properly configured to connect with your specific PLC model and IP address. Set the device number, trend description, number of cycles, cycle time, buffer size, and PLC IP address at the beginning of the script:

```python
# Settings
device_number = "Blend B"  # part of filename
trend_desc = "Phase 1"  # part of filename
cycles = 99999  # number of samples to take
cycle_time = 1  # time between cycles (Seconds)  
buffer_size = 10  # collect this many rows before saving to file
plc_ip = '192.168.0.1'
```

## How to Use

Simply run the script in your Python environment. The script will automatically start collecting data from the PLC and write to the CSV file at the specified interval. The file and folder structure will be based on the current date and device information provided.

Make sure that the PLC is online and the tags list contains the correct addresses for the data points you wish to log.

## Dependencies

```python
import time
import datetime
import os
import csv
from pylogix import PLC
```

_readme.md genenerated with GPT_
