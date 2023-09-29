current_col_letters = []

def is_column(column):
    if len(column) != 2:
        print("not 2")
        return False
    
    elif column[0].isalpha() and column[1] in '123456789':
        print(f"{column} is valid")
        return True
    else:
        print(f"{column} is not valid")
        return False

def is_multi_column(column):
    if len(column) != 5:
        print("not 5")
        return False
    
    elif is_column(column[:2]) and is_column(column[3:]):
        print(f"{column} multi-column")
        return True
    else:
        print(f"{column} not multi-column")
        return False

def is_letter(input):
    return True if input in 'abcdefghijklmnopqrstuvwxyz' else False

# Prompt the user for a character input
def to_ascii():
    user_input = input("Enter a character: ")

    # Ensure the input is an alphabet
    if not is_letter(user_input):
        print("Please enter only characters in a-z")

    else:
        # Convert the character to its ASCII equivalent
        ascii_value = ord(user_input)
        print("ASCII value of", user_input, "is", ascii_value)


is_multi_column("a9:a2")


# generate a radix-like string of aplhabet and numbers

def get_column_letters():
    pass

def generate_string(length):
    if length < 0 or length > 250:
        print(f"{length} is not invalid, Length should be between 1 and 250")

    alpha_numeric_list = [] # store the generated alphanumerical characters
    alphabetical_list= [] # store the generated alphabets separately

    for i in range(length + 1):
        # formula to ensure alphabets are placed at 0, 10, 20, ... positions
        j = i % 10

        if j == 0:
            # append the alphabet to both lists at specific positions
            alpha_numeric_list.append(chr(97 + (i//10)))
            alphabetical_list.append(chr(97 + (i//10)))
        
        # append numbers to the list when 'i' isn't divisible by 10
        else:
            alpha_numeric_list.append(str(j))

    return ''.join(alpha_numeric_list), ''.join(alphabetical_list)

while True:
    try:
        desired_length = int(input("Enter length: "))
    except ValueError:
        print("hasto be number try again")
        continue

    alphanumber, alphabet = generate_string(desired_length)

    print(f"[1]radix-like number: {alphanumber}")
    print(f"[2]radix-like number length: {len(alphanumber) - 1}")
    print(f"[3]radix-like letter: {alphabet}")
    print(f"[4]radix-like letter length: {len(alphabet)}")
