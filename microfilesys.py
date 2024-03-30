

import os
import sys

class microfilesys:
    def __init__(self):
        self.is_open = False
        self.file_open = None

    def is_file(self, file_name):
        return not os.stat(f"{os.getcwd()}/{file_name}")[0] & 0x4000

    def is_folder(self, folder_name):
        return os.stat(f"{os.getcwd()}/{folder_name}")[0] & 0x4000

    def get_file_length(self, file_name):
        """
        Returns the line length of the file.
        """
        return len(self.get_file_content(file_name))

    def get_file_content(self, file_name):
        """
        Returns a list of contents of the file.
        """
        with open(file_name, 'r') as file:
            file_lines = file.readlines()

        # adds a newline character when reading a blank file.
        if not file_lines:
            file_lines.append('\n')

        return file_lines

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
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def read_line(self, file, line):
        with open(file, "r") as f:
            print(f.readlines())
        
    def read_line_indicator(self, file, line):
        with open(file, "r") as f:
            print("Line: Indicator on")
            print(f.readlines()[line - 1])

    def read_all(self, file):
        with open(file, "r") as f:
            print(f.read())
    
    def read_all_indicator(self, file):
        with open(file, "r") as f:
            print("All: Indicator on")
            print(f.read())

    def run(self):
        while True:
            try:
                if self.is_open:
                    user_input = input(f"{os.getcwd().replace("\\", "/")}/{self.file_open}[1/{self.get_file_length(self.file_open)}]: ")
                else:
                    user_input = input(f"{os.getcwd().replace("\\", "/")}: ")

                if not user_input:
                    continue

                user_input = user_input.split() # the write content needs to be split out, result will be in "".
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                return
            
            # quit, help, version, undo, redo
            if user_input in ["q", "quit", "exit"]:
                sys.exit(0)
            
            elif user_input in ["h", "help", "?"]:
                print("help")
                continue

            elif user_input in ["v", "version"]:
                print("version")
                continue

            elif user_input in ["undo"]:
                print("undo")
                continue

            elif user_input in ["redo"]:
                print("redo")
                continue

            # navigate through the filesystem
            if user_input[0] == "ls":
                if len(user_input) == 1:
                    self.ls(os.getcwd())
                elif len(user_input) == 2:
                    self.ls(user_input[1])
                else:
                    print(f"Error: expects 'ls [directory]'.")
                continue

            elif user_input[0] == "cd":
                if len(user_input) == 2:
                    self.cd(user_input[1])
                else:
                    print(f"Error: expects 'cd <directory>'.")
                continue

            # create or delete files, directories, or paths
            elif user_input[0] == "make":
                if len(user_input) == 1:
                    print("Error: expects 'make <--file | --directory | --path> <filename>'.")

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
                continue
                
            elif user_input[0] == "delete":
                if (len(user_input) == 1):
                    print("Error: expects 'delete <--file | --directory | --path> <filename>'.")

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
                continue

            elif user_input[0] == "open":
                if len(user_input) == 2:
                    if self.open(user_input[1]):
                        print(f"Opened {user_input[1]}")
                else:
                    print("Error: expects 'open <file>'.")
                continue

            # file read and write operations
            elif user_input[0] == "read": # done
                if not self.is_open:
                    print("Error: No file is open, use 'open <file>' to open and edit a file.")
                    continue
                if len(user_input) == 1:
                    print("Error: expects 'read [--line <line> | --all] [--indicator]'.")
                    continue
                if ("-l" in user_input and "--line" in user_input) or ("-a" in user_input and "--all" in user_input):
                    print("Error: same flag cant be used at the same time.")
                    continue
                if ("-l" in user_input or "--line" in user_input) and ("-a" in user_input or "--all" in user_input):
                    print("Error: --line and --all cant be used at the same time.")
                    continue

                if "--indicator" in user_input:
                    self.indicator_read = True

                if "-l" in user_input or "--line" in user_input:
                    arg_index = None
                    try:
                        arg_index = user_input.index("-l")
                    except ValueError:
                        arg_index = user_input.index("--line")

                    try:
                        line = int(user_input[arg_index + 1])

                        if line >= 1 and line <= self.get_file_length(self.file_open):
                            if self.indicator_read:
                                self.read_line_indicator(self.file_open, line)
                            else:
                                self.read_line(self.file_open, line)
                        else:
                            print(f"Error: line number must be in range of 1/{self.get_file_length(self.file_open)}.")
                    except ValueError:
                        print("Error: line number must be an integer.")
                    except IndexError:
                        print("Error: line number is not provided.")

                elif "-a" in user_input or "--all" in user_input:
                    arg_index = None
                    try:
                        arg_index = user_input.index("-a")
                    except ValueError:
                        arg_index = user_input.index("--all")
                    
                    if self.indicator_read:
                        self.read_all_indicator(self.file_open)
                    else:
                        self.read_all(self.file_open)
                continue

            elif user_input[0] == "write":
                if not self.is_open:
                    print("Error: No file is open, use 'open <file>' to open and edit a file.")
                    continue
                if len(user_input) == 1:
                    print("Error: expects 'write [--line <line> | --end [line] | --all] [string]'.")
                    continue
                if ("-l" in user_input and "--line" in user_input) or ("-e" in user_input and "--end" in user_input) or ("-a" in user_input and "--all" in user_input):
                    print("Error: same flag cant be used at the same time.")
                    continue
                if ("-l" in user_input or "--line" in user_input) and ("-e" in user_input or "--end" in user_input):
                    print("Error: --line and --end cant be used at the same time.")
                    continue
                if ("-l" in user_input or "--line" in user_input) and ("-a" in user_input or "--all" in user_input):
                    print("Error: --line and --all cant be used at the same time.")
                    continue
                if ("-e" in user_input or "--end" in user_input) and ("-a" in user_input or "--all" in user_input):
                    print("Error: --end and --all cant be used at the same time.")
                    continue
                if ("-l" in user_input or "--line" in user_input) and ("-e" in user_input or "--end" in user_input) and ("-a" in user_input or "--all" in user_input):
                    print("Error: --line, --end, and --all cant be used at the same time.")
                    continue
                
                if not (("-l" in user_input or "--line" in user_input) or ("-e" in user_input or "--end" in user_input) or ("-a" in user_input or "--all" in user_input)):
                    # write "string"
                    has_content = any(arg.startswith("\"") for arg in user_input)
                    if has_content:
                        print("write \"string\"")
                    else:
                        print("Error: did you mean 'write <\"string\">'.")

                if "-l" in user_input or "--line" in user_input:
                    arg_index = None
                    line = None
                    has_content = any(arg.startswith("\"") for arg in user_input)

                    try:
                        arg_index = user_input.index("-l")
                    except ValueError:
                        arg_index = user_input.index("--line")

                    try:
                        line = int(user_input[arg_index + 1])

                        if not (line >= 1 and line <= self.get_file_length(self.file_open)):
                            print(f"Error: line number must be in range of 1/{self.get_file_length(self.file_open)}.")
                        
                        else:
                            if has_content:
                                print("write [--line <line>] [\"string\"]")
                            else:
                                if len(user_input) < 4:
                                    print("write --line <line>")
                                else:
                                    print("Error: did you mean 'write [--line <line>] [\"string\"]'.")
                    except ValueError:
                        print("Error: line number must be an integer.")
                    except IndexError:
                        print("Error: line number is not provided.")

                elif "-e" in user_input or "--end" in user_input:
                    arg_index = None
                    line = None
                    has_content = any(arg.startswith("\"") for arg in user_input)

                    try:
                        arg_index = user_input.index("-e")
                    except ValueError:
                        arg_index = user_input.index("--end")
                    

                    # ==========================
                    if len(user_input) == 2:
                        # write --end
                        print(f"{user_input[0]} {user_input[1]}")
                        continue

                    elif len(user_input) == 3:
                        if not user_input[2].isdigit() and not has_content:
                            print("Error: line number must be an integer.")
                            continue
                            
                        if has_content:
                            # write --end "string" | write "string" --end
                            print(f"{user_input[0]} {user_input[1]} {user_input[2]}")
                        else:
                            # write --end 1
                            line = int(user_input[2])
                            print(f"{user_input[0]} {user_input[1]} {user_input[2]}")


                    elif len(user_input) == 4:
                        # write --end 1 "string"
                        if user_input[arg_index + 1].isdigit():
                            line = int(user_input[arg_index + 1])
                            if not (line >= 1 and line <= self.get_file_length(self.file_open)):
                                print(f"Error: line number must be in range of 1/{self.get_file_length(self.file_open)}.")
                            else:
                                if has_content:
                                    # write --end 1 "string" | write "string" --end 1
                                    print(f"{user_input[0]} {user_input[1]} {user_input[2]} {user_input[3]}")
                                else:
                                    print("Error: did you mean 'write --end <line> \"string\"'.")
                        else:
                            print("Error: line number must be an integer.")
                    else:
                        print("Error: expects 'write [--end [line]] [\"string\"]'.")
                    continue
                
                elif "-a" in user_input or "--all" in user_input:
                    has_content = any(arg.startswith("\"") for arg in user_input)
                    if len(user_input) == 2:
                        # write --all
                        print(f"{user_input[0]} {user_input[1]}")
                    elif len(user_input) == 3:
                        if has_content:
                            # write --all "string" | write "string" --all
                            print(f"{user_input[0]} {user_input[1]} {user_input[2]}")
                        else:
                            print("Error: did you mean 'write [--all] [\"string\"]'.")
                    else:
                        print("Error: expects 'write [--all] [\"string\"]'.")
                else:
                    print("Error: expects 'write [--line <line> | --end [line] | --all] [string]'.")

                    # add and finish error conditions

                    # line number and content is provided.
                    # write "string" /

                    # write --line 1 /
                    # write --line 1 "string" /
                    # write "string" --line 1 /

                    # write --end /
                    # write --end "string" /
                    # write --end 1 "string" /
                    # write "string" --end /
                    # write "string" --end 1 /

                    # write --all /
                    # write --all "string" /
                    # write "string" --all /

            elif user_input[0] == "clear":
                if not self.is_open:
                    print("Error: No file is open, use 'open <file>' to open and edit a file.")
                    continue
                if len(user_input) == 1:
                    print("Error: expects 'clear [--line <line> | --all]'.")
                
            elif user_input[0] == "remove":
                if not self.is_open:
                    print("Error: No file is open, use 'open <file>' to open and edit a file.")
                    continue
                if len(user_input) == 1:
                    print("Error: expects 'remove [--line <line> | --all]'.")
                

microfilesys().run()

"""
ls [directory]
cd <directory>
open <file>
make <--file | --directory | --path> <filename>
delete <--file | --directory | --path> <filename>

read [<--line <line> | --all>] [--indicator]
write [<--line <line> | --end [line] | --all>] [string]
clear <--line <line> | --all>
remove <--line <line> | --all>

q quit exit
h help ?
v version

undo
redo
"""