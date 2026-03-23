# 1..Write a function that returns a random dice roll between 1 and 6. The function should not have any parameters.
# Write a main program that rolls the dice until the result is 6. The main program should print out the result of
# each roll.

import random

def roll_dice():
    return random.randint(1, 6)

def main():
    result = 0
    while result != 6:
        result = roll_dice()
        print("Roll:", result)

main()


#2.. Modify the function above so that it gets the number of sides on the dice as a parameter. With the modified function you can for
#     example roll a 21-sided role-playing dice. The difference to the last exercise is that the dice rolling in the main program continues
#     until the program gets the maximum number on the dice, which is asked from the user at the beginning.
#


def roll_dice(x):
    return random.randint(1, x)

num1 = int(input("Enter the number of sides: "))
while True:

    result = roll_dice(num1)
    print("Roll:", result)

    if result == num1:
        break

#3.. Write a function that gets the quantity of gasoline in American gallons and returns the number converted to litres.
# Write a main program that asks for a volume in gallons from the user and converts the value to liters. The conversion
# must be done by using the function.Conversions continue until the user inputs a negative value.


def conversion(x):
    liters = x * 3.785
    return liters

while True:
    gallon = int(input("Enter the amount of gallons: "))
    if gallon < 0 :
        break

    converted = conversion(gallon)
    print(converted)

# 4...Write a function that gets a list of integers as a parameter. The function returns the sum of all the numbers in the list.
# For testing, write a main program where you create a list, call the function, and print out the value it returned.

def sum_list(lst1):
    sum = 0
    for i in lst1:
        sum += i
    return sum

lst1 =[1,4,12,5,16,8]
result = sum_list(lst1)
print(result)


#5... Write a function that gets a list of integers as a parameter. The function returns a second list that is otherwise the same
# as the original list except that all uneven numbers have been removed. For testing, write a main program where you create a list,
# call the function, and then print out both the original as well as the cut-down list.

def next_list(lst1):
    new_lst = []
    for i in lst1:
        if i % 2 == 0:
            new_lst.append(i)
    return new_lst


lst1 = [1,5,8,9,11,78,45,22,336,55]
result = next_list(lst1)
print(lst1)
print(result)


#6... Write a function that receives two parameters: the diameter of a round pizza in centimeters and the price of the pizza in euros.
# The function calculates and returns the unit price of the pizza per square meter. The main program asks the user to enter the
# diameter and price of two pizzas and tells the user which pizza provides better value for money (which of them has a lower unit price).
# You must use the function you wrote for calculating the unit prices.


import math
def unit_price(diameter,price):
    radius = diameter / 2
    radius_m = radius / 100
    area = math.pi  * radius_m ** 2
    return price / area


dia1 = float(input("enter diameter of pizza 1 : "))
pr1 = float(input("enter price of pizza 1 : "))
dia2 = float(input("enter diameter of pizza 2 : "))
pr2 = float(input("enter price of pizza 2 : "))

price1 = unit_price(dia1,pr1)
price2 = unit_price(dia2,pr2)
print("Pizza 1 price : " ,price1)
print("Pizza 2 price : " ,price2)

if price1 < price2:
    print("Pizza 1 price is provides better value for money ")
else:
    print("Pizza 2 price is provides better value for money ")
