import os
import getpass
import sys
import ctypes

ISSRPS_Path = r'C:\Windows\System32\IntegratedServicesRegionPolicySet.json'
EEA_Strings = '"AT", "BE", "BG", "CH", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", "GF", "GP", "GR", "HR", "HU", "IE", "IS", "IT", "LI", "LT", "LU", "LV", "MT", "MQ", "NL", "NO", "PL", "PT", "RE", "RO", "SE", "SI", "SK", "YT"'

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        print("This script requires administrative privileges. Please run it as an administrator.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

run_as_admin()

if not os.path.exists(ISSRPS_Path):
    print(f"File {ISSRPS_Path} does not exist.")
    sys.exit()

print(f"Taking ownership of {ISSRPS_Path}...")
os.system(f'takeown /f "{ISSRPS_Path}" /A')

print(f"Setting permissions for {ISSRPS_Path}...")
os.system(f'icacls "{ISSRPS_Path}" /grant {getpass.getuser()}:F')

print(f"Removing EEA strings from {ISSRPS_Path}...")
with open(ISSRPS_Path, 'r') as file:
    data = file.read()
    data = data.replace(EEA_Strings, '""')
    file.close()
print(f"Removed EEA strings from {ISSRPS_Path}.")

print(f"Deleting original {ISSRPS_Path}...")
os.remove(ISSRPS_Path)
print(f"Original {ISSRPS_Path} deleted.")

print(f"Writing changes to {ISSRPS_Path}...")
with open(ISSRPS_Path, 'w') as file:
    file.write(data)
    file.close()
print(f"Changes written to {ISSRPS_Path}.")
print(f'Checking modifications...')
with open(ISSRPS_Path, 'r') as file:
    data = file.read()
    if EEA_Strings in data:
        print(f"EEA strings still present in {ISSRPS_Path}.")
        print(f"Failed !")
    else:
        print(f"EEA strings successfully removed from {ISSRPS_Path}.")
        print(f"Done ! Remember to restart your computer for the changes to take effect.")
    file.close()
input("Press Enter to exit...")
