version = "v.0.3.4"
updated = "12/08/23"

import os

# file mode
FE_MODE = "file_editor_mode"
FM_MODE = "file_manager_mode"

current_open_file = None

# commands
file_editor_command = ['read', 'write', 'clear', 'remove']
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
list_aliases = ['ls', 'list']

# boolean functions section
def is_file(file_name):
    """
    Check if the file exist on the current working directory.
    """
    return file_name in os.listdir()

def is_line_number_in_range(line_number):
    """
    Check if the line given is in the range of the lines of the file.
    """
    total_lines = get_file_length(current_open_file)
    return line_number >= 1 and line_number <= total_lines

# getter functions section
def get_file_content(file_name):
    """
    Return a list of contents of the file.
    """
    with open(file_name, 'r') as file:
        file_lines = file.readlines()

    # adds a newline character when reading on a blank file.
    if not file_lines:
        file_lines.append('\n')

    return file_lines

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
        line_number = input_parts[2]
        line_number = int(line_number)

    except IndexError:
        print(f"Expected an line number after {option}, i.e. '{command} {option} 1'")
        return None

    except ValueError:
        print(f"'{line_number}' is not a number.")
        return None
    
    if line_number < 1:
        print("Line number cannot be zero or negative.")
        return None

    return line_number

def get_line_number_in_range(raw_input):
    """
    Return the line if its within the file lines length.
    """
    line_number = get_line_number(raw_input)

    if not line_number:
        return None
    
    if not is_line_number_in_range(line_number):
        print(f"Line number must be in range of 1 to {get_file_length(current_open_file)}.")
        return None
    
    return line_number

def get_content(raw_input):
    """
    Return the content if it exist, is enclosed with a pair of double quotes, else None.
    """
    input_parts = raw_input.split()
    command = input_parts[0]
    option = input_parts[1]
    line_number = input_parts[2]

    try:
        # split the input into 4 elements being the 4th element is the content.
        content = raw_input.split(None, 3)[3]

    except IndexError:
        print(f"Expected an content after '{command}', i.e. '{command} {option} {line_number} \"content\"'")
        return None

    if not content.startswith('"') or not content.endswith('"') or content.count('"') != 2:
        print("Content string should be enclosed with a pair of double quotes.")
        return None

    # remove the double quotes.
    return content[1:-1]

def microfilesys_writelines(file_lines):
    """
    Rewrites the whole file with the specified list.
    """
    with open(current_open_file, 'w') as file:
        for line_content in file_lines:
            file.write(line_content)

def microfilesys_rjust(string, width, fill_char=' '):
    """
    Return a right-justified string.
    """
    if len(string) > width:
        return string
    
    else:
        padding = fill_char * (width - len(string))
        return padding + string

# command's source code section
def create_file(file_name):
    with open(file_name, 'w') as file:
        print(f"'{file_name}' created successfully.")

def delete_file(file_name):
    os.remove(file_name)
    print(f"'{file_name}' deleted successfully.")

def read_line(line_number):
    file_lines = get_file_content(current_open_file)
    line_content = file_lines[line_number - 1].rstrip('\n')

    # generate a right-justified line number.
    line_number = microfilesys_rjust(str(line_number), 4)

    print(f"{line_number}| {line_content}")

def read_all():
    file_length = get_file_length(current_open_file)
 
    # read() include the newline buffer at the end so use this instead.
    # this shit is very slow lmao try it with 9999+ lines
    for line in range(1, file_length + 1):
        read_line(line)

def write_line(line_number, content):
    file_lines = get_file_content(current_open_file)

    # load new lines when writing beyond the current range of lines in the file.
    while len(file_lines) < line_number:
        file_lines.append('\n')

    file_lines[line_number - 1] = content + '\n'

    microfilesys_writelines(file_lines)

def write_end(line_number, content):
    file_lines = get_file_content(current_open_file)

    # replace the newline character with the content and re-append the newline character after.
    file_lines[line_number - 1] = file_lines[line_number - 1].rstrip('\n') + content + '\n'

    microfilesys_writelines(file_lines)

def clear_line(line_number):
    file_lines = get_file_content(current_open_file)
    file_lines[line_number - 1] = '\n'

    microfilesys_writelines(file_lines)

def clear_all():
    file_lines = get_file_content(current_open_file)

    # replace each line with a newline character while keeping the original line length (makes it blank line).
    file_lines = ['\n'] * len(file_lines)

    microfilesys_writelines(file_lines)

