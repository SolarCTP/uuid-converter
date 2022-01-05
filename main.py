#!/usr/bin/env python3

import json
from os import rename
from sys import argv
import glob
import requests

# Specify an API to fetch dd
converter = "http://tools.glowingmines.eu/convertor/uuid/"

# Take old UUID (if valid) and get new UUID from "converter", than rename each file
def convert_uuid(datfile):

    uuid = datfile[-40:-4].strip("-")
    print("Looking up UUID:", uuid)
    response = json.loads(requests.get(converter + uuid).content)
    if "error" in response:
        invalid_uuids.append(uuid)
        print(f"Invalid UUID:    {uuid}")
    else:
        new_uuid = response["offlinesplitteduuid"]
        print(f"New UUID:        {new_uuid}")
        rename(f"{data_folder}/{uuid}.dat", f"{data_folder}/{new_uuid}.dat")


data_folder = argv[1]
print(data_folder)

if not data_folder:
    print("No folder specified")
    quit()

datafiles_list = glob.glob(data_folder + "/*.dat")
invalid_uuids = [] # all invalid (non-premium or wrong) UUIDs will be added here
if len(datafiles_list) == 0:
    print("The selected folder does not contain any .DAT files")
else:
    for dat in datafiles_list:
        convert_uuid(dat)
    if not invalid_uuids == []:
        print("The following UUID's are not valid and weren't updated:\n" + "\n".join(invalid_uuids))
