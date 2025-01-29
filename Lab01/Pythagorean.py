#Pythagorean Theorem

answer = input("What is the length of  side 1? ")
side1 = int(answer)

answer2 = input("\nWhat is the length of side 2? ")
side2 = int(answer2)

import math 

hypotenuse = math.sqrt((side1**2) + (side2**2))
rounded = round(hypotenuse, 2)
print("The hypotenuse of your triangle is " + str(rounded))