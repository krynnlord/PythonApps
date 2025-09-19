import os
import json
from datetime import datetime, timedelta
import time
import base64
import pyperclip
from cryptography.fernet import Fernet
from hashlib import sha256

VAULT_FILE = 'notes/notes.dat'

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
    name = input("\33[93mNote Name: \33[0m")
    site = input("\33[93mNew Note: \33[0m")
    vault[site] = {'task': site, 'name' : name, 'time' : current_time}
    
def view_entry_list(vault: dict, filtered_sites=None):
       
    if not vault:
        return
    
    print("")
    
    sites = filtered_sites if filtered_sites is not None else list(vault.keys())
    sites.sort(key=lambda site: vault[site]['name'])
        
    if not sites:
        return

    for i, site in enumerate(sites, start=1):
        print("\33[34m"+f"{i}. "+"\33[0m"+ f"{vault[site]['name']}"+"\33[0m")
        
    print("\n")
    
    try: 
        choice = int(input("Enter number (0 to cancel): "))
        clear_screen()

        if choice == 0:
                return
        selected_site = sites[choice - 1] 
        print("\33[92mNote\33[0m")
        print(vault[selected_site]['name'])
        print("\33[92m\nDetails\33[0m")
        print(vault[selected_site]['task'])

        c = input("\n\n\33[93mEnter to continue (c to copy) \33[0m")
        if c.lower() == 'c':
            pyperclip.copy(f"{vault[selected_site]['task']}")
            print("✅ Note copied to clipboard.")
            time.sleep(1)
    
    except (ValueError, IndexError):
        return
    
               
def delete_entry(vault: dict):
    if not vault:
        print("Vault is empty.")
        return

    sites = list(vault.keys())
    sites.sort(key=lambda site: vault[site]['time'])
    
    print("\33[93mSelect a task to delete:\33[0m\n")
    for i, site in enumerate(sites, start=1):
        
        print("\33[34m"+f"{i}. "+"\33[0m"+ f"{vault[site]['name']}"+"\33[0m")
       
    try:
        selection = int(input("\nEnter number (0 to cancel): "))
        if selection == 0:
            return
        selected_site = sites[selection - 1]

        del vault[selected_site]
        print(f"✅ Note deleted.")
        
    except (ValueError, IndexError):
        print("Invalid selection.")
    
    time.sleep(1)

def get_num_of_entries(vault: dict):
    return len(vault)    
    
def main():
       
    while True:
        master_password = '12345'
        key = derive_key(master_password)
        fernet = Fernet(key)
        vault = load_vault(fernet)
        num_of_entries = get_num_of_entries(vault)
        clear_screen()
        print("\33[93m================================\33[0m")
        print("\33[34m              Notes    \33[0m")
        print("\33[93m================================\33[0m")
        print("Note Count: ", num_of_entries)#view_entry_list(sorter, timestamp, vault)
        print("")

        print("[\33[92mA\33[0m] Add Note")
        if vault:
            print("[\33[92mV\33[0m] View Note")
            print("[\33[92mD\33[0m] Delete Note")
        print("[\33[92mQ\33[0m] Quit\n")
        
        choice = input("> ").strip().lower()
        clear_screen()
        if choice == 'a':
            add_entry(vault)
            save_vault(vault, fernet)
        elif choice == 'v' and vault:
            view_entry_list(vault)    
        elif choice == 'd' and vault:
            delete_entry(vault)
            save_vault(vault, fernet)
        elif choice == 'q':
            save_vault(vault, fernet)
            print("Tasks saved. Exiting.")
            break
        else:
            print("Invalid option.")
        
if __name__ == "__main__":
    main()