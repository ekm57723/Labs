radius = input("What would you like the radius of your circle to be? ")

radii = float(radius)

if radii > 0:
    print("\nThank you for your input.\n")
else: 
    radius2 = input("\nPlease enter a valid value for the radius of your circle: ")

import math

circumference = math.pi * radii * 2
area = math.pi * radii**2
circumference1 = round(circumference, 2)
area1 = round(area, 2)

print("The circumference of your circle with radius ", radii, " is ", circumference1, ", and the area of your circle is ", area1, ".")