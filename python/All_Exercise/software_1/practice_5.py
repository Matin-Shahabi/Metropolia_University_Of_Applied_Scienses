
#practice 1

# Write a program that asks the user how many dice to roll. The program rolls all the dice once and prints
# out the sum of the numbers. Use a for loop.

import random
dice_count = random.randint(1,6)
print(dice_count)
total = random.randint(1,6)
print(total)
sum = total + dice_count
print(sum)

#practice 2


# Write a program that asks the user to enter numbers until they input an empty string to quit. At the end,
# the program prints out the five greatest numbers sorted in descending order. Hint: You can reverse the order of
# sorted list items by using the sort method with the reverse=True argument.


numbers = []

while True:
    user_input = input("Enter a number (press Enter to quit): ")
    if user_input == "":
        break
    numbers.append(float(user_input))

numbers.sort(reverse=True)

print("Five greatest numbers:")
for num in numbers[:5]:
    print(num)

#practice 3

# Write a program that asks the user for an integer and tells if the number is a prime number.
# Prime numbers are number that are only divisible by one or the number itself.
#
# For example, 13 is a prime number as it can only be divided by 1 or 13 so that the result is an integer.
# On the other hand, 21 is not a prime number as it is divisible by 3 and 7.


user_input = input("Enter a number(empty to quit): ")
if user_input == "number":
    print("number")
else:
    print("wrong input")


#practice 4

# Write a program that asks the user to enter the names of five cities one by on (use a for loop for reading the names)
# and stores them into a list structure. Finally, the program prints out the names of the cities one by one, one city
# per line, in the same order they were read as input. Use a for loop for asking the names and a for/in loop to iterate
# through the list.

cities= []
for i in range(5):
    name = input("Enter a city name: ")
    cities.append(name)
for city in cities:
    print(cities)

