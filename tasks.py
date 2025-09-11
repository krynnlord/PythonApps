import os
import json
from datetime import datetime, timedelta
import time
import base64
from cryptography.fernet import Fernet
from hashlib import sha256

VAULT_FILE = 'tasks.dat'

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def derive_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(sha256(password.encode()).digest())

def load_vault(fernet: Fernet) -> dict:
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, 'rb') as f:
        encrypted_data = f.read()
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data)
    except:
        print("Invalid master password or corrupted vault.")
        exit(1)

def save_vault(data: dict, fernet: Fernet):
    with open(VAULT_FILE, 'wb') as f:
        encrypted_data = fernet.encrypt(json.dumps(data).encode())
        f.write(encrypted_data)

def add_entry(vault: dict):
    current_date = datetime.now()
    current_time = current_date.strftime("%m/%d/%Y %I:%M%p")
    site = input("\33[93mTask: \33[0m")
    vault[site] = {'task': site, 'priority': '3', 'time' : current_time}

def change_priority(sorter, vault: dict):
    if not vault:
        print("Vault is empty.")
        return

    sites = list(vault.keys())
    if sorter == 1:
        sites.sort(key=lambda site: vault[site]['priority'])
    if sorter == 2:
        sites.sort(key=lambda site: vault[site]['time'])
    
    print("\33[93mSelect a task:\33[0m\n")
    for i, site in enumerate(sites, start=1):
        
        if vault[site]['priority'] == '3':
            print("\33[34m"+f"{i}. "+"\33[0m"+ f"{site}"+"\33[0m")
        if vault[site]['priority'] == '2':
            print("\33[34m"+f"{i}. "+"\33[93m"+ f"{site}"+"\33[0m")    
        if vault[site]['priority'] == '1':
            print("\33[34m"+f"{i}. "+"\033[0;31m"+ f"{site}"+"\33[0m")  

    try:
        
        selection = int(input("\nEnter number (0 to cancel): "))
        if selection == 0:
            return
        selected_site = sites[selection - 1]

        print("\n1 - \033[0;31mCritical\33[0m  " ,end="")
        print("2 - \33[93mImportant\33[0m  ", end="")
        print("3 - Normal")
        pri = input("Set Priority: ")
        if pri == '0':
            return
        if pri == '1' or pri == '2' or pri == '3':
            vault[selected_site]['priority'] = pri
                
    except (ValueError, IndexError):
        print("Invalid selection.")
      
def view_entry_list(sorter, timestamp, vault: dict, filtered_sites=None):
       
    if not vault:
        return
    
    print("")
    
    sites = filtered_sites if filtered_sites is not None else list(vault.keys())
    if sorter == 1:
        sites.sort(key=lambda site: vault[site]['priority'])
    if sorter == 2:
        sites.sort(key=lambda site: vault[site]['time'])
        
    if not sites:
        return

    for i, site in enumerate(sites, start=1):
        
        current_pri_string = 'Normal'
        
        if vault[site]['priority'] == '1':
            current_pri_string = 'Critical'
        if vault[site]['priority'] == '2':
            current_pri_string = 'Important'
        if vault[site]['priority'] == '3':
            current_pri_string = 'Normal'
        
        # Overdue calculation !-1 week
        task_time = datetime.strptime(vault[site]['time'], "%m/%d/%Y %I:%M%p")
        overdue1 = (datetime.now() - task_time) > timedelta(days=7)
        weeks_overdue = (datetime.now() - task_time).days // 7
        
        if vault[site]['priority'] == '3':
            print("\33[34m"+f"{i}. "+"\33[0m"+ f"{site}"+"\33[0m", end="")
            if overdue1:
                print(" \033[0;31m!\33[0m", end="")
            if timestamp == True:
                print()
                print("\33[34mCreated:\33[0m", vault[site]['time'],end="")
                print("\33[34m Priority:\33[0m", current_pri_string, end="")
                if overdue1:
                    print("\033[034m Overdue:\33[0m " + str(weeks_overdue) +" week")
                else:
                    print(" \033[034mOverdue:\33[0m No")  
        if vault[site]['priority'] == '2':
            print("\33[34m"+f"{i}. "+"\33[93m"+ f"{site}"+"\33[0m", end="")
            if overdue1:
                print(" \033[0;31m!\33[0m", end="")
            if timestamp == True:
                print()
                print("\33[34mCreated:\33[0m", vault[site]['time'],end="")
                print("\33[34m Priority:\33[0m", current_pri_string, end="")
                if overdue1:
                    print("\033[034m Overdue:\33[0m " + str(weeks_overdue) +" week")
                else:
                    print(" \033[034mOverdue:\33[0m No")   
        if vault[site]['priority'] == '1':
            print("\33[34m"+f"{i}. "+"\033[0;31m"+ f"{site}"+"\33[0m", end="")
            if overdue1:
                print(" \033[0;31m!\33[0m", end="")
            if timestamp == True:
                print()
                print("\33[34mCreated:\33[0m", vault[site]['time'],end="")
                print("\33[34m Priority:\33[0m", current_pri_string, end="")
                if overdue1:
                    print("\033[034m Overdue:\33[0m " + str(weeks_overdue) +" week")
                else:
                    print(" \033[034mOverdue:\33[0m No") 
        print()
        
