version = "v.0.3.8"
updated = "01/02/24"

import os
import re

# file operation modes
FILE_EDITOR_MODE = "file_editor_mode"
FILE_MANAGER_MODE = "file_manager_mode"

# command list
FILE_EDITOR_COMMAND = ["read", "write", "clear", "remove"]
FILE_MANAGER_COMMAND = ["create", "open", "delete"]
VALID_COMMANDS = FILE_EDITOR_COMMAND + FILE_MANAGER_COMMAND

# option aliases list
LINE_OPTION_ALIASES = ["-l", "--line", "l", "line"]
ALL_OPTION_ALIASES = ["-a", "--all", "a", "all"]
ALL_FAST_OPTION_ALIASES = ["-af", "--all-fast", "af", "all-fast"]
END_OPTION_ALIASES = ["-e", "--end", "e", "end"]
FILE_EDITOR_OPTION_ALIASES = LINE_OPTION_ALIASES + ALL_OPTION_ALIASES + ALL_FAST_OPTION_ALIASES + END_OPTION_ALIASES

FILE_OPTION_ALIASES = ["-f", "--file", "f", "file"]
DIR_OPTION_ALIASES = ["-d", "-dir", "--directory", "d", "dir", "directory"]
FILE_MANAGER_OPTION_ALISES = FILE_OPTION_ALIASES + DIR_OPTION_ALIASES

# are these considered a command or keywords?
QUIT_KEYWORD = ["q", "quit", "exit"]
HELP_KEYWORD = ["h", "help", "man", "manual"]
LIST_KEYWORD = ["ls", "list"]
VERSION_KEYWORD = ["v", "ver", "version"]
EXAMPLE_KEYWORD = ["ex", "example"]

current_open_path = None
current_file_mode = FILE_MANAGER_MODE

# boolean functions
def is_file(file_name, path=os.getcwd()):
    """
    Returns True if the file exists in the specified directory; otherwise, returns False.
    """
    return file_name in os.listdir(path) and not os.stat(f"{path}/{file_name}")[0] & 0x4000

def is_folder(folder_name, path=os.getcwd()):
    """
    Returns True if the folder exists in the specified directory; otherwise, returns False.
    """
    return folder_name in os.listdir(path) and os.stat(f"{path}/{folder_name}")[0] & 0x4000

def is_path_exists(path):
    """
    Returns True if the specified path exists; otherwise, returns False.
    """
    try:
        os.listdir(path)
        return True
    except OSError:
        return False

def is_valid_path_format(path):
    """
    Returns True if the specified path format is valid; otherwise, returns False.
    """
    directory_parts = path.split('/')[:-1]
    actual_directory_parts = [part for part in directory_parts if part != '']

    if len(actual_directory_parts) != path.count('/'):
        print(f"Invalid file path: {path}")
        return False
    
    if path.endswith('/'):
        print("File path must end with a file name.")
        return False
    
    if not bool(re.match("^[a-zA-Z0-9_./]*$", path)) and not path.startswith("C:"):
        print("Directory should only contain characters from 'a-z', 'A-Z', '0-9', '.', '_', and '/'.")
        return False
    
    return True

def is_line_number_in_range(line_number):
    """
    Returns True if the given line number is in the range of the lines of the file; otherwise, returns False.
    """
    total_lines = get_file_length(current_open_path)
    return 1 <= line_number <= total_lines

# getter functions
def get_ustyle_path(path):
    """
    Returns a string path that doesn't contain Windows-like path style.
    """
    return path.replace('\\', '/')

def get_valid_path(path):
    """
    Validates and returns a formatted path but doesn't ensure that the path exists.
    """
    # using the RPi Pico directory
    if path.startswith("/"):
        path = path[2:]

    if not is_valid_path_format(path):
        return None
    
    return handle_parent_dir(get_ustyle_path(path))

def get_file_content(file_name):
    """
    Returns a list of contents of the file.
    """
    with open(file_name, 'r') as file:
        file_lines = file.readlines()

    # adds a newline character when reading a blank file.
    if not file_lines:
        file_lines.append('\n')

    return file_lines

def get_file_length(file_name):
    """
    Returns the line length of the file.
    """
    return len(get_file_content(file_name))

