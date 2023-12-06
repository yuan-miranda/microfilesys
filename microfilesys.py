# Microfilesys.py v.0.3.3 (complete re-work)
# last update: 12/06/23

import os

# file mode
FE_MODE = "file_editor_mode"
FM_MODE = "file_manager_mode"

# commands
file_editor_command = ['read', 'write', 'clear']
file_manager_command = ['create', 'open', 'delete']
valid_commands = file_editor_command + file_manager_command

# option aliases
line_option_aliases = ['-l', '--line', 'l', 'line']
all_option_aliases = ['-a', '--all', 'a', 'all']
end_option_aliases = ['-e', '--end', 'e', 'end']
valid_options = line_option_aliases + all_option_aliases + end_option_aliases

# help and quit commands? idk maybe keywords
quit_aliases = ['q', 'quit', 'exit']
help_aliases = ['h', 'help', 'man', 'manual']

# boolean functions section
def is_file(file_name):
    """
    Check if the file exist on the current working directory.
    """
    return file_name in os.listdir()

def is_line_number_in_range(line, file_name):
    """
    Check if the line given is in the range of the lines of the file.
    """
    total_lines = get_file_length(file_name)
    return line >= 1 and line <= total_lines

# getter functions section
def get_file_content(file_name):
    """
    Return a list of contents of the file.
    """
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # reading on a blank file returns an empty list because it doesnt have newline(\n) characterat the end
    # of the line. read() do return a list but it reads the whole file and store it on a single string.
    if not lines:
        lines.append('\n')

    return lines

def get_file_length(file_name):
    """
    Return the line length of the file.
    """
    return len(get_file_content(file_name))

def get_line_number(raw_input):
    """
    Return line if the line given exist, is a number, and non-negative, else None.
    """
    try:
        input_parts = raw_input.split()
        command = input_parts[0]
        option = input_parts[1]
        line = input_parts[2]
        line = int(line)

    except IndexError:
        print(f"Expected an line number after {option}, i.e. '{command} {option} 1'")
        return None

    except ValueError:
        print(f"'{line}' is not a number.")
        return None
    
    if line < 1:
        print("Line number cannot be zero or negative.")
        return None

    return line

def get_line_number_in_range(raw_input, file_name):
    """
    Return the line if its within the file lines length.
    """
    line_number = get_line_number(raw_input)

    if not line_number:
        return None
    
    if not is_line_number_in_range(line_number, file_name):
        print(f"Line number must be in range of 1 to {get_file_length(file_name)}.")
        return None
    
    return line_number

def get_content(raw_input):
    """
    Return the content if it exist, is enclosed with a pair of double quotes, else None.
    """
    input_parts = raw_input.split()
    command = input_parts[0]
    option = input_parts[1]
    line = input_parts[2]

    try:
        content = raw_input.split(None, 3)[3]

    except IndexError:
        print(f"Expected an content after '{command}', i.e. '{command} {option} {line} \"content\"'")
        return None
    
    if not content.startswith('"') or not content.endswith('"') or content.count('"') != 2:
        print("Content string should be enclosed with a pair of double quotes.")
        return None
    
    return content[1:-1]

# command's source code section
def create_file(file_name):
    with open(file_name, 'w') as file:
        print(f"'{file_name}' created successfully.")

def open_file(file_name):
     # Return the name of the opened file
    return file_name

def delete_file(file_name):
    os.remove(file_name)
    print(f"'{file_name}' deleted successfully.")

def read_line(line, file_name):
    lines = get_file_content(file_name)
    line_content = lines[int(line) - 1].rstrip('\n')

    print(line_content)

def read_all(file_name):
    with open(file_name, 'r') as file:
        print(file.read())

def write_line(line, content, file_name):
    lines = get_file_content(file_name)

    while line > len(lines):
        lines.append('\n')

    lines[line - 1] = content + '\n'

    with open(file_name, 'w') as file:
        for line_content in lines:
            file.write(line_content)

def write_end(line, content, file_name):
    lines = get_file_content(file_name)
    lines[line - 1] = lines[line - 1].rstrip('\n') + content + '\n'
    
    with open(file_name, 'w') as file:
        for line_content in lines:
            file.write(line_content)

def clear_line(line, file_name):
    lines = get_file_content(file_name)
    lines[line - 1] = '\n'

    with open(file_name, 'w') as file:
        for line_content in lines:
            file.write(line_content)

def clear_all(file_name):
    with open(file_name, 'w') as file:
        file.write('')

# command input validator section
def process_read_command(raw_input, file_name):
    """
    validate incomming inputs for the read command.
    """
    input_parts = raw_input.split()
    option = input_parts[1]

    if option in line_option_aliases:
        line = get_line_number_in_range(raw_input, file_name)
        
        if not line:
            return None
        
        # prevent something like 'read --line 1 extra_argument blah blah'
        if len(input_parts) != 3:
            print(f"Expected 'read {option} {line}'")
            return None
        
        read_line(line, file_name)

    elif option in all_option_aliases:
        if len(input_parts) != 2:
            print(f"Expected 'read {option}'")
            return None
        
        read_all(file_name)
        
    else:
        print(f"'read' command doesnt have a '{option}' option.")

