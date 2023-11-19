import os

# NOTE TO CHANGE
#   convert self.line to int 11/16 FIX
#   writeend() FIX
#   line not number error FIX
#   get_content to just auto deetect not index specified FIX

# TODO FIX:
# writeend() having double quotes on content FIX
# fix the indexing issue with writeline() and writeend() FIX
# check if the input is a content FIX
# make line int FIX

def is_content(command_parts, content_index):
    string = ' '.join(command_parts[content_index:]) 
    content_start = string[0]
    content_end = string[-1]

    # prevent: a", a"", '"a"'
    if content_start != '"' and string.count('"') != 2:
        print(f"missing \" on the start of the content: {string}")
        return False
    
    # prevent: "a, ""a, '"a"'
    if content_end != '"' and string.count('"') != 2:
        print(f"missing \" on the end of the content: {string}")
        return False
    
    # if the content has more or less than double quotes on it
    if string.count('"') != 2:
        print(f"invalid content format: {string}")
        return False
    
    return True

def get_content(input_string):
    result = []
    current_word = ''
    inside_quotes = False

    for char in input_string:
        if char == ' ' and not inside_quotes:
            # Split at space only if not inside quotes
            result.append(current_word)
            current_word = ''
        elif char == '"':
            # Toggle the inside_quotes flag when a double quote is encountered
            inside_quotes = not inside_quotes
        else:
            current_word += char

    # Add the last word after the loop
    result.append(current_word)

    return result

def is_file(filename):
    return filename in os.listdir()

def file_length(filename):
    """
    returns the file length of the specified file.
    """
    with open(filename, 'r') as file:
        return len(file.readlines())
    
