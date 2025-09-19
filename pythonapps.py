import os
import subprocess

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def confirmexit():
    while True:
        choice = input("Are you sure you want to exit? (y/n): ").strip().lower()
        if choice == 'y':
            return True
        else:
            return False
    
def main():
       
    while True:
        clear_screen()
        print("\33[93m================================\33[0m")
        print("\33[34m           Python Apps    \33[0m")
        print("\33[93m================================\33[0m")
        print("")

        print("[\33[92m1\33[0m] Tasks")
        print("[\33[92m2\33[0m] Password Vault")
        print("[\33[92m3\33[0m] Notes")
        print("[\33[92m4\33[0m] ND Counties")
        print("[\33[92m5\33[0m] Contacts")
        print("")
        print("[\33[92mQ\33[0m] Quit")
        print("")
        choice = input("> ").strip().lower()
        
        if choice == '1':
            subprocess.run(['python', 'tasks/tasks.py'])
        elif choice == '2':
            subprocess.run(['python', 'vault/vault.py'])
        elif choice == '3':
            subprocess.run(['python', 'notes/notes.py'])
        elif choice == '4':
            subprocess.run(['python', 'ndcounties/ndcounties.py'])
        elif choice == '5':
            subprocess.run(['python', 'contacts/contacts.py'])
        elif choice == 'q':
            if confirmexit():
                break   
        clear_screen()
        
if __name__ == "__main__":
    main()