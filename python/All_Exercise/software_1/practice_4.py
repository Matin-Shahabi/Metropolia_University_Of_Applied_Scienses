#Excercise 1

number =1
while number <= 1000:
    if number % 3 == 0:
        print(number)
    number += 1

#Excercise 2

number = float(input("Enter length in inches(negative value to quite:"))
while number >= 0:
    centimeters = number *2.54
    print(centimeters)
    break

# Excercise 3

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
    if correct_username == username and correct_password == password:
        print("welcome")
        break
    else:
        print("Wrong username or password")
        break










