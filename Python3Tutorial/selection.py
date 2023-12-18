# Define a variable for the ambient temperature
temperature = 12

# Simple if statement
if temperature < 32:
    print("It is cold outside")

# if..else statement
temperature = 75
if temperature < 32:
    print("It is cold outside")
else:
    print("It is not too cold today")

# if..elif..else statement
temperature = 90
if temperature < 32:
    print("It is cold outside")
elif 32 <= temperature <= 80:
    print("It is a pleasant day today")
else:
    print("It is a hot day today")
