import os

is_open = False
file_open = None
read_indicator = False
last_line_modified = 1
current_index = 0
action_array = []

# command help messages for the microfilesys
command_help = {
    "ls": "ls [directory] - List the contents of the directory.",
    "cd": "cd <directory> - Change the current working directory.",
    "make": "make <--file | --directory | --path> <filename>... - Create a file, directory, or path.\nFlags: --file\t\tCreate a file\n       --directory\tCreate a directory\n       --path\t\tCreate a path\nEx:    make --file file.txt",
    "delete": "delete <--file | --directory | --path> <filename>... - Delete a file, directory, or path.\nFlags: --file\t\tDelete a file\n       --directory\tDelete a directory\n       --path\t\tDelete a path\nEx:    delete --file file.txt",
    "open": "open <file> - Open a file to read and write.\nEx:    open file.txt",
    "close": "close - Close the currently opened file.",
    "read": "read [--line <line> | --all] [--indicator] - Read the line or all lines content.\nFlags: --line <line>\tLine to read\n       --all\t\tRead all lines\n       --indicator\tDisplay line number\nEx:    read --line 1",
    "write": 'write [--line <line> | --end [line] | --all] ["string"] - Write content to the line, end of the line, or all lines.\nFlags: --line <line>\tLine to write\n       --end [line]\tWrite at the end of the line\n       --all\t\tReplace all lines with the string\nEx:    write --line 1 "Hello, World!"',
    "clear": "clear <--line <line> | --all> - Clear the line or all lines content.\nFlags: --line <line>\tClear the line content\n       --all\t\tClear all file content\nEx:    clear --line 1",
    "remove": "remove <--line <line> | --all> - Remove the line or all lines content.\nFlags: --line <line>\tRemove the line\n       --all\t\tRemove all file lines\nEx:    remove --line 1",
    "undo": "undo - Undo the last action.",
    "redo": "redo - Redo the last action.",
}


def is_file(file_name):
    """Check if the given name is a file (not a directory)."""
    return not os.stat(f"{os.getcwd()}/{file_name}")[0] & 0x4000


def is_folder(folder_name):
    """Check if the given name is a directory."""
    return os.stat(f"{os.getcwd()}/{folder_name}")[0] & 0x4000


def is_line_number_in_range(line_number):
    """Check if the line number is within the range of the file length."""
    global file_open
    total_lines = get_file_length(file_open)
    return 1 <= line_number <= total_lines


def get_file_length(file_name):
    """Get the total number of lines in the file."""
    return len(get_file_content(file_name))


def get_file_content(file_name):
    """Get the content of the file as a list of lines."""
    with open(file_name, "r") as file:
        file_lines = file.readlines()

    # add a newline character when reading a blank file
    if not file_lines:
        file_lines.append("\n")
    return file_lines


def writelines_to_file(file_lines):
    """Rewrite the whole file with the list of lines."""
    global file_open
    with open(file_open, "w") as file:
        for line_content in file_lines:
            file.write(line_content)


def right_justify_string(string, width, fill_char=" "):
    """Return a right-justified string with padding."""
    if len(string) >= width:
        return string
    else:
        padding = fill_char * (width - len(string))
        return padding + string


def update_action_array():
    """Update the action array with the current file content."""
    global current_index, action_array, file_open
    if current_index != len(action_array):
        action_array = action_array[: current_index + 1]
        current_index = len(action_array)
    else:
        current_index += 1
        action_array.append(get_file_content(file_open))


def parse_content(string):
    """Find the first and last occurrence of quotes in the string.
    Multiple quotes are allowed - quotes are used to enclose content."""
    if string.count('"') == 0:
        return ""
    first_quote = string.find('"')  # first occurrence of double quote
    if first_quote == -1:
        print("No starting quote found")
        return None
    second_quote = string[first_quote + 1 :].rfind(
        '"'
    )  # last occurrence of double quote
    if second_quote == -1:
        print("No ending quote found")
        return None
    content = string[first_quote : first_quote + second_quote + 2]
    return content


