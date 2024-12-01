def entering_data():
    name = input('The tournemant name: ')
    starting_date = input("The date of the begining of the tournement: ")
    ending__date = input("The date of the endining of the tournement: ")
    description = input("Please write a description of the tournement: ")
    return name, starting_date, ending__date, description

def starting_tournament():
    print('WELCOME \n Pleas choose your turnement information')
    data = entering_data()
    
    check = "no"
    while check != 'yes':
        print("Thank you for your choice: ")
        print("Check if your data is correct")
        print(f"Tournement name - {data[0]}")
        print(f"Startign date - {data[1]}")
        print(f"Ending date - {data[2]}")
        print(f"Description - {data[3]}")
        print(f"    ")
        print("If your data is fine please write 'yes' ")
        print('If not press any key')
        check = input().lower()
        if check == 'yes':
            break
        print("Lets try again. ")
        data = entering_data()
