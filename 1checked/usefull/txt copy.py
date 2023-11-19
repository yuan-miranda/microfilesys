def replace_line(file_path, line_number, new_text):
    # Read the contents of the file into a list of lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    while line_number > len(lines):
        lines.append('\n')
    
    # update the line with the new content
    lines[line_number - 1] = new_text + '\n'

    # write the modified line
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Example usage
file_path = 'foo'
line_number = 25
new_text = 'This is the new content for line 25'
replace_line(file_path, line_number, new_text)

# Example usage with a higher line number
new_line_number = 100
new_text = 'This is the new content for line 30'
replace_line(file_path, new_line_number, new_text)
