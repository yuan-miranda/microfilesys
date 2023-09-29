def is_letter(input):
    return True if input in 'abcdefghijklmnopqrstuvwxyz' else False

# Prompt the user for a character input
def to_ascii():
    user_input = input("Enter a character: ")

    # Ensure the input is a single character
    if len(user_input) != 1:
        print("Please enter only a single character.")

    # Ensure the input is an alphabet
    elif not is_letter(user_input):
        print("Please enter only characters in a-z")

    else:
        # Convert the character to its ASCII equivalent
        ascii_value = ord(user_input)
        print("ASCII value of", user_input, "is", ascii_value)


to_ascii()