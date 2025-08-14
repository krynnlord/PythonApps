import os
import json
import time
import base64
from cryptography.fernet import Fernet
from hashlib import sha256

VAULT_FILE = 'tasks.dat'
version_number = '1.1'

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
    site = input("\33[93mTask: \33[0m")
    vault[site] = {'task': site}
    
def view_entry_list(vault: dict, filtered_sites=None):
    if not vault:
        return
    
    print("")
    
    sites = filtered_sites if filtered_sites is not None else list(vault.keys())
    
    if not sites:
        return

    for i, site in enumerate(sites, start=1):
        print("\33[34m"+f"{i}. "+"\33[0m"+ f"{site}")

def delete_entry(vault: dict):
    if not vault:
        print("Vault is empty.")
        return

    sites = list(vault.keys())
    
    print("\33[93mSelect a task to delete:\33[0m\n")
    for i, site in enumerate(sites, start=1):
        
        print("\33[34m"+f"{i}. "+"\33[0m"+ f"{site}")

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
    
    while True:
        master_password = '12345'
        key = derive_key(master_password)
        fernet = Fernet(key)
        vault = load_vault(fernet)
        clear_screen()
        print("\33[93m================================\33[0m")
        print("\33[34m             Tasks    \33[0m")
        print("\33[93m================================\33[0m")
        view_entry_list(vault)
        print("")

        print("[\33[92mA\33[0m] Add Task")
        if vault:
            print("[\33[92mD\33[0m] Delete Task")

      
        print("[\33[92mQ\33[0m] Quit\n")
        
        choice = input("> ").strip().lower()
        clear_screen()
        if choice == 'a':
            add_entry(vault)
            save_vault(vault, fernet)
        elif choice == 'd':
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