def get_line_number(raw_input):
    """
    Returns the line if the given line exists, is a number, and non-negative; otherwise, returns None.
    """
    try:
        input_parts = raw_input.split()
        command = input_parts[0]
        option = input_parts[1]
        line_number = input_parts[2]
        line_number = int(line_number)

    except IndexError:
        print(f"Expected a line number after {option}, i.e., '{command} {option} 1'")
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
    Returns the line if it's within the file lines length; otherwise, returns None.
    """
    line_number = get_line_number(raw_input)

    if not line_number:
        return None
    
    if not is_line_number_in_range(line_number):
        print(f"Line number must be in the range of 1 to {get_file_length(current_open_path)}.")
        return None
    
    return line_number

def get_content(raw_input):
    """
    Returns the content if it exists. Content string enclosed with a pair of single or double quotes; otherwise, returns None.
    """
    input_parts = raw_input.split()
    command = input_parts[0]
    option = input_parts[1]
    line_number = input_parts[2]

    try:
        # split the input into 4 elements where the 4th element is the content.
        content = raw_input.split(None, 3)[3]

    except IndexError:
        print(f"Expected content after '{command}', i.e., '{command} {option} {line_number} \"content\"'")
        return None

    if len(content) == 1 or not (content.startswith('"') and content.endswith('"')) and not (content.startswith("'") and content.endswith("'")):
        print("Content string should be enclosed with a pair of single or double quotes.")
        return None

    # remove the double quotes.
    return content[1:-1]

# microfilesys functions
def microfilesys_removedirs(path):
    """
    Recursively removes the specified directory. Based on Roberthh's implementation: https://forum.micropython.org/viewtopic.php?t=7512#p42783.
    Note: Expects a formatted path and any parent directory operations to be done before running this function.
    """
    if os.stat(path)[0] & 0x4000:
        for file in os.listdir(path):
            microfilesys_removedirs(f"{path}/{file}")
            
        if os.getcwd() == path:
            os.chdir("..")

        os.rmdir(path)
        
    else:
        delete_file(path)

def microfilesys_writelines(file_lines):
    """
    Rewrites the whole file with the specified list of lines.
    """
    with open(current_open_path, 'w') as file:
        for line_content in file_lines:
            file.write(line_content)

def microfilesys_rjust(string, width, fill_char=' '):
    """
    Returns a right-justified string.
    """
    if len(string) >= width:
        return string
    
    else:
        padding = fill_char * (width - len(string))
        return padding + string

# command functions
def create_file(file_name, path=os.getcwd()):
    """
    Creates a new file with the specified name in the given path.
    """
    with open(f"{path}/{file_name}", 'w') as file:
        pass

def create_folder(directory_name, path=os.getcwd()):
    """
    Creates a new folder with the specified name in the given path.
    """
    os.mkdir(f"{path}/{directory_name}")

def delete_folder(path):
    """
    Deletes the specified folder recursively.
    """
    microfilesys_removedirs(path)

def delete_file(path):
    """
    Deletes the specified file.
    """
    os.remove(path)

def read_line(line_number):
    """
    Reads and print out the specified line of the file with line number indicator.
    """
    file_lines = get_file_content(current_open_path)
    line_content = file_lines[line_number - 1].rstrip('\n')

    # generate a right-justified line number.
    line_number = microfilesys_rjust(str(line_number), 4)

    print(f"{line_number}| {line_content}")

def read_all():
    """
    Reads and print out the entire file content with line number indicator.
    """
    file_length = get_file_length(current_open_path)

    # print out the entire file content with line number indicator on each line.
    # this operation can be slow for large files.
    for line in range(1, file_length + 1):
        read_line(line)

def fast_read_all():
    """
    Reads and print out the entire content without the line number indicator.
    """
    with open(current_open_path, 'r') as file:
        file_lines = file.readlines()

    if file_lines:
        file_lines[-1] = file_lines[-1].rstrip('\n')

    print(''.join(file_lines))        

def write_line(line_number, content):
    """
    Writes the specified content to the given line number in the currently open file.
    """
    file_lines = get_file_content(current_open_path)

    # load new lines when writing beyond the current range of lines in the file.
    while len(file_lines) < line_number:
        file_lines.append('\n')

    file_lines[line_number - 1] = content + '\n'

    microfilesys_writelines(file_lines)

def write_end(line_number, content):
    """
    Writes the specified content at the end of the line with the given line number in the currently open file.
    """
    file_lines = get_file_content(current_open_path)

    # replace the newline character with the content and re-append the newline character after.
    file_lines[line_number - 1] = file_lines[line_number - 1].rstrip('\n') + content + '\n'

    microfilesys_writelines(file_lines)

def clear_line(line_number):
    """
    Clears the content of the specified line in the currently open file.
    """
    file_lines = get_file_content(current_open_path)
    file_lines[line_number - 1] = '\n'

    microfilesys_writelines(file_lines)

def clear_all():
    """
    Clears all content in the currently open file.
    """
    file_lines = get_file_content(current_open_path)

    # replace each line with a newline character while keeping the original line length (makes it a blank line).
    file_lines = ['\n'] * len(file_lines)

    microfilesys_writelines(file_lines)

def remove_line(line_number):
    """
    Removes the specified line from the currently open file.
    """
    file_lines = get_file_content(current_open_path)
    file_lines.pop(line_number - 1)

    microfilesys_writelines(file_lines)

def remove_all():
    """
    Removes all content from the currently open file.
    """
    with open(current_open_path, 'w') as file:
        file.write('')

# processes function
def process_open_command(option, path):
    """
    Processes the 'open' command, sets the global current_open_path and current_file_mode based on the specified option and path.
    """
    global current_open_path, current_file_mode
    target_path = '/'.join(path.split('/')[:-1])
    target_name = path.split('/')[-1]

    if option not in FILE_OPTION_ALIASES:
        print(f"Invalid option '{option}' for 'open' command.")
        return None

    if not is_path_exists(target_path):
        print(f"Invalid path '{path}' doesn't exist.")
        return None
    
    if not is_file(target_name, target_path) and not is_folder(target_name, target_path):
        print(f"File '{target_name}' doesn't exist on {target_path}")
        return None
    
    if is_folder(target_name, target_path):
        print("Folder can't be used in the 'open' command.")
        return None
    
    current_open_path = path
    current_file_mode = FILE_EDITOR_MODE

def process_create_command(option, path):
    """
    Processes the 'create' command, creates a new file or folder based on the specified option and path.
    """
    target_path = '/'.join(path.split('/')[:-1])
    target_name = path.split('/')[-1]

    if option not in FILE_MANAGER_OPTION_ALISES:
        print(f"Invalid option '{option}' for 'create' command.")
        return None

    if not is_path_exists(target_path):
        print(f"Invalid path '{target_path}' doesn't exist.")
        return None
    
    if target_name in os.listdir(target_path):
        if option in DIR_OPTION_ALIASES and is_file(target_name, target_path):
            print(f"File '{target_name}' already exists on {target_path}")
            return None

        elif option in FILE_OPTION_ALIASES and is_folder(target_name, target_path):
            print(f"Folder '{target_name}' already exists on {target_path}")
            return None
    
    if option in FILE_OPTION_ALIASES:
        if is_file(target_name, target_path):
            if input(f"File '{target_name}' already exists in the directory. Proceed and truncate the file? (y/N): ").lower() not in ['y', "yes"]:
                return None
            
            else:
                create_file(target_name, target_path)
                print(f"File '{target_name}' created successfully. Existing file content erased.")

        else:
            create_file(target_name, target_path)
            print(f"File '{target_name}' created successfully on {target_path}")

    elif option in DIR_OPTION_ALIASES:
        if is_folder(target_name, target_path):
            print(f"Folder '{target_name}' already exists on {target_path}")

        else:
            create_folder(target_name, target_path)
            print(f"Folder '{target_name}' created successfully on {target_path}")

# absolute working
def process_delete_command(option, path):
    """
    Processes the 'delete' command, validates the input, and performs deletion of a file or folder based on the specified option and path.
    """
    target_path = '/'.join(path.split('/')[:-1])
    target_name = path.split('/')[-1]

    if option not in FILE_MANAGER_OPTION_ALISES:
        print(f"Invalid option '{option}' for 'delete' command.")
        return None

    if not is_path_exists(target_path):
        print(f"Invalid path: '{path}' doesn't exist.")
        return None

    if option in FILE_OPTION_ALIASES:
        if is_file(target_name, target_path):
            delete_file(f"{target_path}/{target_name}")
            print(f"File '{target_name}' deleted successfully on {target_path}")

        else:
            print(f"File '{target_name}' doesn't exist on {target_path}")
            return None

    elif option in DIR_OPTION_ALIASES:
        if is_folder(target_name, target_path):
            delete_folder(f"{target_path}/{target_name}")
            print(f"Folder '{target_name}' deleted successfully on {target_path}")

        else:
            print(f"Folder '{target_name}' doesn't exist on {target_path}")
            return None

def process_read_command(option, raw_input):
    """
    Processes the 'read' command, validates incoming inputs.
    """
    input_parts = raw_input.split()

    if option in LINE_OPTION_ALIASES:
        line_number = get_line_number_in_range(raw_input)

        if not line_number:
            return None

        if len(input_parts) != 3:
            print(f"Expected 'read {option} {line_number}'")
            return None
        
        read_line(line_number)

    elif option in ALL_FAST_OPTION_ALIASES:
        if len(input_parts) != 2:
            print(f"Expected 'read {option}'")
            return None
        
        fast_read_all()

    elif option in ALL_OPTION_ALIASES:
        if len(input_parts) != 2:
            print(f"Expected 'read {option}'")
            return None
        
        read_all()

    else:
        print(f"Invalid option '{option}' for 'read' command.")
        return None
    
def process_write_command(option, raw_input):
    """
    Processes the 'write' command, validates incoming inputs and performs writing to a specified line or end of the file.
    """
    line_number = get_line_number(raw_input)

    if not line_number:
        return None

    content = get_content(raw_input)

    if content is None:
        return None

    if option in LINE_OPTION_ALIASES:
        write_line(line_number, content)

    elif option in END_OPTION_ALIASES:
        line_number = get_line_number_in_range(raw_input)
        
        if not line_number:
            return None

        write_end(line_number, content)

    else:
        print(f"Invalid option '{option}' for 'write' command.")
        return None

def process_clear_command(option, raw_input):
    """
    Processes the 'clear' command, validates incoming inputs.
    """
    process_common_command(option, raw_input)

def process_remove_command(option, raw_input):
    """
    Processes the 'remove' command, validates incoming inputs.
    """
    process_common_command(option, raw_input)

def process_common_command(option, raw_input):
    """
    A generic function to handle 'clear', and 'remove' commands.
    """
    common_command_handler = {
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
    command = input_parts[1]

    if option in LINE_OPTION_ALIASES:
        line_number = get_line_number_in_range(raw_input)

        if not line_number:
            return None

        if len(input_parts) != 3:
            print(f"Expected '{command} {option} {line_number}'")
            return None

        common_command_handler[command]["line"]()

    elif option in ALL_OPTION_ALIASES:
        if len(input_parts) != 2:
            print(f"Expected '{command} {option}'")
            return None
        
        common_command_handler[command]["all"]()

    else:
        print(f"Invalid option '{option}' for '{command}' command.")
        return None

# display function
def display_help():
    """
    Displays the help page with information on syntax, options, arguments, and examples.
    """
    print(
f"""Syntax:
    open <-f path="file.txt">                       Open a file for editing (used to access file editor mode).
    create <-f | -d> <path="file.txt">              Create a file or folder in the specified path.
    delete <-f | -d> <path="file.txt">              Delete a file or folder in the specified path.

    read <-l line=int | -a | -af>                   Read the content from the file.
    write <-l | -e> <line=int content="string">     Write content to the file.
    clear <-l line=int | -a>                        Clear the content of from the file but keep the lines.
    remove <-l line=int | -a>                       Remove a line from the file.

    q quit exit                                     Exit the program or go back to file manager mode when in file editor mode.
    h help man manual                               Print out the help page.
    ls list                                         Lis current directory where this script is located and the contents of it.
    v ver version                                   Print out the version of the Microfilesys currently running.

