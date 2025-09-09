import os
import json
from datetime import datetime, timedelta
import time
import base64
from cryptography.fernet import Fernet
from hashlib import sha256

VAULT_FILE = 'ndcounties.dat'

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

    site = input("\33[93mCounty Name: \33[0m")
    site_number = input("\33[93mCounty Number: \33[0m")
    site_cities = input("\33[93mCities (space separated): \33[0m")
    vault[site] = {'county': site, 'number' : site_number, 'cities' : site_cities}
    
def view_entry_list(vault: dict, fernet: Fernet, xtra_options, filtered_sites=None):
       
    if not vault:
        return
    
    print("")
    
    sites = filtered_sites if filtered_sites is not None else list(vault.keys())
    sites.sort(key=lambda site: vault[site]['number'])
        
    if not sites:
        return

    for i, site in enumerate(sites, start=1):
        print("\33[34m"+f"{i}. "+"\33[0m"+ f"{vault[site]['number']+" - " +vault[site]['county']}"+"\33[0m")
        
    print("\n")
    
    try: 
        choice = int(input("Enter number (0 to cancel): "))
        clear_screen()

        if choice == 0:
                return
        selected_site = sites[choice - 1] 
        print("\33[92mCounty Information\33[0m")
        print(vault[selected_site]['number']+' - ' + vault[selected_site]['county'] )
        print("\33[92m\nCities\33[0m")
        print(vault[selected_site]['cities'])

        if xtra_options:
            c = input("\n\n\33[93mEnter to continue (c to add cities) \33[0m")
        else:
            c = input("\n\n\33[93mEnter to continue \33[0m")
        if c == "c" and xtra_options:
            add_cities(vault, fernet, selected_site)

    except (ValueError, IndexError):
        return

def add_cities(vault: dict, fernet: Fernet, site: str):
    new_cities = input("\33[93mAdd Cities (space separated): \33[0m")
    if new_cities:
        vault[site]['cities'] += " " + new_cities
        print("✅ Cities added.")
        save_vault(vault, fernet)
        time.sleep(1)    
               
def delete_entry(vault: dict):
    if not vault:
        print("Vault is empty.")
        return

    sites = list(vault.keys())
    sites.sort(key=lambda site: vault[site]['number'])
    
    print("\33[93mSelect a task to delete:\33[0m\n")
    for i, site in enumerate(sites, start=1):
        
        print("\33[34m"+f"{i}. "+"\33[0m"+ f"{vault[site]['county']}"+"\33[0m")
       
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

def get_num_of_entries(vault: dict):
    return len(vault)    

def search_vault(vault: dict, fernet: Fernet, xtra_options):
    term = input("\33[93mSearch: \33[0m").strip().lower()
    matches = [site for site in vault if term in site.lower() or term in vault[site]['cities'].lower()]
    clear_screen()
    view_entry_list(vault, fernet, xtra_options, filtered_sites=matches)
    
def main():
    
    xtra_options = False
       
    while True:
        master_password = '12345'
        key = derive_key(master_password)
        fernet = Fernet(key)
        vault = load_vault(fernet)
        num_of_entries = get_num_of_entries(vault)
        clear_screen()
        print("\33[93m================================\33[0m")
        print("\33[34m           ND Counties    \33[0m")
        if xtra_options:
            print("        Maintenance Mode ")
        print("\33[93m================================\33[0m")
        print("Total Counties: " + str(num_of_entries))
        
        print("")

        print("[\33[92mS\33[0m] Search")
        print("[\33[92mV\33[0m] View Counties")
        if xtra_options:
            print("[\33[92mA\33[0m] Add County")
        if vault and xtra_options:
            print("[\33[92mD\33[0m] Delete County")
        print("[\33[92m?\33[0m] Maintenance Mode")
        print("[\33[92mQ\33[0m] Quit\n")
        
        choice = input("> ").strip().lower()
        clear_screen()
        if choice == 'a' and xtra_options == True:
            add_entry(vault)
            save_vault(vault, fernet)
        elif choice == 's' and vault:
            search_vault(vault,fernet, xtra_options)
        elif choice == 'v' and vault:
            view_entry_list(vault, fernet, xtra_options)    
        elif choice == 'd' and vault and xtra_options == True:
            delete_entry(vault)
            save_vault(vault, fernet)
        elif choice == '?':
            if xtra_options == True:
                xtra_options = False
            else:
                xtra_options = True
        elif choice == 'q':
            save_vault(vault, fernet)
            print("Tasks saved. Exiting.")
            break
        else:
            print("Invalid option.")
        
if __name__ == "__main__":
    main()