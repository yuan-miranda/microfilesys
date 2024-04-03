version = "v.0.4.3"

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

    def is_file(self, file_name):
        return not os.stat(f"{os.getcwd()}/{file_name}")[0] & 0x4000

    def is_folder(self, folder_name):
        return os.stat(f"{os.getcwd()}/{folder_name}")[0] & 0x4000

    def get_file_length(self, file_name):
        return len(self.get_file_content(file_name))

    def get_file_content(self, file_name):
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
        total_lines = self.get_file_length(self.file_open)
        return 1 <= line_number <= total_lines

    def update_action_array(self):
        if self.current_index != len(self.action_array):
            self.action_array = self.action_array[:self.current_index + 1]
            self.current_index = len(self.action_array)
        else:
            self.current_index += 1
            self.action_array.append(self.get_file_content(self.file_open))

    def parse_content(self, raw_input):
        # this finds the first and last occurance of '"' in the string.
        # you can input as many quotes as you want and it will still be valid.
        # '"' is used to enclose the content.
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

    def help(self):
        print("""
ls [directory]
cd <directory>
open <file>
make <--file | --directory | --path> <filename>
delete <--file | --directory | --path> <filename>

read [--line <line> | --all] [--indicator]
write [--line <line> | --end [line] | --all] ["string"]
clear <--line <line> | --all>
remove <--line <line> | --all>

q quit exit
h help ?
v version
close

undo
redo
""")

    def ls(self, path):
        try:
            content = os.listdir(path)
            for item in content:
                print(item)
        except Exception as e:
            print(f"Error: {e}")

    def cd(self, directory):
        try:
            os.chdir(directory)
        except Exception as e:
            print(f"Error: {e}")

    def mkdir(self, folders):
        for folder in folders:
            try:
                os.mkdir(folder)
            except Exception as e:
                print(f"Error: {e}")

    def rmdir(self, folders):
        for folder in folders:
            try:
                os.rmdir(folder)
            except Exception as e:
                print(f"Error: {e}")

    def mkfile(self, files):
        for file in files:
            try:
                with open(file, "w") as f:
                    pass
            except Exception as e:
                print(f"Error: {e}")

    def rmfile(self, files):
        for file in files:
            try:
                os.remove(file)
            except Exception as e:
                print(f"Error: {e}")


    def mkpath(self, paths):
        for path in paths:
            try:
                os.makedirs(path)
            except Exception as e:
                print(f"Error: {e}")

    def rmpath(self, paths):
        """Recursively removes the specified directory. Based on Roberthh's implementation: https://forum.micropython.org/viewtopic.php?t=7512#p42783."""
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
        self.is_open = False
        self.file_open = None
        self.current_index = 0
        self.action_array = []

    def read_line(self, line_number):
        file_lines = self.get_file_content(self.file_open)
        line_content = file_lines[line_number - 1].rstrip('\n')
        print(line_content)

    def read_line_indicator(self, line_number):
        file_lines = self.get_file_content(self.file_open)
        line_content = file_lines[line_number - 1].rstrip('\n')
        line_number = self.microfilesys_rjust(str(line_number), 4)

        print(f"{line_number}| {line_content}")
    
    def read_all(self):
        with open(self.file_open, 'r') as file:
            for line in file:
                print(line.rstrip("\n"))

    def read_all_indicator(self):
        file_lines = self.get_file_content(self.file_open)
        for line_number, line_content in enumerate(file_lines, 1):
            line_number = self.microfilesys_rjust(str(line_number), 4)
            print(f"{line_number}| {line_content.rstrip('\n')}")

    def write_line(self, line_number, content):
        file_lines = self.get_file_content(self.file_open)
        while len(file_lines) < line_number:
            file_lines.append('\n')

        file_lines[line_number - 1] = content + '\n'
        self.microfilesys_writelines(file_lines)

    def write_end(self, line_number, content):
        file_lines = self.get_file_content(self.file_open)
        file_lines[line_number - 1] = file_lines[line_number - 1].rstrip('\n') + content + '\n'
        self.microfilesys_writelines(file_lines)

    def clear_line(self, line_number):
        file_lines = self.get_file_content(self.file_open)
        file_lines[line_number - 1] = '\n'
        self.microfilesys_writelines(file_lines)

    def clear_all(self):
        file_lines = self.get_file_content(self.file_open)
        file_lines = ['\n'] * len(file_lines)
        self.microfilesys_writelines(file_lines)

    def remove_line(self, line_number):
        file_lines = self.get_file_content(self.file_open)
        file_lines.pop(line_number - 1)
        self.microfilesys_writelines(file_lines)

    def remove_all(self):
        with open(self.file_open, 'w') as file:
            file.write('')

    def read_command(self, args):
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
                        print(f"Error: line number must be in range of 1/{self.get_file_length(self.file_open)}.")
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
                print("Error: Invalid syntax did you mean 'write --line <line> \"string\"'.")

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
                print("Error: No file is open, use 'open <file>' to open and edit a file.")

            # quit, help, version, undo, redo
            elif user_input[0] in ["q", "quit", "exit"]:
                if len(user_input) != 1:
                    print("Error: expects 'q' or 'quit' or 'exit'.")
                else:
                    sys.exit(0)

            elif user_input[0] in ["h", "help", "?"]:
                if len(user_input) != 1:
                    print("Error: expects 'h' or 'help' or '?'")
                else:
                    self.help()

            elif user_input[0] in ["v", "version"]:
                if len(user_input) != 1:
                    print("Error: expects 'v' or 'version'.")
                else:
                    print(f"microfilesys.py {version}")

            elif user_input[0] == "close":
                if len(user_input) != 1:
                    print("Error: expects 'close'.")
                elif not self.is_open:
                    print("Error: No file is open.")
                else:
                    self.close()
                    print("File closed.")

            elif user_input[0] == "undo":
                if len(user_input) != 1:
                    print("Error: expects 'undo'.")

                if self.current_index <= 1:
                    pass
                else:
                    print("undo")
                    self.current_index -= 1
                    self.clear_all()
                    self.microfilesys_writelines(self.action_array[self.current_index - 1])

            elif user_input[0] == "redo":
                if len(user_input) != 1:
                    print("Error: expects 'redo'.") 

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
                    print(f"Error: expects 'ls [directory]'.")

            elif user_input[0] == "cd":
                if len(user_input) == 2:
                    self.cd(user_input[1])
                else:
                    print(f"Error: expects 'cd <directory>'.")

            # create or delete files, directories, or paths
            elif user_input[0] == "make":
                if len(user_input) == 1:
                    print("Usage: make <--file | --directory | --path> <filename>")
                    print("Flags: --file\t\tCreate a file")
                    print("       --directory\tCreate a directory")
                    print("       --path\t\tCreate a path")
                    print("Ex:    make --file file.txt")

                elif user_input[1] in ["-f", "--file"]:
                    if len(user_input) == 2:
                        print("Error: expects 'make --file <filename>'.")
                    else:
                        self.mkfile(user_input[2:])

                elif user_input[1] in ["-d", "--directory"]:
                    if len(user_input) == 2:
                        print("Error: expects 'make --directory <filename>'.")
                    else:
                        self.mkdir(user_input[2:])

                elif user_input[1] in ["-p", "--path"]:
                    if len(user_input) == 2:
                        print("Error: expects 'make --path <filename>'.")
                    else:
                        self.mkpath(user_input[2:])

            elif user_input[0] == "delete":
                if len(user_input) == 1:
                    print("Usage: delete <--file | --directory | --path> <filename>")
                    print("Flags: --file\t\tDelete a file")
                    print("       --directory\tDelete a directory")
                    print("       --path\t\tDelete a path")
                    print("Ex:    delete --file file.txt")

                elif user_input[1] in ["-f", "--file"]:
                    if len(user_input) == 2:
                        print("Error: expects 'delete --file <filename>'.")
                    else:
                        self.rmfile(user_input[2:])

                elif user_input[1] in ["-d", "--directory"]:
                    if len(user_input) == 2:
                        print("Error: expects 'delete --directory <filename>'.")
                    else:
                        self.rmdir(user_input[2:])

                elif user_input[1] in ["-p", "--path"]:
                    if len(user_input) == 2:
                        print("Error: expects 'delete --path <filename>'.")
                    else:
                        self.rmpath(user_input[2:])

            elif user_input[0] == "open":
                if len(user_input) == 1:
                    print("Usage: open <file>")
                    print("Ex:    open file.txt")

                elif len(user_input) == 2:
                    if self.is_open:
                        print(f"Error: {self.file_open}  is already open, use 'close' to close the file and open a new one.")
                    elif self.open(user_input[1]):
                        print(f"File '{self.file_open}' opened.")
                else:
                    print("Error: expects 'open <file>'.")
                    
            elif user_input[0] == "read":
                if len(user_input) == 1:
                    print("Usage: read [--line <line> | --all] [--indicator]")
                    print("Flags: --line <line>\tLine to read")
                    print("       --all\t\tRead all lines")
                    print("       --indicator\tDisplay line number")
                    print("Ex:    read --line 1")
                else:
                    self.read_command(user_input)

            elif user_input[0] == "write":
                if len(user_input) == 1:
                    print("Usage: write [--line <line> | --end [line] | --all] [\"string\"]")
                    print("Flags: --line <line>\tLine to write")
                    print("       --end [line]\tWrite at the end of the line")
                    print("       --all\t\tReplace all lines with the string")
                    print("Ex:    write --line 1 \"Hello, World!\"")
                else:
                    self.write_command(user_input)
                    self.update_action_array()

            elif user_input[0] == "clear":
                if len(user_input) == 1:
                    print("Usage: clear <--line <line> | --all>")
                    print("Flags: --line <line>\tClear the line content")
                    print("       --all\t\tClear all file content")
                    print("Ex:    clear --line 1")
                else:
                    self.clear_command(user_input)
                    self.update_action_array()

            elif user_input[0] == "remove":
                if len(user_input) == 1:
                    print("Usage: remove <--line <line> | --all>")
                    print("Flags: --line <line>\tRemove the line")
                    print("       --all\t\tRemove all file lines")
                    print("Ex:    remove --line 1")
                else:
                    self.remove_command(user_input)
                    self.update_action_array()
            else:
                print(f"Error: {user_input[0]} is not a valid command.")

            continue

microfilesys().run()