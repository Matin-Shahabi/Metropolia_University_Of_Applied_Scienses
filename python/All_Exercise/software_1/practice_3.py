#
# age = int(input("Enter age: "))
# if 15 <= age < 18:
#     weight = float(input("Enter weight (kg): "))
# if (age >=18 or age>=15 and weight >=55):
#     print("The medicine can be used.")
# age = int(input("Enter age: "))
# if 15 <= age < 18:
#     weight = float(input("Enter weight (kg): "))
# if (age >=18 or age>=15 and weight >=55):
#     print("The medicine can be used.")
# else:
#     print("The medicine cannot be used.")
#
# age = int(input("Enter your age: "))
# if age>=18:
#     print("You can vote.")
# elif age<18:
#     print("You can not vote.")
# else:
#     different = 18- age
#     print (f"You are a small child.")
#
# consumption = float(input("Enter your favorite number: "))
# if consumption <= 50:
#     print (" bill cost is 0.1")
# elif consumption >200 :
#     print ("bill cost is 0.8")
# elif consumption >50 or consumption >200:
#     print ("bill cost is 0.6")
# else:
#     print ( "finnish")
# physical_score = int(input("Enter your physic grade: "))
# math = int(input("Enter your math grade: "))
# chemistry_score = int(input("Enter your chemistry grade: "))
# if physical_score  <=50 or math <= 50 or chemistry_score <= 50 :
#     print ("your score is too low")
# elif chemistry_score >= 95 :
#     print (" you can give scholarship")
# elif physical_score >=90 and math >=90 :
#     print (" you can give scholarship")
# else:
#     print (" you can  not give scholarship")
# score = int(input("Enter your score: "))
# if score >= 90:
#     print("Your score is good")
# elif score < 50:
#     print("Your score is bad")
# elif score >= 50 or score < 90 :
#     print("Your score is better")
# else:
#     print(" good lock")
#
# Exercise 1
# length = int(input("Enter the length of fish (cm): "))
# if length < 42 :
#     difference = 42 - length
#     print(f"Fish is {difference} cm. you back into the lake.")
# else :
#     print ("you got it")
#
# # Exercise 2
# cabin_class = input("Enter the cabin class:")
# if cabin_class == "lux":
#     print("upper desk cabin with a balcony.")
# elif cabin_class == "A":
#     print("Above the car desk, equipped with a window")
# elif cabin_class == "B":
#     print("Windowless cabin above the car desk.")
# elif cabin_class == "C":
#     print("Windowless cabin below the car desk.")
# else:
#     print("Cabin not recognized.")
#
# #Exercise 3
# gender = input("Enter your  gender (m/f: ")
# hemoglobin = int(input("Enter the hemoglobin:"))
# if gender == "f":
#     if hemoglobin < 155 or hemoglobin > 117:
#         print("hemoglobin is normal")
# elif gender == "m":
#     if hemoglobin < 167 or hemoglobin > 134:
#         print("hemoglobin is normal")
# else:
#     print("hemoglobin not recognized.")
#
# #Exercise 4
# year = int(input("Enter the year:"))
# if year % 4 == 0 and year % 100 == 0 or year % 400 == 0:
#     print("leap year")
# else:
#     print("not leap year")
#
# money = int(input("Enter your money:"))
# if money < 5:
#     print("Sorry, you cannot buy more than 5 dollars")
# else:
#     print("Your money is enough to buy more than 5 dollars")
#
#
#
#
#
# week 3...
# while (condition):
#     block to be repeat
# rounds =int(input("enter number of rounds :"))
# finished_round = 0
# while (finished_round < rounds):
#     print("good morning")
#     finished_round = finished_round + 1
#
#
# rounds = int(input("enter  number round of rounds: :"))
# finished_round = 0
# while (finished_round < rounds):
#     print("good night")
#     finished_round = finished_round + 1
#
# times = int(input("enter number of times you want it to be printed: ")
# finished(times) = 0
# while finished < times:
#     print("I love you")
#
#
#
# command = input ("enter command: ")
# while command != "stop":
#     print("executing command: " + command)
#     command = input ("enter command: ")
#     print("execution stopped")
#
#
# command = input("enter password")
# while command != "python 1,2,3":
#     print("enter password")
#     command = input("enter password")
# print ("correct")
#
# import random
# dice1 = dice2 = rolls = 0
# while dice1!=6 or dice2!=6:
#     dice1 = random.randint(1,6)
#     dice2 = random.randint(1,6)
#     rolls = rolls + 1
# print(f"Rolled {rolls:d} times.")
#
#
#
#
# correct_password = "python123"
# password = ""
# while password != correct_password:
#     password = input("Enter your password: ")
#     print("Password is correct")
#
# first = 1
# while first < 5:
#     second = 1
#     while second < 5:
#         print(f"{first} x {second} = {first * second:d}")
#         second = second + 1
#         first = first + 1
# first = 1
# while first < 10:
#     second = 1
#     while second < 10:
#         print(f"{first}*{second} = {first * second}")
#         second = second + 1
#         first = first + 1
#
#
# import random
# rounds = 0
# total_rolls = 0
#
# while rounds < 100000:
#     dice1 = dice2 = rolls = 0
#     while (dice1!=6 or dice2!=6):
#         dice1 = random.randint(1,6)
#         dice2 = random.randint(1,6)
#         rolls = rolls + 1
#     rounds = rounds + 1
#     total_rolls = total_rolls + rolls
# average_rolls = total_rolls/rounds
# print(f"Average rolls required: {average_rolls:6.2f}")
#
#
# command = input("Enter command:")
# while command != "stop":
#     if command =="mayday":
#         break
#     print("Executing command:" + command)
#     command = input("Enter command:")
# else:
#     print("good bye.")
# print("Execution stopped.")

number = int(input("Enter a number: "))
while number <= 1000:
    if number % 3 == 0:
        print(number)
        number += 1
        break
    else:
        print("number is wrong")
        break


