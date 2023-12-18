# Define a list
a_list = [10, 25.2, "Hey"]

# Access the list elements
print("a_list[0]: ", a_list[0])
print("a_list[1]: ", a_list[1])
print("a_list[2]: ", a_list[2])

# Iterate over a list
for item in a_list:
    print(item)

# Add a boolean item to the end of the list
a_list.append(True)
print(a_list)

# Print the length of the list
print("List length:", len(a_list))

# Create a list of lists
list_of_lists = [
    [1, 2, 3],
    ["1", "2", "3"],
    [True, False, True]
]
print(list_of_lists)

# Access the second item in the second list
print(list_of_lists[1][1])

# Clear a list
a_list.clear()
print("a_list after clear: ", a_list)
