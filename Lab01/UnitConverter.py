userinput = input("What measurement (distance or weight) would you like to convert? ")

i = 0
letters = len(userinput)

while userinput[i] != " ":
    i += 1

value = float(userinput[0:i])
unit = str(userinput[i+1])

if unit == "C" or unit == "c":
    measurement = value / 2.54
    newunit = "inches"
elif unit == "I" or unit == "i":
    measurement = value * 2.54
    newunit = "centimeters"
elif unit == "Y" or unit == "y":
    measurement = value * 0.9144
    newunit = "meters"
elif unit == "M" or unit == "m":
    measurement = value / 0.9144
    newunit = "yards"
elif unit == "O" or unit == "o":
    measurement = value * 28.3495
    newunit = "grams"
elif unit == "G" or unit == "g":
    measurement = value / 28.3495
    newunit = "ounces"
elif unit == "L" or unit == "l" or unit == "P" or unit == "p":
    measurement = value * 0.453592
    newunit = "kilograms"
elif unit == "K" or unit == "k":
    measurement = value / 0.453592
    newunit = "pounds"

print("\n\nThe conversion of ", userinput, " is ", measurement, " ", newunit, ".")