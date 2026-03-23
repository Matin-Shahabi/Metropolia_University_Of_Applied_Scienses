#EXAM 1

seasons = ("winter", "spring", "summer", "autumn")
month = (int(input("Enter a month(1_12): ")))
if month ==12 or month ==1 or month ==2:
    print(seasons[0])
elif month ==3 or month ==4 or month ==5:
    print(seasons[1])
elif month ==6 or month ==7 or month ==8:
    print(seasons[2])
elif month ==9 or month ==10 or month ==11:
    print(seasons[3])
else:
    print("Invalid month")

# EXAM 2

names = set()
while True:
    name = input("Enter a name: ")
    if name  == "":
        break
    if name in names:
        print("Existing name")
    else:
        print("New name")
        names.add(name)
print("All name :")
for name in names:
    print(name)

#EXAM 3

airport ={}
while True:
    print("1:Add new airport")
    print("2: fetch airport information")
    print("3: Quit")
    choice = int(input("Enter a choice (1-2): "))
    if choice == 1:
        code = input("Enter ICAO code: ")
        name = input("Enter airport name: ")
        airport[code] = name
        print("Airport added")
    elif choice == 2:
        code = input("Enter ICAO code: ")
        if code in airport:
            print("Airport name :")
            print(airport[code])
        else:
            print("Invalid code")
    elif choice == 3:
        print("Quit")
        break
    else:
        print("Invalid choice")


