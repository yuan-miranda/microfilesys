import os
import sys

class microfilesys:
    def __init__(self):
        self.is_open = False
        self.file_open = None
        self.indicator_read = False
        self.last_line_modified = 1
        self.current_index = 0
        self.action_array = []

        # thanks ChatGPT for generating this very tedious help message lol.
        self.command_help = {
            "ls": "ls [directory] - List the contents of the specified directory.",
            "cd": "cd <directory> - Change the current working directory.",
            "make": "make <--file | --directory | --path> <filename>... - Create a file, directory, or path.\nFlags: --file\t\tCreate a file\n       --directory\tCreate a directory\n       --path\t\tCreate a path\nEx:    make --file file.txt",
            "delete": "delete <--file | --directory | --path> <filename>... - Delete a file, directory, or path.\nFlags: --file\t\tDelete a file\n       --directory\tDelete a directory\n       --path\t\tDelete a path\nEx:    delete --file file.txt",
            "open": "open <file> - Open a file to read and write.\nEx:    open file.txt",
            "close": "close - Close the currently opened file.",
            "read": "read [--line <line> | --all] [--indicator] - Read the specified line or all lines content.\nFlags: --line <line>\tLine to read\n       --all\t\tRead all lines\n       --indicator\tDisplay line number\nEx:    read --line 1",
            "write": "write [--line <line> | --end [line] | --all] [\"string\"] - Write content to the specified line, end of the line, or all lines.\nFlags: --line <line>\tLine to write\n       --end [line]\tWrite at the end of the line\n       --all\t\tReplace all lines with the string\nEx:    write --line 1 \"Hello, World!\"",
            "clear": "clear <--line <line> | --all> - Clear the specified line or all lines content.\nFlags: --line <line>\tClear the line content\n       --all\t\tClear all file content\nEx:    clear --line 1",
            "remove": "remove <--line <line> | --all> - Remove the specified line or all lines content.\nFlags: --line <line>\tRemove the line\n       --all\t\tRemove all file lines\nEx:    remove --line 1",
            "undo": "undo - Undo the last action.",
            "redo": "redo - Redo the last action."
        }

    def is_file(self, file_name):
        """Returns True if the specified file is a file, otherwise False."""
        return not os.stat(f"{os.getcwd()}/{file_name}")[0] & 0x4000

    def is_folder(self, folder_name):
        """Returns True if the specified folder is a directory, otherwise False."""
        return os.stat(f"{os.getcwd()}/{folder_name}")[0] & 0x4000

    def get_file_length(self, file_name):
        """Returns the total number of lines in the specified file."""
        return len(self.get_file_content(file_name))

    def get_file_content(self, file_name):
        """Returns the content of the specified file as a list of lines."""
        with open(file_name, 'r') as file:
            file_lines = file.readlines()

        # adds a newline character when reading a blank file.
        if not file_lines:
            file_lines.append('\n')
        return file_lines

    def microfilesys_writelines(self, file_lines):
        """Rewrites the whole file with the specified list of lines."""
        with open(self.file_open, 'w') as file:
            for line_content in file_lines:
                file.write(line_content)

    def microfilesys_rjust(self, string, width, fill_char=' '):
        """Returns a right-justified string."""
        if len(string) >= width:
            return string
        else:
            padding = fill_char * (width - len(string))
            return padding + string

    def is_line_number_in_range(self, line_number):
        """Returns True if the specified line number is in range of the file length, otherwise False."""
        total_lines = self.get_file_length(self.file_open)
        return 1 <= line_number <= total_lines

    def update_action_array(self):
        """Updates the action array with the current file content."""
        if self.current_index != len(self.action_array):
            self.action_array = self.action_array[:self.current_index + 1]
            self.current_index = len(self.action_array)
        else:
            self.current_index += 1
            self.action_array.append(self.get_file_content(self.file_open))

    def parse_content(self, raw_input):
        """This finds the first and last occurance of '"' in the string.
        you can input as many quotes as you want and it will still be valid.
        '"' is used to enclose the content."""
        if raw_input.count('\"') == 0:
            return ""
        first_quote = raw_input.find('\"') # first occurrence of double quote
        if first_quote == -1:
            print("Error: No starting quote found")
            return None
        second_quote = raw_input[first_quote + 1:].rfind('\"') # second occurrence of double quote
        if second_quote == -1:
            print("Error: No ending quote found")
            return None
        content = raw_input[first_quote:first_quote + second_quote + 2]
        return content

    def help(self, command):
        """Prints the help message for the specified command. If no command is provided,
        it prints all available commands keywords."""
        if command == None:
            print("Commands:")
            print("ls, cd, make, delete, open, close, read, write, clear, remove, undo, redo")
            print("Type 'help [command]' for more information.")
        else:
            print(self.command_help[command])
            
    def ls(self, path):
        """Lists the contents of the specified directory."""
        try:
            content = os.listdir(path)
            for item in content:
                print(item)
        except Exception as e:
            print(f"Error: {e}")

    def cd(self, directory):
        """Changes the current working directory."""
        try:
            os.chdir(directory)
        except Exception as e:
            print(f"Error: {e}")

    def mkdir(self, folders):
        """Creates the specified directories."""
        for folder in folders:
            try:
                os.mkdir(folder)
            except Exception as e:
                print(f"Error: {e}")

    def rmdir(self, folders):
        """Removes the specified directories."""
        for folder in folders:
            try:
                os.rmdir(folder)
            except Exception as e:
                print(f"Error: {e}")

    def mkfile(self, files):
        """Creates the specified files."""
        for file in files:
            try:
                with open(file, "w") as f:
                    pass
            except Exception as e:
                print(f"Error: {e}")

    def rmfile(self, files):
        """Removes the specified files."""
        for file in files:
            try:
                os.remove(file)
            except Exception as e:
                print(f"Error: {e}")

    def mkpath(self, paths):
        """Creates the specified directories recursively."""
        for path in paths:
            try:
                os.makedirs(path)
            except Exception as e:
                print(f"Error: {e}")

    def rmpath(self, paths):
        """Recursively removes the specified directory. Based on Roberthh's implementation
        https://forum.micropython.org/viewtopic.php?t=7512#p42783."""
        for path in paths:
            try:
                if os.stat(path)[0] & 0x4000:
                    for item in os.listdir(path):
                        if item not in [".", ".."]:
                            self.rmpath([f"{path}/{item}"])
                    self.rmdir([path])
                else:
                    self.rmfile([path])
            except Exception as e:
                print(f"Error: {e}")

    def open(self, file):
        """Opens the specified file for reading and writing."""
        try:
            with open(file, "r") as f:
                self.file_open = file
                self.is_open = True
                self.current_index = 1
                # store the initial file content.
                self.action_array.append(self.get_file_content(self.file_open))
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def close(self):
        """Closes the currently opened file."""
        self.is_open = False
        self.file_open = None
        self.current_index = 0
        self.action_array = []

    def read_line(self, line_number):
        """Reads the specified line content."""
        file_lines = self.get_file_content(self.file_open)
        line_content = file_lines[line_number - 1].rstrip('\n')
        print(line_content)

    def read_line_indicator(self, line_number):
        """Reads the specified line content with line number."""
        file_lines = self.get_file_content(self.file_open)
        line_content = file_lines[line_number - 1].rstrip('\n')
        line_number = self.microfilesys_rjust(str(line_number), 4)
        print(f"{line_number}| {line_content}")
    
    def read_all(self):
        """Reads all lines content."""
        with open(self.file_open, 'r') as file:
            for line in file:
                print(line.rstrip("\n"))

    def read_all_indicator(self):
        """Reads all lines content with line number."""
        file_lines = self.get_file_content(self.file_open)
        for line_number, line_content in enumerate(file_lines, 1):
            line_number = self.microfilesys_rjust(str(line_number), 4)
            print(f"{line_number}| {line_content.rstrip('\n')}")

    def write_line(self, line_number, content):
        """Writes the specified content at the specified line number.
        If the line number is out of range, it appends the content at the end of the file."""
        file_lines = self.get_file_content(self.file_open)
        while len(file_lines) < line_number:
            file_lines.append('\n')

        file_lines[line_number - 1] = content + '\n'
        self.microfilesys_writelines(file_lines)

    def write_end(self, line_number, content):
        """Writes the specified content at the end of the specified line number.
        If the line number is out of range, it appends the content at the end of the file."""
        file_lines = self.get_file_content(self.file_open)
        file_lines[line_number - 1] = file_lines[line_number - 1].rstrip('\n') + content + '\n'
        self.microfilesys_writelines(file_lines)

    def clear_line(self, line_number):
        """Clears the specified line content."""
        file_lines = self.get_file_content(self.file_open)
        file_lines[line_number - 1] = '\n'
        self.microfilesys_writelines(file_lines)

    def clear_all(self):
        """Clears the entire file content."""
        file_lines = self.get_file_content(self.file_open)
        file_lines = ['\n'] * len(file_lines)
        self.microfilesys_writelines(file_lines)

    def remove_line(self, line_number):
        """Removes the specified line content."""
        file_lines = self.get_file_content(self.file_open)
        file_lines.pop(line_number - 1)
        self.microfilesys_writelines(file_lines)

    def remove_all(self):
        """Removes the entire file content."""
        with open(self.file_open, 'w') as file:
            file.write('')

    def read_command(self, args):
        """Parses the read command and executes the appropriate action."""
        if "--indicator" in args:
            self.indicator_read = True
        if "-l" in args or "--line" in args:
            arg_index = [args.index(arg) for arg in args if arg in ["-l", "--line"]][0]
            line = None

            # check if the line number provided is an integer and in range of the file length.
            try:
                if args[arg_index + 1].isdigit():
                    line = int(args[arg_index + 1])
                    if not self.is_line_number_in_range(line):
                        print(f"Error: Line number must be in range of 1/{self.get_file_length(self.file_open)}.")
                        return
                else:
                    print("Error: Line number must be an integer.")
                    return
            except IndexError:
                print("Error: Line number is not provided.")
                return

            # read --line <line>             - read the specified line content.
            # read --line <line> --indicator - read the specified line content with line number.
            if len(args) == 3: # read --line <line>
                self.read_line(line)
            elif self.indicator_read and len(args) == 4: # read --line <line> --indicator | read --indicator --line <line>
                self.read_line_indicator(line)
            else:
                print("Error: Invalid syntax did you mean 'read --line <line> --indicator'?")
        elif "-a" in args or "--all" in args:
            # read --all             - read all lines content.
            # read --all --indicator - read all lines content with line number.
            if len(args) == 2: #  read --all
                self.read_all()
            elif len(args) == 3 and self.indicator_read: # read --all --indicator | read --indicator --all
                self.read_all_indicator()
            else:
                print("Error: Invalid syntax did you mean 'read --all --indicator'?")
        else:
            print("Error: Invalid syntax did you mean 'read [--line <line> | --all] [--indicator]'?")
        self.indicator_read = False

    def write_command(self, args):
        """Parses the write command and executes the appropriate action."""
        content = " ".join([arg for arg in args if arg.startswith("\"")])

        # write "string" - write "string" at the end of the current line.
        if len(args) == 2 and args[1].startswith("\""):
            self.write_end(self.last_line_modified, content[1:-1])
            return
        elif "-l" in args or "--line" in args:
            arg_index = [args.index(arg) for arg in args if arg in ["-l", "--line"]][0]
            line = None
            has_content = any(arg.startswith("\"") for arg in args)

            # check if the line number provided is an integer and in range of the file length.
            try:
                if args[arg_index + 1].isdigit():
                    line = int(args[arg_index + 1])
                else:
                    print("Error: Line number must be an integer.")
                    return
            except IndexError:
                print("Error: Line number is not provided.")
                return
            
            # write --line <line>          - do nothing.
            # write --line <line> "string" - write "string" at the specified line.
            if len(args) == 3: # write --line <line>
                # self.write_line(line, "")
                pass
            elif has_content and len(args) == 4: # write --line <line> "string" | write "string" --line <line>
                self.write_line(line, content[1:-1])
            else:
                print("Error: Invalid syntax did you mean 'write --line <line> \"string\"'?")
            self.last_line_modified = line
        elif "-e" in args or "--end" in args:
            arg_index = [args.index(arg) for arg in args if arg in ["-e", "--end"]][0]
            line = None
            has_content = any(arg.startswith("\"") for arg in args)
            try:
                if args[arg_index + 1].isdigit():
                    line = int(args[arg_index + 1])
                    if not self.is_line_number_in_range(line):
                        print(f"Error: Line number must be in range of 1/{self.get_file_length(self.file_open)}.")
                        return
                else:
                    pass
            except IndexError:
                pass

            # write --end                 - do nothing.
            # write --end [line]          - do nothing.
            # write --end "string"        - write "string" at the end of the file.
            # write --end [line] "string" - write "string" at the end of the specified line.
            if len(args) == 2: # write --end            
                # self.write_end(self.get_file_length(self.file_open), "")
                pass
            elif len(args) == 3 and line: # write --end [line]
                # self.write_end(line, "")
                pass
            elif len(args) == 3 and has_content: # write --end "string" | write "string" --end
                self.write_end(self.get_file_length(self.file_open), content[1:-1])
            
            # added "arg_index + 1 < len(args)" to prevent IndexError when the last argument is --end.
            # cause this assumes that the next argument is a line number, but --end is the last argument.
            elif len(args) == 4 and arg_index + 1 < len(args) and line and has_content: # write --end [line] "string" | write "string" --end [line]
                self.write_end(int(args[arg_index + 1]), content[1:-1])
            else:
                print("Error: Invalid syntax did you mean 'write --end [line] \"string\"'?")
        elif "-a" in args or "--all" in args:
            has_content = any(arg.startswith("\"") for arg in args)

            # write --all          - do nothing.
            # write --all "string" - replace the entire file content with "string".
            if len(args) == 2: # write --all
                # self.clear_all()
                pass
            elif len(args) == 3 and has_content: # write --all "string" | write "string" --all
                self.clear_all()
                self.write_line(1, content[1:-1])
            else:
                print("Error: Invalid syntax did you mean 'write --all \"string\"'?")
        else:
            print("Error: Invalid syntax did you mean 'write [--line <line> | --end [line] | --all] [\"string\"]'?")

    def clear_command(self, args):
        """Parses the clear command and executes the appropriate action."""
        if "-l" in args or "--line" in args:
            arg_index = [args.index(arg) for arg in args if arg in ["-l", "--line"]][0]
            line = None

            # check if the line number provided is an integer and in range of the file length.
            try:
                if args[arg_index + 1].isdigit():
                    line = int(args[arg_index + 1])
                    if not (line >= 1 and line <= self.get_file_length(self.file_open)):
                        print(f"Error: Line number must be in range of 1/{self.get_file_length(self.file_open)}.")
                        return
                else:
                    print("Error: Line number must be an integer.")
                    return
            except IndexError:
                print("Error: Line number is not provided.")
                return
            
            # clear --line <line> - clear the specified line content.
            if len(args) == 3: # clear --line <line>
                self.clear_line(line)
            else:
                print("Error: Invalid syntax did you mean 'clear --line <line>'?")
        elif "-a" in args or "--all" in args:
            # clear --all - clear the entire file content.
            if len(args) == 2: # clear --all
                self.clear_all()
            else:
                print("Error: Invalid syntax did you mean 'clear --all'?")
        else:
            print("Error: Invalid syntax did you mean 'clear [--line <line> | --all]'?")
        self.last_line_modified = 1

    def remove_command(self, args):
        """Parses the remove command and executes the appropriate action."""
        if "-l" in args or "--line" in args:
            arg_index = [args.index(arg) for arg in args if arg in ["-l", "--line"]][0]
            line = None

            # check if the line number provided is an integer and in range of the file length.
            try:
                if args[arg_index + 1].isdigit():
                    line = int(args[arg_index + 1])
                    if not (line >= 1 and line <= self.get_file_length(self.file_open)):
                        print(f"Error: Line number must be in range of 1/{self.get_file_length(self.file_open)}.")
                        return
                else:
                    print("Error: Line number must be an integer.")
                    return
            except IndexError:
                print("Error: Line number is not provided.")
                return
            
            # remove --line <line> - remove the specified line content.
            if len(args) == 3: # remove --line <line>
                self.remove_line(line)
            else:
                print("Error: Invalid syntax did you mean 'remove --line <line>'?")
        elif "-a" in args or "--all" in args:
            # remove --all - remove the entire file content.
            if len(args) == 2: # remove --all
                self.remove_all()
            else:
                print("Error: Invalid syntax did you mean 'remove --all'?")
        else:
            print("Error: Invalid syntax did you mean 'remove [--line <line> | --all]'?")
        self.last_line_modified = 1

    def run(self):
        """Main loop."""
        while True:
            try:
                if self.is_open:
                    user_input = input(f"{os.getcwd().replace("\\", "/")}/{self.file_open}[1/{self.get_file_length(self.file_open)}]: ")
                else:
                    user_input = input(f"{os.getcwd().replace("\\", "/")}: ")
    
                if not user_input:
                    continue

                # early check if the command is write (possibly) and if the content is enclosed double quotes.
                if user_input.startswith("write"):
                    content = self.parse_content(user_input)
                    if content == None:
                        continue
                    elif content:
                        # replace the content with an empty string to prevent it from being split, then replace it back with the actual content.
                        # the outcome will be, a list of arguments with the content enclosed with double quotes attaining the original content format.
                        user_input = user_input.replace(content, "\"\"").split()
                        user_input[user_input.index("\"\"")] = content
                    else:
                        user_input = user_input.split()
                else:
                    user_input = user_input.split()
            except KeyboardInterrupt:
                break
            
            if user_input[0] in ["read", "write", "clear", "remove", "undo", "redo"] and not self.is_open:
                print("Error: No opened file. Use 'open <file>' to open and edit a file.")

            # quit, help, undo, redo
            elif user_input[0] in ["q", "quit", "exit"]:
                if len(user_input) != 1:
                    print("Error: Invalid command. Did you mean 'q' or 'quit' or 'exit'?")
                else:
                    sys.exit(0)

            elif user_input[0] in ["h", "help", "?"]:
                if len(user_input) == 1:
                    self.help(None)
                elif len(user_input) == 2:
                    if user_input[1] in list(self.command_help.keys()):
                        self.help(user_input[1])
                    else:
                        print(f"Error: {user_input[1]} is not a valid command.")
                else:
                    print("Error: Invalid command. Did you mean 'h, help, ? [command]'?")

            elif user_input[0] == "close":
                if len(user_input) != 1:
                    print("Error: Invalid command. Did you mean 'close'?")
                elif not self.is_open:
                    print("Error: No file is open.")
                else:
                    self.close()
                    print("File closed.")

            elif user_input[0] == "undo":
                if len(user_input) != 1:
                    print("Error: Invalid command. Did you mean 'undo'?")
                if self.current_index <= 1:
                    pass
                else:
                    print("undo")
                    self.current_index -= 1
                    self.clear_all()
                    self.microfilesys_writelines(self.action_array[self.current_index - 1])

            elif user_input[0] == "redo":
                if len(user_input) != 1:
                    print("Error: Invalid command. Did you mean 'redo'?") 
                if self.current_index  >= len(self.action_array):
                    pass
                else:
                    print("redo")
                    self.current_index += 1
                    self.clear_all()
                    self.microfilesys_writelines(self.action_array[self.current_index - 1])

            # navigate through the filesystem
            elif user_input[0] == "ls":
                if len(user_input) == 1:
                    self.ls(os.getcwd())
                elif len(user_input) == 2:
                    self.ls(user_input[1])
                else:
                    print(f"Error: Invalid command. Did you mean 'ls [directory]'?")

            elif user_input[0] == "cd":
                if len(user_input) == 2:
                    self.cd(user_input[1])
                else:
                    print(f"Error: Invalid command. Did you mean 'cd <directory>'?")

            # create or delete files, directories, or paths
            elif user_input[0] == "make":
                if len(user_input) == 1:
                    print(self.command_help["make"])
                elif user_input[1] in ["-f", "--file"]:
                    if len(user_input) == 2:
                        print("Error: Invalid command. Did you mean 'make --file <filename>...'?")
                    else:
                        self.mkfile(user_input[2:])
                elif user_input[1] in ["-d", "--directory"]:
                    if len(user_input) == 2:
                        print("Error: Invalid command. Did you mean 'make --directory <filename>...'?")
                    else:
                        self.mkdir(user_input[2:])
                elif user_input[1] in ["-p", "--path"]:
                    if len(user_input) == 2:
                        print("Error: Invalid command. Did you mean 'make --path <filename>...'?")
                    else:
                        self.mkpath(user_input[2:])
                else:
                    print("Error: Invalid command. Did you mean 'make <--file | --directory | --path> <filename>...'?")

            elif user_input[0] == "delete":
                if len(user_input) == 1:
                    print(self.command_help["delete"])
                elif user_input[1] in ["-f", "--file"]:
                    if len(user_input) == 2:
                        print("Error: Invalid command. Did you mean 'delete --file <filename>...'?")
                    else:
                        self.rmfile(user_input[2:])
                elif user_input[1] in ["-d", "--directory"]:
                    if len(user_input) == 2:
                        print("Error: Invalid command. Did you mean 'delete --directory <filename>...'?")
                    else:
                        self.rmdir(user_input[2:])
                elif user_input[1] in ["-p", "--path"]:
                    if len(user_input) == 2:
                        print("Error: Invalid command. Did you mean 'delete --path <filename>...'?")
                    else:
                        self.rmpath(user_input[2:])
                else:
                    print("Error: Invalid command. Did you mean 'delete <--file | --directory | --path> <filename>...'?")

            elif user_input[0] == "open":
                if len(user_input) == 1:
                    print(self.command_help["open"])
                elif len(user_input) == 2:
                    if self.is_open:
                        print(f"Error: {self.file_open}  is already open, use 'close' to close the file and open a new one.")
                    elif self.open(user_input[1]):
                        print(f"File '{self.file_open}' opened.")
                else:
                    print("Error: Invalid command. Did you mean 'open <file>'?")
                    
            elif user_input[0] == "read":
                if len(user_input) == 1:
                    print(self.command_help["read"])
                else:
                    self.read_command(user_input)

            elif user_input[0] == "write":
                if len(user_input) == 1:
                    print(self.command_help["write"])
                else:
                    self.write_command(user_input)
                    self.update_action_array()

            elif user_input[0] == "clear":
                if len(user_input) == 1:
                    print(self.command_help["clear"])
                else:
                    self.clear_command(user_input)
                    self.update_action_array()

            elif user_input[0] == "remove":
                if len(user_input) == 1:
                    print(self.command_help["remove"])
                else:
                    self.remove_command(user_input)
                    self.update_action_array()

            else:
                print(f"Error: {user_input[0]} is not a valid command.")

            continue

if __name__ == "__main__":
    microfilesys().run()