def help_command(command):
    """Print the help message for the command. If no command is provided,
    print all available command keywords."""
    global command_help
    if command is None:
        print("Commands:")
        print(
            "ls, cd, make, delete, open, close, read, write, clear, remove, undo, redo"
        )
        print("Type 'help [command]' for more information.")
    else:
        print(command_help[command])


def ls_command(path):
    """List the contents of the directory."""
    try:
        content = os.listdir(path)
        for item in content:
            print(item)
    except Exception as e:
        print(f"Error: {e}")


def cd_command(path):
    """Change the current working directory."""
    try:
        os.chdir(path)
    except Exception as e:
        print(f"Error: {e}")


def mkdir_command(folders):
    """Create directories."""
    for folder in folders:
        try:
            os.mkdir(folder)
        except Exception as e:
            print(f"Error: {e}")


def rmdir_command(folders):
    """Remove directories."""
    for folder in folders:
        try:
            os.rmdir(folder)
        except Exception as e:
            print(f"Error: {e}")


def mkfile_command(files):
    """Create empty files."""
    for file in files:
        try:
            with open(file, "w") as f:
                pass
        except Exception as e:
            print(f"Error: {e}")


def rmfile_command(files):
    """Remove files."""
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error: {e}")


def mkpath_command(paths):
    """Create directories recursively."""
    for path in paths:
        try:
            os.makedirs(path)
        except Exception as e:
            print(f"Error: {e}")


def rmpath_command(paths):
    """Recursively remove the contents of the directory.
    Based on Roberthh's implementation:
    https://forum.micropython.org/viewtopic.php?t=7512#p42783"""
    for path in paths:
        try:
            if os.stat(path)[0] & 0x4000:
                for item in os.listdir(path):
                    if item not in [".", ".."]:
                        rmpath_command([f"{path}/{item}"])
                rmdir_command([path])
            else:
                rmfile_command([path])
        except Exception as e:
            print(f"Error: {e}")


def open_file(file):
    """Open the file for reading and writing operations."""
    global file_open, is_open, current_index, action_array
    try:
        with open(file, "r") as f:
            file_open = file
            is_open = True
            current_index = 1
            # store the initial file content
            action_array.append(get_file_content(file_open))
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def close_file():
    """Close the currently opened file."""
    global is_open, file_open, current_index, action_array
    is_open = False
    file_open = None
    current_index = 0
    action_array = []


def read_line(line_number):
    """Read the content of a specific line."""
    global file_open
    file_lines = get_file_content(file_open)
    line_content = file_lines[line_number - 1].rstrip("\n")
    print(line_content)


def read_line_with_indicator(line_number):
    """Read the content of a line with preceding line number."""
    global file_open
    file_lines = get_file_content(file_open)
    line_content = file_lines[line_number - 1].rstrip("\n")
    line_num_str = right_justify_string(str(line_number), 4)
    print(f"{line_num_str}| {line_content}")


def read_all_lines():
    """Read the content of the entire file."""
    global file_open
    with open(file_open, "r") as file:
        for line in file:
            print(line.rstrip("\n"))


def read_all_lines_with_indicator():
    """Read the entire content of the file with preceding line numbers."""
    global file_open
    file_lines = get_file_content(file_open)
    for line_number, line_content in enumerate(file_lines, 1):
        line_num_str = right_justify_string(str(line_number), 4)
        print(f"{line_num_str}| {line_content.rstrip('\n')}")


def write_line(line_number, content):
    """Rewrite the specified line with the content.
    If the line is out of range, append the content at the end of the file."""
    global file_open
    file_lines = get_file_content(file_open)
    while len(file_lines) < line_number:
        file_lines.append("\n")

    file_lines[line_number - 1] = content + "\n"
    writelines_to_file(file_lines)


def write_at_end_of_line(line_number, content):
    """Write content at the end of the specified line.
    If the line number is out of range, append the content at the end of the file."""
    global file_open
    file_lines = get_file_content(file_open)
    file_lines[line_number - 1] = (
        file_lines[line_number - 1].rstrip("\n") + content + "\n"
    )
    writelines_to_file(file_lines)


