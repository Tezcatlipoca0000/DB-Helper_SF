# Main file
# ISQL # CONNECT "localhost:C:/Users/casa/Desktop/DB-Helper/PDVDATA.FDB" user 'SYSDBA' password 'masterkey';
# CONDA # C:\Users\casa\Desktop\DB-Helper>python main.py enforce=true include=Ricolino,Treviño exclude=Verdura
from get_prov import get_prov
from save_to_db import update_db
from save_to_xl import copy_price
import sys
import os
import subprocess

force = False
incl = []
excl = []
for arg in sys.argv:
    if 'enforce=' in arg:
        x = arg.replace('enforce=', '').lower()
        if x == 'true':
            force = True
    if 'include=' in arg:
        incl = arg.replace('include=', '')
        incl = incl.split(',')
    if 'exclude=' in arg:
        excl = arg.replace('exclude=', '')
        excl = excl.split(',')
    if '-h' in arg or '-help' in arg:
        print("Options:\nenforce=true|false\ninclude=Name1,Name2...\nexclude=Name1,Name2...")
        quit()

print('The update options:', 'enforce:', force, 'include:', incl, 'exclude:', excl)

"""
# make sure server is running
print("Making sure the server is running...")
try:
    service = os.popen("sc query FirebirdGuardianDefaultInstance").read()
    print("Firebird Guardian is ----> ", service, type(service), ("STOPPED" in service), ("RUNNING" in service))
except:
    service = ""
if not "RUNNING" in service:
    result = subprocess.run(["cmd", "/c", "runas", "/user:Admin", "C:\\Users\\casa\\Desktop\\DB-Helper\\initiate_server.cmd"], check=True)
    print(result)
    #prog = subprocess.Popen(['runas', '/profile:Admin', '/user:Admin', 'initiate_server.cmd'], stdin=subprocess.PIPE)
    #prog.stdin.write("123")
    #prog.communicate()
"""    


print('Starting...')
dept_info = get_prov()
dept_err = dept_info['errors']
dict_prov = dept_info['data']
#print('dict_prov ----->', dict_prov)
#print('errors ---->', dept_err)

# First get an excel sheet with all prices from PDV 
print('Making a copy of PVENTA...')
copy_price()

while True:
    proceed = input('A file named "updated-price.xlsx" was created.\nCompare those values of "PVENTA" with "Precio al Público" from "Provedores Todos.xlsx"\nAfter review, copy the values of "Última Rev. Precios"\nThen copy "Provedores Todos" again to the "DB-Helper" folder\n After updating the file, press the corresponding key to continue:\n ----> e) Exit (Without updating the DB)\n ----> c) Continue (update DB)\n ----> ')

    if proceed.upper() == 'C':
        print('Proceeding to update DB...')
        update_db(dict_prov=dict_prov, enforce=force, include=incl, exclude=excl) 
        break
    elif proceed.upper() == 'E':
        print('Exiting system without updating the DB')
        break
