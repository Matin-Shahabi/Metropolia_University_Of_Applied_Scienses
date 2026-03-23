#Excercise 1

number = 1
while number <= 1000:
    if number % 3 == 0:
        print(number)
    number += 1

#Excercise 2

inches = float(input("Enter a number in inches: "))
if inches > 0:
    print(inches + 2.5)
else:
    print("end")

#Excercise 3
smallest = None
largest = None
while True :
    user_input = input("Enter a number(press Enter to stop: ")
    if user_input == "":
        break
    number = int(user_input)
    if smallest is  None or number < smallest:
        smallest = number
    if largest is  None or number  > largest:
        largest = number
    print("smallest: ", smallest)
    print("largest: ", largest)

#Excercise 4

import random
secret_number = random.randint(1, 10)
while True:
    guess = int(input("Guess a number: "))
    if guess < secret_number:
        print("Too low")
    elif guess > secret_number:
            print("Too high")
    if guess == secret_number:
        print("correct")
        break

#Excercise 5

correct_username = "python"
correct_password = "rules"
attempt =0
while attempt < 5:
    attempt += 1
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if correct_username == correct_username and correct_password == correct_password:
        print("welcome")
        break
    else:
        print("Wrong username or password")
        break

    #Exre..6

    import random
    N= int(input("Enter a number: "))