def clear_line(line_number):
    """Clear the content of a specific line."""
    global file_open
    file_lines = get_file_content(file_open)
    file_lines[line_number - 1] = "\n"
    writelines_to_file(file_lines)


def clear_all_lines():
    """Clear the entire file content."""
    global file_open
    file_lines = get_file_content(file_open)
    file_lines = ["\n"] * len(file_lines)
    writelines_to_file(file_lines)


def remove_line(line_number):
    """Remove a specific line from the file."""
    global file_open
    file_lines = get_file_content(file_open)
    file_lines.pop(line_number - 1)
    writelines_to_file(file_lines)


def remove_all_lines():
    """Remove all content from the file."""
    global file_open
    with open(file_open, "w") as file:
        file.write("")


def read_command(args):
    """Parse the arguments and execute the appropriate read command."""
    global read_indicator, file_open
    if "--indicator" in args:
        read_indicator = True
    if "-l" in args or "--line" in args:
        arg_index = [args.index(arg) for arg in args if arg in ["-l", "--line"]][0]
        line = None

        # check if the line number provided is an integer and in range of the file length
        try:
            if args[arg_index + 1].isdigit():
                line = int(args[arg_index + 1])
                if not is_line_number_in_range(line):
                    print(
                        f"Line number must be in range of 1/{get_file_length(file_open)}."
                    )
                    return
            else:
                print("Line number must be an integer.")
                return
        except IndexError:
            print("Line number is not provided.")
            return

        # read --line <line>             - read the line content
        # read --line <line> --indicator - read the line content with line number
        if len(args) == 3:  # read --line <line>
            read_line(line)
        elif (
            read_indicator and len(args) == 4
        ):  # read --line <line> --indicator | read --indicator --line <line>
            read_line_with_indicator(line)
        else:
            print("Invalid syntax. Did you mean 'read --line <line> --indicator'?")
    elif "-a" in args or "--all" in args:
        # read --all             - read all lines content
        # read --all --indicator - read all lines content with line number
        if len(args) == 2:  # read --all
            read_all_lines()
        elif (
            len(args) == 3 and read_indicator
        ):  # read --all --indicator | read --indicator --all
            read_all_lines_with_indicator()
        else:
            print("Invalid syntax. Did you mean 'read --all --indicator'?")
    else:
        print(
            "Invalid syntax. Did you mean 'read [--line <line> | --all] [--indicator]'?"
        )
    read_indicator = False


def write_command(args):
    """Parse the arguments and execute the appropriate write command."""
    global last_line_modified, file_open
    content = " ".join([arg for arg in args if arg.startswith('"')])

    # write "string" - write "string" at the end of the current line
    if len(args) == 2 and args[1].startswith('"'):
        write_at_end_of_line(last_line_modified, content[1:-1])
        return
    elif "-l" in args or "--line" in args:
        arg_index = [args.index(arg) for arg in args if arg in ["-l", "--line"]][0]
        line = None
        has_content = any(arg.startswith('"') for arg in args)

        # check if the line number provided is an integer
        try:
            if args[arg_index + 1].isdigit():
                line = int(args[arg_index + 1])
            else:
                print("Line number must be an integer.")
                return
        except IndexError:
            print("Line number is not provided.")
            return

        # write --line <line>          - do nothing
        # write --line <line> "string" - write "string" at the line
        if len(args) == 3:  # write --line <line>
            pass
        elif (
            has_content and len(args) == 4
        ):  # write --line <line> "string" | write "string" --line <line>
            write_line(line, content[1:-1])
        else:
            print("Invalid syntax. Did you mean 'write --line <line> \"string\"'?")
        last_line_modified = line
    elif "-e" in args or "--end" in args:
        arg_index = [args.index(arg) for arg in args if arg in ["-e", "--end"]][0]
        line = None
        has_content = any(arg.startswith('"') for arg in args)
        try:
            if args[arg_index + 1].isdigit():
                line = int(args[arg_index + 1])
                if not is_line_number_in_range(line):
                    print(
                        f"Line number must be in range of 1/{get_file_length(file_open)}."
                    )
                    return
            else:
                pass
        except IndexError:
            pass

        # write --end                 - do nothing
        # write --end [line]          - do nothing
        # write --end "string"        - write "string" at the end of the file
        # write --end [line] "string" - write "string" at the end of the line
        if len(args) == 2:  # write --end
            pass
        elif len(args) == 3 and line:  # write --end [line]
            pass
        elif (
            len(args) == 3 and has_content
        ):  # write --end "string" | write "string" --end
            write_at_end_of_line(get_file_length(file_open), content[1:-1])
        # added "arg_index + 1 < len(args)" to prevent IndexError when the last argument is --end
        # this assumes that the next argument is a line number, but --end may be the last argument
        elif (
            len(args) == 4 and arg_index + 1 < len(args) and line and has_content
        ):  # write --end [line] "string" | write "string" --end [line]
            write_at_end_of_line(int(args[arg_index + 1]), content[1:-1])
        else:
            print("Invalid syntax. Did you mean 'write --end [line] \"string\"'?")
    elif "-a" in args or "--all" in args:
        has_content = any(arg.startswith('"') for arg in args)

        # write --all          - do nothing
        # write --all "string" - replace the entire file content with "string"
        if len(args) == 2:  # write --all
            pass
        elif (
            len(args) == 3 and has_content
        ):  # write --all "string" | write "string" --all
            clear_all_lines()
            write_line(1, content[1:-1])
        else:
            print("Invalid syntax. Did you mean 'write --all \"string\"'?")
    else:
        print(
            "Invalid syntax. Did you mean 'write [--line <line> | --end [line] | --all] [\"string\"]'?"
        )


