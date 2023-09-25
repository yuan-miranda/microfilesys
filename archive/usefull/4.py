# generate a radix-like string of aplhabet and numbers

def generate_string(length):
    if length < 0 or length > 250:
        return f"{length} is not invalid, Length should be between 1 and 250"

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
