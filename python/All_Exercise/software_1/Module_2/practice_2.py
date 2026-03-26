#Exersice 1
name = input("what is your name? ")
print("hello, " + name )

#Exersice2
radius = float(input("enter the radius of the circle: "))
area = 3.14159 * radius ** 2
print("the area of the circle is " + str(area))

#Exersice 3
length = float(input("enter the length of the rectangle: "))
width = float(input("enter the width of the rectangle: "))
area = length * width
print("the area of the rectangle is " + str(area))

#Exersice 4
num1 = int(input("enter the first number: "))
num2 = int(input("enter the second number: "))
num3 = int(input("enter the third number: "))
sum = num1 + num2 + num3
product = num1 * num2 * num3
average = sum / 3
print("the sum of the three numbers is " + str(sum))
print("the product of the three numbers is " + str(product))
print("the average of the three numbers is " + str(average))

#Exersice 5
talents = int(input("enter the number of talents: "))
pounds = int(input("enter the number of pounds: "))
lots = float(input("enter the number of lots: "))
#convert every thing to lots
total = talents * 20 *32 + pounds * 32 + lots
#convert lots to grams
total_lots = talents * 20 * 32 + pounds * 32 + lots
grams = total_lots * 13.3
#convert grams to kilograms and grams
kilograms = int(grams // 1000)
remaining_grams = grams % 1000
print(f"the weight is {kilograms} kilograms and {grams : .2f} grams.")

#Exercise 6
import random
digit_three_1 = random.randint(0,9)
digit_three_2 = random.randint(0,9)
digit_three_3 = random.randint(0,9)
digit_four_1 = random.randint(0,6)
digit_four_2 = random.randint(0,6)
digit_four_3 = random.randint(0,6)
digit_four_4 = random.randint(0,6)
print(f"3_digit code:\n {digit_three_1}{digit_three_2}{digit_three_3}")
print(f"4_digit code:\n {digit_four_1}{digit_four_2}{digit_four_3}{digit_four_4}")