Options:
    -l --line l line                                Specify the line of the file (available: read, write, clear).
    -a --all a all                                  Select all the content of the file (available: read, clear).
    -e --end e end                                  Move the content to the end of the line (available: write).
    -af --all-fast af all-fast                      Used in read command to print the entile file faster (available: read).

    -f --file f file                                Specify that the file argument is an file (available: opem, create, delete).
    -d -dir --directory d dir directory             Specify that the file argument is an folder (available: create, delete).

Argument:
    line=int                                        Specify the line number to work on, i.e. 1, 10, 69.
    content="string"                                Specify a string to be written to the file, i.e. "example string".
    path="file.txt"                                 Specify the path.

Version:
    microfilesys.py {version} {updated}""")

def display_file_list():
    """
    Displays the list of files in the current directory.
    """
    print(os.getcwd())
    for files in os.listdir():
        print(f"|-- {files}")

def display_version():
    """
    Displays the version information.
    """
    print(f"{version} {updated}")

def display_example():
    """
    Displays the example commands.
    """
    print(
"""Example:
    open --file example.txt                         Open the file named "example.txt" for file editing.

    create --file file.txt                          Create a new file named "file.txt" on the current directory.
    create --directory folder                       Create a new directory (folder) named "folder" on the current directory.

    delete --file file.txt                          Delete the file named "file.txt" on the current directory.
    delete --directory folder                       Delete the directory named "folder" and its content on the current directory.

    read --line 1                                   Read and displays the contents of the first line of the file with line number.
    read --all                                      Read and displays the entire contents of the file with line number indicator.
    read --all-fast                                 Read and displays the entire contents of the file quickly without the line number.

    write --line 1 "Lorem"                          Write the string "Lorem" to the first line of the file.
    write --end 1 " Ipsum"                          Append the string " Ipsum" to the end of the first line in the file.

    clear --line 1                                  Clear the content of the first line but keep the of the file.
    clear --all                                     Clear the entire content of the file but keep the lines.

    remove --line 1                                 Remove the first line from the file.
    remove --all                                    Remove all lines from the file.""")

# handle function
def handle_parent_dir(path):
    """
    Handles and formats the path that has a parent directory.
    """
    path_parts = path.split('/')
    target_path = []

    for directory in path_parts:
        if directory == "..":
            # remove the last directory because '..' essentially goes back to the last directory it's currently in or 'folder/.. = folder'.
            if target_path:
                target_path.pop()
        
        else:
            target_path.append(directory)
    
    return '/'.join(target_path)

# main function
def start():
    """
    Starting point of the program, handles the basic input validation.
    """
    global current_open_path, current_file_mode

    print(f"microfilesys.py {version} {updated}\nEnter 'help' for help and 'quit' to quit.\n")

    while True:
        try:
            current_path = os.getcwd()
            raw_input = input(f"microfilesys-{current_open_path}[1/{get_file_length(current_open_path)}]: " if current_open_path else "microfilesys: ")
            input_parts = raw_input.split()

        except KeyboardInterrupt:
            # if the current file mode is file manager when exiting, exit the program.
            if current_file_mode == FILE_MANAGER_MODE:
                return

            # but when its on file manager, just go back to the file editor mode.
            else:
                print()
                current_open_path = None
                current_file_mode = FILE_MANAGER_MODE
                continue

        if not input_parts:
            continue

        # same operation from the KeyboardInterrupt exception.
        if raw_input.strip() in QUIT_KEYWORD:
            if current_file_mode == FILE_MANAGER_MODE:
                return

            else:
                current_open_path = None
                current_file_mode = FILE_MANAGER_MODE
                continue

        if raw_input.strip() in HELP_KEYWORD:
            display_help()
            continue

        if raw_input.strip() in LIST_KEYWORD:
            display_file_list()
            continue
        
        if raw_input.strip() in VERSION_KEYWORD:
            display_version()
            continue
        
        if raw_input.strip() in EXAMPLE_KEYWORD:
            display_example()
            continue

        command = input_parts[0]

        if command not in VALID_COMMANDS:
            print(f"'{raw_input}' is not recognized as a valid command.")
            continue

        if command in FILE_MANAGER_COMMAND:
            if current_file_mode != FILE_MANAGER_MODE:
                print("Status is currently in file editor, exit the mode by entering 'q' in the console.")
                continue
            
            if len(input_parts) == 1:
                print(f"Expected an option after '{command}', i.e. '{command} --line ...'")
                continue

            option = input_parts[1]
            
            if option not in FILE_MANAGER_OPTION_ALISES:
                print(f"'{option}' is not recognized as a valid option.")
                continue

            if len(input_parts) == 2:
                print(f"Expected an file path after '{command}' command, i.e. '{command} --file example.txt'")
                continue
            
            input_path = input_parts[2]
            current_path = get_valid_path(f"{current_path}/{input_path}")

            if not current_path:
                continue
            
            if len(input_parts) > 3:
                print(f"Expected {command} {option} {current_path}")
                continue

            if command == "open":
                process_open_command(option, current_path)

            elif command == "create":
                process_create_command(option, current_path)

            elif command == "delete":
                process_delete_command(option, current_path)

        elif command in FILE_EDITOR_COMMAND:
            if current_file_mode != FILE_EDITOR_MODE:
                print("Status is currently in file manager, open a file by typing 'open --file <file>' in the console.")
                continue

            if len(input_parts) < 2:
                print(f"Expected an option after '{command}', i.e. '{command} --line ...'")
                continue

            option = input_parts[1]

            if option not in FILE_EDITOR_OPTION_ALIASES:
                print(f"'{option}' is not recognized as a valid option.")
                continue

            if command == "read":
                process_read_command(option, raw_input)

            elif command == "write":
                process_write_command(option, raw_input)

            elif command == "clear":
                process_clear_command(option, raw_input)

            elif command == "remove":
                process_remove_command(option, raw_input)

start()