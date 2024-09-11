#!/usr/bin/env python3

#####################################################################################3
import subprocess
import yaml
import re
import os

from yamldb import YamlDB    # Configuration and Data DB
db = YamlDB(filename="data/db.yaml")

verbose = 0
data_structure = {}

##############################################################################
# Tools

# Example usage:
# directory_path = '/path/to/directory'
# create_directory_if_not_exists(directory_path)
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")
    else:
        print(f"Directory '{directory}' already exists.")

##############################################################################
# Obtain data from ESP board
bash_command = "esptool.py flash_id"

# Execute the command
process = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the command to complete
stdout, stderr = process.communicate()

# Check if there was an error
if process.returncode != 0:
    print("Error running 'esptool.py'")
    print("-- Please ensure that there is an ESPboard plugged in.")
    # print(stderr)
    quit()

flash_id = stdout.decode().strip().split('\n')

data_structure['flash_id'] = flash_id

##############################################################################
# Decode data

regex_pattern = r'^Detecting chip type... (.+)$'
pattern1 = re.compile(regex_pattern)

regex_pattern = r'^Chip is (.+)$'
pattern2 = re.compile(regex_pattern)

regex_pattern = r'^MAC: (.{17})$'
pattern3 = re.compile(regex_pattern)

data = {}

for line in flash_id:
    if verbose: print(f"  {line}");

    match = re.search(pattern1, line)
    if match:
        if verbose: print(f"Regex match found in: {line} {match[1]}")
        data['chip'] = match[1]

    match = re.search(pattern2, line)
    if match:
        if verbose: print(f"Regex match found in: {line} {match[1]}")
        data['chip_decription'] = match[1]

    match = re.search(pattern3, line)
    if match:
        if verbose: print(f"Regex match found in: {line} {match[1]}")
        data['mac'] = match[1]


        regexp_pattern= r'\:'
        pattern4 = re.compile(regexp_pattern)
        match = pattern4.sub('',data['mac'])

        regexp_pattern= r'^......'
        pattern5 = re.compile(regexp_pattern)
        match = pattern5.sub('',match)

        match = match.upper()
        data['id'] =  match

        data_structure['chip'] = data

data_structure["device"]   = db["device"]
data_structure["customer"] = db["customer"]
data_structure["site"]     = db["site"]
data_structure["comment"]  = db["comment"]

##############################################################################
# Report Data
print("Device Hardware")
print("---------------")
for key in data.keys():
    print("{s:20} {data}".format(s=key, data=data[key]))
print()
print("Details")
print("-------")
print("Device:   {}".format(data_structure["device"]))
print("Customer: {}".format(data_structure["customer"]))
print("Site:     {}".format(data_structure["site"]))
print("Comment :")
print("{}".format(data_structure["comment"]))
print()
##############################################################################
# Save Data

datadir = "data"
devicedir = datadir+"/units/"+data['id']

# Example usage:
create_directory_if_not_exists(datadir)
create_directory_if_not_exists(devicedir)

# Convert the data structure to YAML
yaml_data = yaml.dump(data_structure, default_flow_style=False, indent=2)

datafile = devicedir+"/device.yaml"

# Example: Write YAML to a file
with open(datafile, 'w') as file:
    file.write(yaml_data)

    print("YAML exported successfully.")
