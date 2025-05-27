import os
import json
import base64
import getpass
from cryptography.fernet import Fernet
from hashlib import sha256

VAULT_FILE = 'vault.dat'

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

def add_entry(vault: dict, PASS_VIS):
    site = input("Site name: ")
    username = input("Username: ")
    if PASS_VIS == True:
        password = input("Enter password: ")
    else:
        password = getpass.getpass("Enter password: ")
    vault[site] = {'username': username, 'password': password}
    print(f"Entry for '{site}' added.")

def view_entry_list(vault: dict, filtered_sites=None):
    if not vault:
        print("Vault is empty.")
        return

    sites = filtered_sites if filtered_sites is not None else list(vault.keys())
    sites.sort(key=str.lower)

    if not sites:
        print("No entries found.")
        return

    print("\nStored sites:")
    for i, site in enumerate(sites, start=1):
        print(f"{i}. {site}")

    try:
        selection = int(input("\nEnter the number of the site to view (0 to cancel): "))
        if selection == 0:
            return
        selected_site = sites[selection - 1]
        creds = vault[selected_site]
        print(f"\nSite: {selected_site}")
        print(f"Username: {creds['username']}")
        print(f"Password: {creds['password']}")
    except (ValueError, IndexError):
        print("Invalid selection.")

def view_vault(vault: dict):
    sorted_sites = sorted(vault.keys(), key=str.lower)
    view_entry_list(vault, filtered_sites=sorted_sites)

def search_vault(vault: dict):
    term = input("Search site name: ").strip().lower()
    matches = [site for site in vault if term in site.lower()]
    view_entry_list(vault, filtered_sites=matches)

def change_password(vault: dict,PASS_VIS):
    if not vault:
        print("Vault is empty.")
        return

    sites = sorted(vault.keys(), key=str.lower)
    print("\nSelect a site to change its password:")
    for i, site in enumerate(sites, start=1):
        print(f"{i}. {site}")

    try:
        selection = int(input("\nEnter number (0 to cancel): "))
        if selection == 0:
            return
        selected_site = sites[selection - 1]
        print(f"\nCurrent username: {vault[selected_site]['username']}")
        print(f"Current password: {vault[selected_site]['password']}")
        if PASS_VIS == False:
            new_password = getpass.getpass("Enter new password: ")
        else:
            new_password = input("Enter new password: ")
        vault[selected_site]['password'] = new_password
        print(f"Password for '{selected_site}' updated.")
    except (ValueError, IndexError):
        print("Invalid selection.")

def delete_entry(vault: dict):
    if not vault:
        print("Vault is empty.")
        return

    sites = sorted(vault.keys(), key=str.lower)
    print("\nSelect a site to delete:")
    for i, site in enumerate(sites, start=1):
        print(f"{i}. {site}")

    try:
        selection = int(input("\nEnter number (0 to cancel): "))
        if selection == 0:
            return
        selected_site = sites[selection - 1]

        confirm = input(f"Are you sure you want to delete '{selected_site}'? (y/N): ").strip().lower()
        if confirm == 'y':
            del vault[selected_site]
            print(f"✅ Entry for '{selected_site}' deleted.")
        else:
            print("Cancelled.")
    except (ValueError, IndexError):
        print("Invalid selection.")

def change_master_password(vault: dict, current_key: bytes,PASS_VIS) -> bytes:
    print("\n=== Change Master Password ===")

    # Confirm old password works by decrypting vault file
    try:
        fernet = Fernet(current_key)
        _ = load_vault(fernet)  # This ensures it's decryptable
    except:
        print("Current master password is incorrect.")
        return current_key

    # Ask for new password
    while True:
        if PASS_VIS == False:
            new_password = getpass.getpass("Enter new master password: ")
            confirm_password = getpass.getpass("Confirm new master password: ")
        else:
            new_password = input("Enter new master password: ")
            confirm_password = input("Confirm new master password: ")
        if new_password == confirm_password:
            break
        else:
            print("Passwords do not match. Try again.")

    # Derive new key
    new_key = derive_key(new_password)
    new_fernet = Fernet(new_key)

    # Save vault with new key
    save_vault(vault, new_fernet)
    print("✅ Master password changed.")
    return new_key
        
def main():
    PASS_VISIBLE = False
    PASS_CHANGED = False
    clear_screen()
    print("================================")
    print("    Richard's Password Vault    ")
    print("================================")
    master_password = getpass.getpass("Enter master password: ")
    key = derive_key(master_password)
    fernet = Fernet(key)

    vault = load_vault(fernet)

    while True:
        clear_screen()
        print("================================")
        print("    Richard's Password Vault    ")
        print("================================")
        print("\n[A] Add entry\n[V] View list\n[S] Search\n[D] Delete entry\n[C] Change password\n[M] Change Master password\n[Y] Password visibility", end=" ")
        if PASS_VISIBLE == True:
            print("[Currently: \33[32m"+str(PASS_VISIBLE)+"\33[0m]\n[Q] Quit\n")
        else:
            print("[Currently: \33[31m"+str(PASS_VISIBLE)+"\33[0m]\n[Q] Quit\n")
        choice = input("> ").strip().lower()
        clear_screen()
        if choice == 'a':
            add_entry(vault,PASS_VISIBLE)
            save_vault(vault, fernet)
        elif choice == 'v':
            view_vault(vault)
        elif choice == 's':
            search_vault(vault)
        elif choice == 'c':
            change_password(vault,PASS_VISIBLE)
            save_vault(vault, fernet)
        elif choice == 'd':
            delete_entry(vault)
            save_vault(vault, fernet)
        elif choice == 'y':
            if PASS_VISIBLE == True:
                PASS_VISIBLE = False 
            else:
                PASS_VISIBLE = True 
            PASS_CHANGED = True
        elif choice == 'm':
            key = change_master_password(vault, key, PASS_VISIBLE)
            fernet = Fernet(key)  # <== this ensures future saves use the new key
        elif choice == 'q':
            save_vault(vault, fernet)
            print("Vault saved. Exiting.")
            break
        else:
            print("Invalid option.")
        if PASS_CHANGED == False:
            input("\nPress Enter to continue...")
        PASS_CHANGED = False

if __name__ == "__main__":
    main()
