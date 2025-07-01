import os
import sys
from microfilesys import (
    ls_command,
    cd_command,
    mkfile_command,
    mkdir_command,
    mkpath_command,
    rmfile_command,
    rmdir_command,
    rmpath_command,
    open_file,
    close_file,
    read_command,
    write_command,
    clear_command,
    remove_command,
    update_action_array,
    clear_all_lines,
    get_file_length,
    parse_content,
    writelines_to_file,
    help_command,
    is_open,
    file_open,
    current_index,
    action_array,
    last_line_modified,
    command_help,
)

def main():
    """Main loop of the program that takes user input and executes commands."""
    global is_open, file_open, current_index, action_array, last_line_modified, command_help

    while True:
        try:
            if is_open:
                user_input = input(
                    f"{os.getcwd().replace('\\', '/')}/{file_open}[1/{get_file_length(file_open)}]: "
                )
            else:
                user_input = input(f"{os.getcwd().replace('\\', '/')}: ")

            if not user_input:
                continue

            # early check if the command is write and if the content is enclosed in double quotes
            if user_input.startswith("write"):
                content = parse_content(user_input)
                if content is None:
                    continue
                elif content:
                    # replace the content with an empty string to prevent it from being split,
                    # then replace it back with the actual content.
                    # the outcome will be a list of arguments with the content enclosed with
                    # double quotes retaining the original content format.
                    user_input = user_input.replace(content, '""').split()
                    user_input[user_input.index('""')] = content
                else:
                    user_input = user_input.split()
            else:
                user_input = user_input.split()
        except KeyboardInterrupt:
            break

        # prevent file editing specific commands from being executed without an opened file
        if (
            user_input[0] in ["read", "write", "clear", "remove", "undo", "redo"]
            and not is_open
        ):
            print("No opened file. Use 'open <file>' to open and edit a file.")

        # quit, help, undo, redo commands
        elif user_input[0] in ["q", "quit", "exit"]:
            if len(user_input) != 1:
                print("Invalid command. Did you mean 'q' or 'quit' or 'exit'?")
            else:
                sys.exit(0)

        elif user_input[0] in ["h", "help", "?"]:
            if len(user_input) == 1:
                help_command(None)
            elif len(user_input) == 2:
                if user_input[1] in list(command_help.keys()):
                    help_command(user_input[1])
                else:
                    print(f"{user_input[1]} is not a valid command.")
            else:
                print("Invalid command. Did you mean 'h, help, ? [command]'?")

        elif user_input[0] == "close":
            if len(user_input) != 1:
                print("Invalid command. Did you mean 'close'?")
            elif not is_open:
                print("No file is open.")
            else:
                close_file()
                print("File closed.")

        elif user_input[0] == "undo":
            if len(user_input) != 1:
                print("Invalid command. Did you mean 'undo'?")
            if current_index <= 1:
                pass
            else:
                print("undo")
                current_index -= 1
                clear_all_lines()
                writelines_to_file(action_array[current_index - 1])

        elif user_input[0] == "redo":
            if len(user_input) != 1:
                print("Invalid command. Did you mean 'redo'?")
            if current_index >= len(action_array):
                pass
            else:
                print("redo")
                current_index += 1
                clear_all_lines()
                writelines_to_file(action_array[current_index - 1])

        # navigate through the filesystem
        elif user_input[0] == "ls":
            if len(user_input) == 1:
                ls_command(os.getcwd())
            elif len(user_input) == 2:
                ls_command(user_input[1])
            else:
                print("Invalid command. Did you mean 'ls [directory]'?")

        elif user_input[0] == "cd":
            if len(user_input) == 2:
                cd_command(user_input[1])
            else:
                print("Invalid command. Did you mean 'cd <directory>'?")

        # create or delete files, directories, or paths
        elif user_input[0] == "make":
            if len(user_input) == 1:
                print(command_help["make"])
            elif user_input[1] in ["-f", "--file"]:
                if len(user_input) == 2:
                    print("Invalid command. Did you mean 'make --file <filename>...'?")
                else:
                    mkfile_command(user_input[2:])
            elif user_input[1] in ["-d", "--directory"]:
                if len(user_input) == 2:
                    print(
                        "Invalid command. Did you mean 'make --directory <filename>...'?"
                    )
                else:
                    mkdir_command(user_input[2:])
            elif user_input[1] in ["-p", "--path"]:
                if len(user_input) == 2:
                    print("Invalid command. Did you mean 'make --path <filename>...'?")
                else:
                    mkpath_command(user_input[2:])
            else:
                print(
                    "Invalid command. Did you mean 'make <--file | --directory | --path> <filename>...'?"
                )

        elif user_input[0] == "delete":
            if len(user_input) == 1:
                print(command_help["delete"])
            elif user_input[1] in ["-f", "--file"]:
                if len(user_input) == 2:
                    print(
                        "Invalid command. Did you mean 'delete --file <filename>...'?"
                    )
                else:
                    rmfile_command(user_input[2:])
            elif user_input[1] in ["-d", "--directory"]:
                if len(user_input) == 2:
                    print(
                        "Invalid command. Did you mean 'delete --directory <filename>...'?"
                    )
                else:
                    rmdir_command(user_input[2:])
            elif user_input[1] in ["-p", "--path"]:
                if len(user_input) == 2:
                    print(
                        "Invalid command. Did you mean 'delete --path <filename>...'?"
                    )
                else:
                    rmpath_command(user_input[2:])
            else:
                print(
                    "Invalid command. Did you mean 'delete <--file | --directory | --path> <filename>...'?"
                )

        elif user_input[0] == "open":
            if len(user_input) == 1:
                print(command_help["open"])
            elif len(user_input) == 2:
                if is_open:
                    print(
                        f"{file_open} is already open, use 'close' to close the file and open a new one."
                    )
                elif open_file(user_input[1]):
                    print(f"File '{file_open}' opened.")
            else:
                print("Invalid command. Did you mean 'open <file>'?")

        elif user_input[0] == "read":
            if len(user_input) == 1:
                print(command_help["read"])
            else:
                read_command(user_input)

        elif user_input[0] == "write":
            if len(user_input) == 1:
                print(command_help["write"])
            else:
                write_command(user_input)
                update_action_array()

        elif user_input[0] == "clear":
            if len(user_input) == 1:
                print(command_help["clear"])
            else:
                clear_command(user_input)
                update_action_array()

        elif user_input[0] == "remove":
            if len(user_input) == 1:
                print(command_help["remove"])
            else:
                remove_command(user_input)
                update_action_array()

        else:
            print(f"{user_input[0]} is not a valid command.")

        continue


if __name__ == "__main__":
    main()
