def writeline(file, index, content):
    with open(file, 'r+') as file:
        lines = file.readlines()
        index = int(index)
                
        # check if input line is in range of file lines
        if index > 0 and index <= len(lines):

            # write at the end of the line using this
            lines[index - 1] = lines[index - 1].rstrip('\n') + content + '\n'
            file.seek(0)
            file.writelines(lines)

        else:
            print(f"line must be in range of 1 to {len(lines)}")

user_input = 'write -l 1 "hello world"'
user_input_split = user_input.split()

print(user_input_split)