def process_write_command(raw_input, file_name):
    """
    validate incomming inputs for the write command.
    """
    input_parts = raw_input.split()
    option = input_parts[1]
    line = get_line_number(raw_input)
    
    if not line:
        return None
    
    content = get_content(raw_input)

    if not content:
        return None
    
    if option in line_option_aliases:
        write_line(line, content, file_name)
        
    elif option in end_option_aliases:
        line = get_line_number_in_range(raw_input, file_name)
        if not line:
            return None
        
        write_end(line, content, file_name)

    else:
        print(f"'write' command doesnt have a '{option}' option.")

def process_clear_command(raw_input, file_name):
    """
    validate incomming inputs for the clear command.
    """
    input_parts = raw_input.split()
    option = input_parts[1]
    
    if option in line_option_aliases:
        line = get_line_number_in_range(raw_input, file_name)
        if not line:
            return None
        
        if len(input_parts) != 3:
            print(f"Expected 'clear {option} {line}'")
            return None
        
        clear_line(line, file_name)

    elif option in all_option_aliases:
        if len(input_parts) != 2:
            print(f"Expected 'clear {option}'")

        clear_all(file_name)

    else:
        print(f"'clear' command doesnt have '{option}' option.")

def display_help():
    print(
"""Syntax:
    [file manager commands]
    create <file>                                   Create a file in the current directory.
    open <file>                                     Open a file (used to access file editor mode).
    delete <file>                                   Delete a file in the current directory.

    [file editor commands]
    read <-l line=int | -a>                         Read the content from the file.
    write <-l | -e> <line=int content="string">     Write content to the file.
    clear <-l line=int | -a>                        Clear the content from the file.

Options:
    -l --line l line                                Specify the line of the file (available: read, write, clear).
    -a --all a all                                  Select all the content of the file (available: read, clear).
    -e --end e end                                  Move the content to the end of the line (available: write).

Argument:
    line=int                                        Specify the line number to work on, e.g., 1, 10, 69.
    content="string"                                Specify a string to be written to the file. Content should be enclosed in double quotes, e.g., "example string".

Example:
    write --line 1 "hello, world!"                  Write "hello, world!" at the first line of the file.
    read -l 10                                      Read the content of line 10 of the file.
    delete example.txt                              Delete the file named "example.txt".

More Info:
    1. There's no current way to have multiple flags at the same time, kind of complicated without the argparse library.
    2. Commands aren't flexible and have predefined argument positions.
    3. Non-flag-like option formats are added because this program was initially intended for mobile (to type faster).
    4. There's an extra line in the file that isn't included in the file reading because it is used to accurately read the file ironically. The last line couldn't be read
    if it's empty (doesn't have '\\n' on that line), so line + 1 works. It was also mentioned in the get_file_content() function.""")

def start():
    """
    starting point of the program, handles the basic input validation.
    """
    current_file_mode = FM_MODE
    current_open_file = None
    current_file = None

    print("Microfilesys.py v.0.3.3 (complete re-work)\nEnter 'help' for help and 'quit' to quit.\n")

    while True:
        try:
            raw_input = input(f"microfilesys-{current_open_file}[1/{get_file_length(current_open_file)}]: " if current_open_file else "microfilesys: ")
            input_parts = raw_input.split()

        except KeyboardInterrupt:
            # if the current file mode is file manager when exiting, exit the program.
            if current_file_mode == FM_MODE:
                return
            
            # but when its on file manager, just go back to the file editor mode.
            else:
                print()
                current_open_file = None
                current_file_mode = FM_MODE
                continue
    
        
        if not input_parts:
            continue
        
        # same operation from the KeyboardInterrupt exception.
        if raw_input.strip() in quit_aliases:
            if current_file_mode == FM_MODE:
                return
            
            else:
                current_open_file = None
                current_file_mode = FM_MODE
                continue
        
        if raw_input.strip() in help_aliases:
            display_help()
            continue

        command = input_parts[0]
        
        if command not in valid_commands:
            print(f"'{raw_input}' is not recognized as a valid command.")
            continue

        if command in file_manager_command:
            if current_file_mode != FM_MODE:
                print("Status is currently in file editor, exit the mode by entering 'q' in the console.")
                continue
            
            if len(input_parts) != 2:
                print(f"Expected a file after '{command}' command, i.e. '{command} example.txt'")
                continue

            current_file = input_parts[1]

            # using 'create' command with a file that already exist
            if command == "create" and is_file(current_file):
                print(f"'{current_file}' already exists.")
                continue
            
            # using 'open' or 'delete' command with a file that doesnt exist
            if command in ['open', 'delete'] and not is_file(current_file):
                print(f"'{current_file}' doesn't exist to be used as a file parameter in '{command}' command.")
                continue

            if command == "create":
                create_file(current_file)
            
            elif command == "open":
                current_open_file = open_file(current_file)
                current_file_mode = FE_MODE
                
            elif command == "delete":
                delete_file(current_file)
        
        elif command in file_editor_command:
            if current_file_mode != FE_MODE:
                print("Status is currently in file manager, open a file by typing 'open <file>' in the console.")
                continue
            
            if len(input_parts) < 2:
                print(f"Expected an option after '{command}', i.e. '{command} --line ...'")
                continue

            option = input_parts[1]

            if option not in valid_options:
                print(f"'{option}' is not recognized as a valid option.")
                continue

            if command == "read":
                process_read_command(raw_input, current_open_file)
                
            elif command == "write":
                process_write_command(raw_input, current_open_file)

            elif command == "clear":
                process_clear_command(raw_input, current_open_file)

start()