def get_content_test(input_string):
    result = []
    current_word = ''
    inside_quotes = False

    for char in input_string:
        if char == ' ' and not inside_quotes:
            # Split at space only if not inside quotes
            result.append(current_word)
            current_word = ''
        elif char == '"':
            # Toggle the inside_quotes flag when a double quote is encountered
            inside_quotes = not inside_quotes
        else:
            current_word += char

    # Add the last word after the loop
    result.append(current_word)

    return result

# Your input string
input_string = 'write -l 1 "hello world              1"'

# Split the string using the custom_split function
result = get_content_test(input_string)[3]
print(len(result))
print(result)
