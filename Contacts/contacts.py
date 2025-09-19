import os
import csv
import time

CSV_FILE = 'contacts/contacts.csv'
FIELDS = ['first_name', 'last_name', 'title', 'phone_number', 'email']

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def load_contacts() -> dict:
    if not os.path.exists(CSV_FILE):
        return {}
    contacts = {}
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row['first_name']
            contacts[key] = row
    return contacts

def save_contacts(data: dict):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for contact in data.values():
            writer.writerow(contact)

def add_entry(contacts: dict):
    first_name = input("\33[93mFirst Name: \33[0m")
    last_name = input("\33[93mLast Name: \33[0m")
    title = input("\33[93mTitle: \33[0m")
    phone_number = input("\33[93mPhone Number: \33[0m")
    email = input("\33[93mEmail: \33[0m")
    contacts[first_name] = {
        'first_name': first_name,
        'last_name': last_name,
        'title': title,
        'phone_number': phone_number,
        'email': email
    }

def view_entry_list(contacts: dict, filtered=None):
    if not contacts:
        return
    print("")
    sites = filtered if filtered is not None else list(contacts.keys())
    sites.sort(key=lambda site: contacts[site]['last_name'])
    if not sites:
        return
    for i, site in enumerate(sites, start=1):
        print("\33[34m"+f"{i}. "+"\33[0m"+ f"{contacts[site]['last_name']}" + ", " + f"{contacts[site]['first_name']}" + "\33[0m")
    print("\n")
    try:
        choice = int(input("Enter number (0 to cancel): "))
        clear_screen()
        if choice == 0:
            return
        selected = sites[choice - 1]
        print("\33[92mContact Information\33[0m\n")
        print("\33[34mName:  \33[0m"+ contacts[selected]['first_name'] + " " + contacts[selected]['last_name'])
        print("\33[34mTitle: \33[0m"+ contacts[selected]['title'])
        print("\33[34mPhone: \33[0m"+ contacts[selected]['phone_number'])
        print("\33[34mEmail: \33[0m"+ contacts[selected]['email'])
        input("\n\33[93mEnter to continue \33[0m")
    except (ValueError, IndexError):
        return

def delete_entry(contacts: dict):
    if not contacts:
        print("Vault is empty.")
        return
    sites = list(contacts.keys())
    sites.sort(key=lambda site: contacts[site]['last_name'])
    print("\33[93mSelect a contact to delete:\33[0m\n")
    for i, site in enumerate(sites, start=1):
        print("\33[34m"+f"{i}. "+"\33[0m"+ f"{contacts[site]['last_name']}" + ", " + f"{contacts[site]['first_name']}" + "\33[0m")
    try:
        selection = int(input("\nEnter number (0 to cancel): "))
        if selection == 0:
            return
        selected = sites[selection - 1]
        del contacts[selected]
        print(f"✅ Contact deleted.")
    except (ValueError, IndexError):
        print("Invalid selection.")
    time.sleep(1)

def get_num_of_entries(contacts: dict):
    return len(contacts)

def search_contacts(contacts: dict):
    term = input("\33[93mSearch: \33[0m").strip().lower()
    matches = [site for site in contacts if
               term in site.lower() or
               term in contacts[site]['first_name'].lower() or
               term in contacts[site]['last_name'].lower() or
               term in contacts[site]['title'].lower() or
               term in contacts[site]['phone_number'].lower() or
               term in contacts[site]['email'].lower()]
    clear_screen()
    view_entry_list(contacts, filtered=matches)

def main():
    xtra_options = False
    while True:
        contacts = load_contacts()
        num_of_entries = get_num_of_entries(contacts)
        clear_screen()
        print("\33[93m================================\33[0m")
        print("\33[34m            Contacts   \33[0m")
        if xtra_options:
            print("        Maintenance Mode ")
        print("\33[93m================================\33[0m")
        print("Total Contacts: " + str(num_of_entries))
        print("")
        print("[\33[92mS\33[0m] Search")
        print("[\33[92mV\33[0m] View Contacts")
        if xtra_options:
            print("[\33[92mA\33[0m] Add Contact")
        if contacts and xtra_options:
            print("[\33[92mD\33[0m] Delete Contact")
        if xtra_options:
            print("[\33[92m?\33[0m] Normal Mode")
        else:
            print("[\33[92m?\33[0m] Maintenance Mode")
        print("[\33[92mQ\33[0m] Quit\n")
        choice = input("> ").strip().lower()
        clear_screen()
        if choice == 'a' and xtra_options == True:
            add_entry(contacts)
            save_contacts(contacts)
        elif choice == 's' and contacts:
            search_contacts(contacts)
        elif choice == 'v' and contacts:
            view_entry_list(contacts)
        elif choice == 'd' and contacts and xtra_options == True:
            delete_entry(contacts)
            save_contacts(contacts)
        elif choice == '?':
            xtra_options = not xtra_options
        elif choice == 'q':
            save_contacts(contacts)
            print("Contacts saved. Exiting.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()