def clear_command(args):
    """Parse the arguments and execute the appropriate clear command."""
    global last_line_modified, file_open
    if "-l" in args or "--line" in args:
        arg_index = [args.index(arg) for arg in args if arg in ["-l", "--line"]][0]
        line = None

        # check if the line number provided is an integer and in range of the file length
        try:
            if args[arg_index + 1].isdigit():
                line = int(args[arg_index + 1])
                if not (line >= 1 and line <= get_file_length(file_open)):
                    print(
                        f"Line number must be in range of 1/{get_file_length(file_open)}."
                    )
                    return
            else:
                print("Line number must be an integer.")
                return
        except IndexError:
            print("Line number is not provided.")
            return

        # clear --line <line> - clear the line content
        if len(args) == 3:  # clear --line <line>
            clear_line(line)
        else:
            print("Invalid syntax. Did you mean 'clear --line <line>'?")
    elif "-a" in args or "--all" in args:
        # clear --all - clear the entire file content
        if len(args) == 2:  # clear --all
            clear_all_lines()
        else:
            print("Invalid syntax. Did you mean 'clear --all'?")
    else:
        print("Invalid syntax. Did you mean 'clear [--line <line> | --all]'?")
    last_line_modified = 1


def remove_command(args):
    """Parse the arguments and execute the appropriate remove command."""
    global last_line_modified, file_open
    if "-l" in args or "--line" in args:
        arg_index = [args.index(arg) for arg in args if arg in ["-l", "--line"]][0]
        line = None

        # check if the line number provided is an integer and in range of the file length
        try:
            if args[arg_index + 1].isdigit():
                line = int(args[arg_index + 1])
                if not (line >= 1 and line <= get_file_length(file_open)):
                    print(
                        f"Line number must be in range of 1/{get_file_length(file_open)}."
                    )
                    return
            else:
                print("Line number must be an integer.")
                return
        except IndexError:
            print("Line number is not provided.")
            return

        # remove --line <line> - remove the line content
        if len(args) == 3:  # remove --line <line>
            remove_line(line)
        else:
            print("Invalid syntax. Did you mean 'remove --line <line>'?")
    elif "-a" in args or "--all" in args:
        # remove --all - remove the entire file content
        if len(args) == 2:  # remove --all
            remove_all_lines()
        else:
            print("Invalid syntax. Did you mean 'remove --all'?")
    else:
        print("Invalid syntax. Did you mean 'remove [--line <line> | --all]'?")
    last_line_modified = 1
