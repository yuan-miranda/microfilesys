def replace_text_in_line(file_path, line_index, start_index, end_index, new_text):
    # prevent user from having "start_index" higher than "end_index"
    if start_index > end_index:
        print("start index cant be higher than end index")

    with open(file_path, 'r+') as file:
        # store the file content line by line on a list
        lines = file.readlines()

        # set the cursor on the beginning of the file
        file.seek(0)

        # throw an error if "line_index" is less than 1 or higher
        # than the file line length
        if line_index < 1 or line_index > len(lines):
            print(f"Invalid line number: {line_index}")
            return
        
        # store specified line content to "line_to_modify"
        line_to_modify = lines[line_index - 1]

        # replace the substring on "line_to_modify" using slicing to "new_text"
        modified_line = line_to_modify.replace(line_to_modify[start_index:end_index], new_text)        
        
        # save the "modified_line" to lines[line_index - 1]
        lines[line_index - 1] = modified_line
        
        # save the changes to the file
        file.writelines(lines)

# Example usage
file_path = 'ee.txt'
line_index = 20
start_index = 13
end_index = 27
new_text = 'absolutely stunning'

replace_text_in_line(file_path, line_index, start_index, end_index, new_text)
