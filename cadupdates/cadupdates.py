import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def list_updates(database,current_step):
    print("")
    if database == 1:
        print("1.  DB1DR" , end="") 
    else: 
        print("1.  DB1", end="")
    if current_step < 2:
        print("")
    if current_step == 2:
        print("\33[93m In Progress\33[0m")
    if current_step >2:
        print("\33[92m ✓\33[0mComplete")
    print("2.  ITDDESOCMQ1", end="")
    if current_step < 4:
        print("")
    if current_step == 4:
        print("\33[93m In Progress\33[0m")
    if current_step >4:
        print("\33[92m ✓\33[0mComplete")
    print("3.  ITDDESOCMQ2", end="")
    if current_step < 6:
        print("")
    if current_step == 6:
        print("\33[93m In Progress\33[0m")
    if current_step >6:
        print("\33[92m ✓\33[0mComplete")
    print("4.  ITDDESOCMQ3", end="")
    if current_step < 8:
        print("")
    if current_step == 8:
        print("\33[93m In Progress\33[0m")
    if current_step >8:
        print("\33[92m ✓\33[0mComplete")
    print("5.  ITDDESOCISM1", end="")
    if current_step < 10:
        print("")
    if current_step == 10:
        print("\33[93m In Progress\33[0m")
    if current_step >10:
        print("\33[92m ✓\33[0mComplete")
    print("6.  ITDDESOCISM2", end="")
    if current_step < 12:
        print("")
    if current_step == 12:
        print("\33[93m In Progress\33[0m")
    if current_step > 12:
        print("\33[92m ✓\33[0mComplete")
    print("7.  ITDDESOCWEBAPP1", end="" )
    if current_step < 14:
        print("")
    if current_step == 14:
        print("\33[93m In Progress\33[0m")
    if current_step >14:
        print("\33[92m ✓\33[0mComplete")
    print("8.  ITDDESOCWEBAPP2", end="")
    if current_step < 16:
        print("")
    if current_step == 16:
        print("\33[93m In Progress\33[0m")
    if current_step >16:
        print("\33[92m ✓\33[0mComplete")
    print("9.  ITDDESOCIF1", end="")
    if current_step < 18:
        print("")
    if current_step == 18:
        print("\33[93m In Progress\33[0m")
    if current_step >18:
        print("\33[92m ✓\33[0mComplete")
    print("10. ITDDESOCIF2", end="")
    if current_step < 20:
        print("")
    if current_step == 20:
        print("\33[93m In Progress\33[0m")
    if current_step >20:
        print("\33[92m ✓\33[0mComplete")
            
    print("")
    
    print("2 Days Later:")
    if database == 2:
        print("1.  DB1DR" , end="") 
    else: 
        print("1.  DB1", end="")
    if current_step < 22:
        print("")
    if current_step == 22:
        print("\33[93m In Progress\33[0m")
    if current_step >22:
        print("\33[92m ✓\33[0mComplete")
    print("2.  ITDDESOCMQ4", end="")
    if current_step < 24:
        print("")
    if current_step == 24:
        print("\33[93m In Progress\33[0m")
    if current_step >24:
        print("\33[92m ✓\33[0mComplete")
    print("3.  ITDDESOCMQ5", end="")
    if current_step < 26:
        print("")
    if current_step == 26:
        print("\33[93m In Progress\33[0m")
    if current_step >26:
        print("\33[92m ✓\33[0mComplete")
    print("4.  ITDDESOCMQ6", end="")
    if current_step < 28:
        print("")
    if current_step == 28:
        print("\33[93m In Progress\33[0m")
    if current_step >28:
        print("\33[92m ✓\33[0mComplete")
    
    print("")

def print_extras(current_step):
    print("\33[93m==============================================\33[0m")
    print("Modules that are red and in Manual mode")
    print("are now normal and can be ignored.")
    print("")
    print ("Failover the database and check Xalt\n")
    print("\33[35mMQ Services Shutdown Procedure\33[0m")
    print("1. rabbitmq-upgrade drain")
    print("2. rabbitmq-service stop\n")
    print("Current Step: " , end="")
    show_current_step(current_step)
    print("\33[93m==============================================\33[0m\n")
    
def show_current_step(current_step):
    print(f"\33[92m({current_step})\33[0m")
    
def mark_next_step(current_step):
    if current_step != 29:
        current_step += 1
        return current_step
    else:
        return current_step

def back_step(current_step):
    if current_step != 1:
        current_step -= 1
        return current_step
    else:
        return current_step   

def reset_updates(current_step):
    current_step = 1
    return current_step

def save_to_file(current_step,database):
    with open("cadupdates/cadupdates.txt", "w") as f:
        f.write(f"{current_step},{database}")

def load_from_file():
    if os.path.exists("cadupdates/cadupdates.txt"):
        with open("cadupdates/cadupdates.txt", "r") as f:
            data = f.read().strip().split(",")
            if len(data) == 2:
                try:
                    current_step = int(data[0])
                    database = int(data[1])
                    if current_step < 1 or current_step > 29 or database not in [1, 2]:
                        return 1, 1
                    return current_step, database
                except ValueError:
                    return 1, 1
    return 1, 1
        
def main():
    
    current_step = 1
    database = 1
    extraflag = False
    current_step, database = load_from_file()
    while True:          
        
        clear_screen()
        print("\33[93m================================\33[0m")
        print("\33[34m           CAD Updates    \33[0m")
        print("\33[93m================================\33[0m")
        list_updates(database,current_step)
        if extraflag == True:
            print_extras(current_step)
        print("[\33[92m1\33[0m] Next Step ")
        print("[\33[92m2\33[0m] Backup Step ")
        print("[\33[92mC\33[0m] Change Primary Database", end="")
        if database == 1:
            print("\33[34m (DB1)\33[0m")
        if database == 2:
            print("\33[34m (DB1DR)\33[0m")
        print("[\33[92mR\33[0m] Reset Update List")
        print("[\33[92m?\33[0m] Toggle Extra Info")
        print("[\33[92mQ\33[0m] Quit\n")
        
        choice = input("> ").strip().lower()
        clear_screen()
        if choice == '1':
            current_step = mark_next_step(current_step)
        if choice == '2':
            current_step = back_step(current_step)
        elif choice == 'c':
            database = 2 if database == 1 else 1
        elif choice == 'r':
            current_step = reset_updates(current_step)
        elif choice == '?':
            if extraflag == False:
                extraflag = True
            else:
                extraflag = False  
        elif choice == 'q':
            save_to_file(current_step,database)
            break
        else:
            print("Invalid option.")
        
if __name__ == "__main__":
    main()