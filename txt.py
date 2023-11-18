def replace_line(file_path, line_number, new_text):
    # Read the contents of the file into a list of lines
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            print('line 13')
            print(lines)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Check if the file is empty
    if not lines:
        print('line 14')
        print(lines)
        lines = ['\n'] * line_number  # Initialize empty lines with '\n'
        print('line 17')
        print(lines)
        lines[line_number - 1] = new_text + '\n'
        print('line 20')
        print(lines)
    else:
        # Make sure the line number is valid
        if 1 <= line_number <= len(lines):
            # Update the specific line with the new text
            lines[line_number - 1] = new_text + '\n'
            print('line 27')
            print(lines)
        else:
            print(f"Invalid line number: {line_number}")
            return

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
        print('line 36')
        print(lines)

# Example usage
file_path = 'foo'
line_number = 3
new_text = 'This is the new content for line 3'
replace_line(file_path, line_number, new_text)
