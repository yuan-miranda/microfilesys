def append_to_line(filename, line_number, text_to_append):
    # Read the file and split it into lines
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Check if the specified line number is valid
    if line_number < 1 or line_number > len(lines):
        print("Invalid line number")
        return

    # Append text to the end of the specified line
    lines[line_number - 1] = lines[line_number - 1].rstrip('\n') + text_to_append + '\n'

    # Write the modified lines back to the file
    with open(filename, 'w') as file:
        file.writelines(lines)

# Example usage
filename = 'todo'
line_number = 2  # Line number to append to (1-based index)
text_to_append = ' Appended text'

append_to_line(filename, line_number, text_to_append)


def writeend(file, line_number, text_to_append):
        # Read the file and split it into lines
        with open(file, 'r') as f:
            lines = f.readlines()

        # Check if the specified line number is valid
        if line_number < 1 or line_number > len(lines):
            print("Invalid line number")
            return

        # Append text to the end of the specified line
        lines[line_number - 1] = lines[line_number - 1].rstrip('\n') + ' ' + text_to_append + '\n'

        # Write the modified lines back to the file
        with open(file, 'w') as file:
            file.writelines(lines)