def remove_line(line_number):
    file_lines = get_file_content(current_open_file)
    file_lines.pop(line_number - 1)

    microfilesys_writelines(file_lines)

def remove_all():
    with open(current_open_file, 'w') as file:
        file.write('')

# command input validator section
def process_read_command(raw_input):
    """
    validate incomming inputs for the read command.
    """
    process_common_command("read", raw_input)

def process_write_command(raw_input):
    """
    validate incomming inputs for the write command.
    """
    input_parts = raw_input.split()
    command = input_parts[0]
    option = input_parts[1]
    line_number = get_line_number(raw_input)

    if not line_number:
        return None

    content = get_content(raw_input)

    if not content:
        return None

    if option in line_option_aliases:
        write_line(line_number, content)

    elif option in end_option_aliases:
        line_number = get_line_number_in_range(raw_input)
        if not line_number:
            return None

        write_end(line_number, content)

    else:
        print(f"Invalid option '{option}' for '{command}' command.")

def process_clear_command(raw_input):
    """
    Validate incomming inputs for the clear command.
    """
    process_common_command("clear", raw_input)

def process_remove_command(raw_input):
    """
    Validate incomming inputs for the remove command.
    """
    process_common_command("remove", raw_input)

def process_common_command(command, raw_input):
    """
    A generic function to handle read, clear, and remove command.
    """
    common_command_handler = {
        "read": {
            "line": lambda: read_line(get_line_number_in_range(raw_input)),
            "all": lambda: read_all()
        },
        "clear": {
            "line": lambda: clear_line(get_line_number_in_range(raw_input)),
            "all": lambda: clear_all()
        },
        "remove": {
            "line": lambda: remove_line(get_line_number_in_range(raw_input)),
            "all": lambda: remove_all()
        }
    }

    input_parts = raw_input.split()
    option = input_parts[1]

    if option in line_option_aliases:
        line_number = get_line_number_in_range(raw_input)

        if not line_number:
            return None

        if len(input_parts) != 3:
            print(f"Expected '{command} {option} {line_number}'")
            return None

        common_command_handler[command]["line"]()

    elif option in all_option_aliases:
        if len(input_parts) != 2:
            print(f"Expected '{command} {option}'")

        common_command_handler[command]["all"]()

    else:
        print(f"Invalid option '{option}' for '{command}' command.")

def display_help():
    print(
f"""Syntax:
    create <file>                                   Create a file in the current directory.
    open <file>                                     Open a file (used to access file editor mode).
    delete <file>                                   Delete a file in the current directory.

    read <-l line=int | -a>                         Read the content from the file.
    write <-l | -e> <line=int content="string">     Write content to the file.
    clear <-l line=int | -a>                        Clear the content of from the file but keep the lines.
    remove <-l line=int | -a>                       Remove line of the file.

    q quit exit                                     exit the program or go back to FM mode when in FE mode.
    h help man manual                               prints out the help page.
    ls list                                         list current directory and files.

Options:
    -l --line l line                                Specify the line of the file (available: read, write, clear).
    -a --all a all                                  Select all the content of the file (available: read, clear).
    -e --end e end                                  Move the content to the end of the line (available: write).

Argument:
    line=int                                        Specify the line number to work on, i.e. 1, 10, 69.
    content="string"                                Specify a string to be written to the file. Content should be enclosed in double quotes, i.e. "example string".

Example:
    write --line 1 "hello, world!"                  Write "hello, world!" at the first line of the file.
    read -l 10                                      Read the content of line 10 of the file.
    delete example.txt                              Delete the file named "example.txt".

Version:
    microfilesys.py {version} {updated}""")

def display_file_list():
    print(os.getcwd())
    for files in os.listdir():
        print(f"|-- {files}")

def start():
    """
    Starting point of the program, handles the basic input validation.
    """
    current_file_mode = FM_MODE
    current_file = None
    global current_open_file

    print(f"microfilesys.py {version} {updated}\nEnter 'help' for help and 'quit' to quit.\n")

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

        if raw_input.strip() in list_aliases:
            display_file_list()
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
                current_open_file = current_file
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
                process_read_command(raw_input)

            elif command == "write":
                process_write_command(raw_input)

            elif command == "clear":
                process_clear_command(raw_input)

            elif command == "remove":
                process_remove_command(raw_input)

start()