# Blessed are thy people who will read this code in the future.
class Microfilesys:
    def __init__(self):
        self.command_parts  = None
        self.command_join   = None
        self.length         = None

        self.file_opetator_command_handlers = {
            'read' : self.handle_read_command,
            'write': self.handle_write_command,
            'clear': self.handle_clear_command
        }
        self.file_manager_command_handlers = {
            'create': self.handle_create_command,
            'open': self.handle_open_command,
            'delete': self.handle_delete_command
        }
        self.option_keywords = {
            'line': ['-l', '--line'],
            'all': ['-a', '--all'],
            'end': ['-e', '--end']
        }

        self.file_operator_mode  = "file operator"
        self.file_manager_mode   = "file manager"
        self.status             = self.file_manager_mode

        self.command_input      = None
        self.command            = None
        self.option             = None
        self.content            = None

        self.mute_log           = False
        self.open_file          = None
        self.current_file       = None
        self.line               = None

    def readline(self):
        """
        read a single line on the file and print it.
        """
        with open(self.open_file, 'r') as file:
            try:
                # read specified line
                print('\n' +  file.readlines()[int(self.line) - 1].rstrip('\n') + '\n')

            # if the input line is not in range of file lines
            except IndexError:
                print(f"IndexError: '{self.open_file}' is only {file_length(self.open_file)} lines long not {self.line}.")

    def readall(self):
        with open(self.open_file, 'r') as file:
            # read whole file
            print('\n' + file.read() + '\n')
    
    def writeline(self):
        # read the entire file content
        with open(self.open_file, 'r') as file:
            lines = file.readlines()
    
        # handle the case where a line is empty (that line would not be stored in the list).
        while self.line > len(lines):
            lines.append('\n')
    
        # update the line with the new content
        lines[self.line - 1] = get_content(self.command_input)[3] + '\n'

        # write the modified line
        with open(self.open_file, 'w') as file:
            file.writelines(lines)

    def writeend(self):
        with open(self.open_file, 'r+') as file:
            lines = file.readlines()
            
            # check if input line is in range of file lines
            if self.line >= 1 and self.line <= len(lines):

                # write at the end of the line using this
                lines[self.line - 1] = lines[self.line - 1].rstrip('\n') + get_content(self.command_input)[3] + '\n'
                file.seek(0)
                file.writelines(lines)
            else:
                print(f"line must be in range of 1 to {len(lines)}")

    def clearline(self):
        with open(self.open_file, 'r') as file:
            lines = file.readlines()
        
        if self.line >= 1 and self.line <= len(lines):
            lines[self.line - 1] = '' + '\n'
            with open(self.open_file, 'w') as file:
                file.writelines(lines)

        else:
            print(f"line must be in range of 1 to {len(lines)}")

    def clearall(self):
        # lol
        self.mute_log = True
        self.delete(self.open_file)
        self.create(self.open_file)
        self.mute_log = False

    def create(self, filename):
        if is_file(filename):
            print(f"'{filename}' already exist")

        else:
            with open(filename, "w") as file:
                if not self.mute_log:
                    print(f"'{filename}' created successfully")
                else:
                    pass

    def open(self):
        pass
    def delete(self, filename):
        if not is_file(filename):
            print(f"'{filename}' doesnt exist")
        
        else:
            os.remove(filename)
            if not self.mute_log:
                print(f"'{filename}' deleted successfully")
            else:
                pass

    def handle_read_command(self):
        # option -l
        if self.option in self.option_keywords['line']:
            if self.length == 2:
                print(f"expexted line number after {self.option}")
            elif self.length == 3:
                self.readline() # call read line function
            else:
                print("invalid line length")

        # option -a
        elif self.option in self.option_keywords['all']:
            if self.length == 2:
                self.readall() # call read all function
            else:
                print("invalid all length")
        else:
            print(f"{self.option} is not a valid option")

    def handle_write_command(self):
        # option -l
        if self.option in self.option_keywords['line']:
            if self.length == 2:
                print(f"expexted line number after {self.option}")
            elif self.length == 3:
                print(f"expected content after line: {self.command_join} \"example content\"")
            elif self.length >= 4:
                if is_content(self.command_parts, 3):
                    self.writeline() # call write line function
            else:
                print("invalid line length")

        # option -end
        elif self.option in self.option_keywords['end']:
            if self.length == 2:
                print(f"expexted line number after {self.option}")
            elif self.length == 3:
                print(f"expected content after line: {self.command_join} \"example content\"")
            elif self.length >= 4:
                if is_content(self.command_parts, 3):
                    self.writeend() # call write end function
            else:
                print("invalid line length")
        else:
            print(f"{self.option} is not a valid option")

    def handle_clear_command(self):
        # option -l
        if self.option in self.option_keywords['line']:
            if self.length == 2:
                print(f"expexted line number after {self.option}")
            elif self.length == 3:
                self.clearline() # call clear line function
            else:
                print("invalid line length")

        # option -a
        elif self.option in self.option_keywords['all']:
            if self.length == 2:
                self.clearall() # call clear all function
            else:
                print("invalid all length")
        else:
            print(f"{self.option} is not a valid option")

    def handle_create_command(self):
        self.create(self.current_file)

    def handle_open_command(self):
        if not is_file(self.current_file):
            print(f"'{self.current_file}' doesnt exist")

        else:
            self.open_file = self.current_file
            self.status = self.file_operator_mode

    def handle_delete_command(self):
        self.delete(self.current_file)

    def start_microfilesys(self):
        running = True
        while running:
            try:
                self.command_input = input(f"microfilesys-{self.open_file}: " if self.open_file else "microfilesys: ")
                
                # quit keywords, same operation as the 'except KeyboardInterrupt' below
                if self.command_input in ['q', 'quit', 'exit']:
                    # make sure the program wont exit if in file operator mode and just go back into file manager mode.
                    if self.status == self.file_operator_mode:
                        self.open_file = None
                        self.status = self.file_manager_mode
                        continue
                    return
                
            except KeyboardInterrupt:
                if self.status == self.file_operator_mode:
                    print()
                    self.open_file = None
                    self.status = self.file_manager_mode
                    continue            
                return
                
            
            if not self.command_input:
                continue
            # initialize all the variable
            self.command_parts  = self.command_input.split()
            self.command_join   = ' '.join(self.command_parts)
            self.length         = len(self.command_parts)
        
            self.command        = self.command_parts[0]
            self.option         = self.command_parts[1] if self.length >= 2 else None
            self.content        = self.command_parts[3] if self.length >= 4 else None
            self.line           = self.command_parts[2] if self.length >= 3 else None
            
            self.current_file   = self.command_parts[1] if self.length == 2 else None

            # file operator command
            if self.command in self.file_opetator_command_handlers:
                if self.status == self.file_operator_mode:
                    if self.option:
                        if self.line and self.line.isdigit():
                            self.line = int(self.line)
                            self.file_opetator_command_handlers[self.command]()
                        else:
                            print("line not number")
                    else:
                        print("expected an option")
                else:
                    print("status is currently in file manager, open a file first")

            # file manager command
            elif self.command in self.file_manager_command_handlers:
                if self.status == self.file_manager_mode:
                    if self.current_file:
                        self.file_manager_command_handlers[self.command]()
                    else:
                        print("empty file name")
                else:
                    print("status is currently in file editor")
            else:
                print("invalid command")

parser = Microfilesys()
parser.start_microfilesys()