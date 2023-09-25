# Function to generate a string of desired length
def generate_string(length):
    mylist = ['a']  # Initialize an empty list to store characters

    # Iterate through the desired length
    for i in range(length - 1):
        j = i % 10 + 1  # Calculate the next character index (1 to 10)

        # Append a character based on the index
        if j == 10:
            mylist.append(chr(97 + (i//9)))  # Append a letter when index is 10
        else:
            mylist.append(str(j))  # Append the index as a string

    return ''.join(mylist)  # Join the characters to form the resulting string

# Desired length of the string
# making 0 is still one, refer to 4.py
desired_length = 1

# Generate the resulting string
resulting_string = generate_string(desired_length)

# Print the resulting string and its length
print(resulting_string)
print(len(resulting_string))




# NOT WORKING