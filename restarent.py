amount=0;
print ("MENU")
print ("1. VEG")
print ("2. NON-VEG")
choice=int(input("Select Ur choice"))
if choice==1:
    print ("1. Dosa-30 2. Idlay-40")
    v_choice=int(input("Select Ur choice"))
    if v_choice==1:
        print ("You selected Dosa , Enter Number of plate")
        P_choice=int(input(""))
        amount=amount+(30*P_choice)
        print amount
        
    
