''' Small script that extracts all passwords of all saved wifi profiles on Win 10 '''

import subprocess
import re   # regex
import os
import json

# get all saved WIFI profiles
profiles = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
profiles = (re.findall("All User Profile     : (.*)\r", profiles))

# save the wifi networks
wifi_list = []

if profiles:
    for ssid in profiles:
        wifi_profile = {}   # a dict for each profile containing SSID and passwd
        wifi_profile["ssid"] = ssid

        # get passwords as clear text
        passwd = subprocess.run(["netsh", "wlan", "show", "profile", ssid, 'key=clear'], capture_output=True).stdout.decode()
        passwd = re.search("Key Content            : (.*)\r", passwd)

        if passwd == None:
            # skip wifi profiles without a password
            pass
        else:
            wifi_profile["passwd"] = passwd[1]

        wifi_list.append(wifi_profile) 

    for item in wifi_list:
        print(item)

    # aks for save to file
    cmd = input('\rSave results as JSON file? (y/n) ')
    filename = 'results.json'
    if cmd == 'y' or cmd == 'Y':
        with open(filename, 'w') as file:
            json.dump(wifi_list, file)

        print(f'Saved file to {os.getcwd()}\\{filename}')
else:
    print('There seem to be no saved WIFI profiles on this machine.')
