def write_to_specific_line(file_path, line_number, new_content):
    # Read the existing content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Modify the desired line
    if 1 <= line_number <= len(lines):
        lines[line_number - 1] = new_content + '\n'  # Adjusting for 0-based indexing

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)
    else:
        print(f"Line number {line_number} is out of range.")

# Example usage
file_path = 'foo'
line_number_to_modify = 3
new_content_for_line = 'This is the new content for line 3'
write_to_specific_line(file_path, line_number_to_modify, new_content_for_line)