def delete_entry(sorter, vault: dict):
    if not vault:
        print("Vault is empty.")
        return

    sites = list(vault.keys())
    if sorter == 1:
        sites.sort(key=lambda site: vault[site]['priority'])
    if sorter == 2:
        sites.sort(key=lambda site: vault[site]['time'])
    
    print("\33[93mSelect a task to delete:\33[0m\n")
    for i, site in enumerate(sites, start=1):
        
        if vault[site]['priority'] == '3':
            print("\33[34m"+f"{i}. "+"\33[0m"+ f"{site}"+"\33[0m")
        if vault[site]['priority'] == '2':
            print("\33[34m"+f"{i}. "+"\33[93m"+ f"{site}"+"\33[0m")    
        if vault[site]['priority'] == '1':
            print("\33[34m"+f"{i}. "+"\033[0;31m"+ f"{site}"+"\33[0m")  
       
    try:
        selection = int(input("\nEnter number (0 to cancel): "))
        if selection == 0:
            return
        selected_site = sites[selection - 1]

        del vault[selected_site]
        print(f"✅ Task deleted.")
        
    except (ValueError, IndexError):
        print("Invalid selection.")
    
    time.sleep(1)
    
    
def main():
    
    timestamp = False
    sorter = 1
    
    while True:
        master_password = '12345'
        key = derive_key(master_password)
        fernet = Fernet(key)
        vault = load_vault(fernet)
        clear_screen()
        print("\33[93m================================\33[0m")
        print("\33[34m             Tasks    \33[0m")
        print("\33[93m================================\33[0m")
        view_entry_list(sorter, timestamp, vault)
        print("")

        print("[\33[92mA\33[0m] Add Task")
        if vault:
            print("[\33[92mD\33[0m] Delete Task")
            print("[\33[92mP\33[0m] Change Priority")
            print("[\33[92mT\33[0m] Timestamp Toggle")
            print("[\33[92mS\33[0m] Sort Method ", end="")
            if sorter == 1:
                print("(\33[34mPriority\33[0m)")
            if sorter == 2:
                print("(\33[34mDate Added\33[0m)")
        print("[\33[92mQ\33[0m] Quit\n")
        
        choice = input("> ").strip().lower()
        clear_screen()
        if choice == 'a':
            add_entry(vault)
            save_vault(vault, fernet)
        elif choice == 'p':
            change_priority(sorter, vault)
            save_vault(vault, fernet)
        elif choice == 'd':
            delete_entry(sorter, vault)
            save_vault(vault, fernet)
        elif choice == 't':
            if timestamp == True:
                timestamp = False
            else:
                timestamp = True
        elif choice == 's':
            if sorter == 1:
                sorter = 2
            else:
                sorter = 1
        elif choice == 'q':
            save_vault(vault, fernet)
            print("Tasks saved. Exiting.")
            break
        else:
            print("Invalid option.")
        
if __name__ == "__main__":
    main()