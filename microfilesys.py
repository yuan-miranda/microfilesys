# Micropython.py v.0.2.8
# last update: 11/21/23

import os

# return true when the list only contain a pair of double quotes. Used to validate get_content().
def is_content(command_parts, content_index):
    string = ' '.join(command_parts[content_index:]) 
    content_start = string[0]
    content_end = string[-1]

    # if content has more/less than double quotes or does have pair of "" but isn't enclosed by it.
    if string.count('"') != 2 or (string.count('"') == 2 and content_start != '"' or content_end != '"'):
        print(f"invalid content format: {string}")
        return False
    
    # prevent: a", a"", '"a"'
    if content_start != '"':
        print(f"missing \" on the start of the content: {string}")
        return False
    
    # prevent: "a, ""a, '"a"'
    if content_end != '"':
        print(f"missing \" on the end of the content: {string}")
        return False
    
    return True

# parse the first string that is enclosed with double quotes i.e. "sometxt"
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

# check if the file exist in the directory
def is_file(file_name):
    return file_name in os.listdir()

# returns the file length of the specified file.
def file_length(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

        if not lines:
            return len(lines) + 1

        return len(lines)

# made a function of this to check if length is 2 and is invalid line
def is_line(length, option, line):
    if length == 2:
        print(f"expected line argument after {option}")
        return False
        
    if not line or not line.isdigit():
        print(f"line argument '{line}' is not a number")
        return False
            
    return True

class Microfilesys:
    def __init__(self):
        # commadn handlers
        self.file_editor_command_handlers = {
            'read' : self.read_command_handler,
            'write': self.write_command_handler,
            'clear': self.clear_command_handler
        }
        self.file_manager_command_handlers = {
            'create': self.create_command_handler,
            'open'  : self.open_command_handler,
            'delete': self.delete_command_handler
        }
        self.option_keywords = {
            'line': ['-l', '--line'],
            'all' : ['-a', '--all'],
            'end' : ['-e', '--end']
        }
        self.expected_command_error = {
            'read'  : "expected 'read <-l line=int | -a>'",
            'write' : "expected 'write <-l | -e> <line=int content=\"sting\">'",
            'clear' : "expected 'clear <-l line=int | -e>",
            'create': "expected 'create <file>",
            'open'  : "expected 'open <file>",
            'delete': "expected 'delete <file>"
        }

        # file related variables
        self.file_editor_mode   = "file editor"
        self.file_manager_mode  = "file manager"
        self.status             = self.file_manager_mode
        self.current_open_file  = None
        self.current_file       = None

        # command measurements
        self.user_input     = None
        self.command_parts  = None
        self.command_join   = None
        self.length         = None

        # command arguments
        self.command = None
        self.option  = None
        self.line    = None
        self.content = None

    def create_file(self, file_name):
        if is_file(file_name):
            with open(file_name, 'w') as file:
                print(f"'{file_name}' created successfully")

    def open_file(self, file_name):
        self.current_open_file = file_name
        self.status = self.file_editor_mode

    def delete_file(self, file_name):
        os.remove(file_name)
        print(f"'{file_name}' deleted successfully")
    

    def readline(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()
        
        # handle the case where a line is empty (that line would not be stored in the list).
        if not lines:
            lines.append('\n')

        if self.line >= 1 and self.line <= len(lines):
            # get the specified line to read and print
            line_content = lines[int(self.line) - 1].rstrip('\n')
            print(line_content)
            
        else:
            print(f"line must be in range of 1 to {len(lines)}")
    
    def readall(self, file_name):
        # read all the file content
        with open(file_name, 'r') as file:
            print(file.read())

    def writeline(self, file_name):
        # read the entire file content
        with open(file_name, 'r') as file:
            lines = file.readlines()
    
        # extend the file length when the user wants to write beyond the current length.
        while self.line > len(lines):
            lines.append('\n')
    
        # update the line with the new content
        lines[self.line - 1] = get_content(self.user_input)[3] + '\n'

        with open(file_name, 'w') as file:
            file.writelines(lines)
        
    def writeend(self, file_name):
        with open(file_name, 'r+') as file:
            lines = file.readlines()

            # handle the case where a line is empty (that line would not be stored in the list).
            if not lines:
                lines.append('\n')
    
            # check if input line is in range of file lines
            if self.line >= 1 and self.line <= len(lines):

                # write at the end of the line
                lines[self.line - 1] = lines[self.line - 1].rstrip('\n') + get_content(self.user_input)[3] + '\n'
                file.seek(0)
                file.writelines(lines)

            else:
                print(f"line must be in range of 1 to {len(lines)}")

    def clearline(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()
        
        # extend the file length when the user wants to write beyond the current length.
        if not lines:
            lines.append('\n')

        # check if input line is in range of file lines
        if self.line >= 1 and self.line <= len(lines):
            # remove the content of the specified line
            lines[self.line - 1] = '' + '\n'

            with open(file_name, 'w') as file:
                file.writelines(lines)

        else:
            print(f"line must be in range of 1 to {len(lines)}")

    def clearall(self, file_name):
        # remove the entire file content, originally I tried to use delete_file() and create_file() lol.
        with open(file_name, 'w') as file:
            file.writelines([])

    # All of the handlers below are responsible for common errors and checking expected arguments
    # before calling the command functions.

    def read_command_handler(self):
        # option -l
        if self.option in self.option_keywords['line']:
            if not is_line(self.length, self.option, self.line):
                return
            
            self.line = int(self.line)
            
            if self.length == 3:
                self.readline(self.current_open_file) # call read line function
            else:
                print(f"invalid length, expected: 'read -l {self.line}'")

        # option -a
        elif self.option in self.option_keywords['all']:
            if self.length == 2:
                self.readall(self.current_open_file) # call read all function
            else:
                print(f"invalid length, expected: 'read -a'")
        else:
            print(f"{self.option} is not a valid option")
            
    def write_command_handler(self):
        # option -l
        if self.option in self.option_keywords['line']:
            if not is_line(self.length, self.option, self.line):
                return
            
            self.line = int(self.line)
            
            if self.length >= 4:
                if is_content(self.command_parts, 3):
                    self.writeline(self.current_open_file) # call write line function
            else:
                print(f"expected content after line: {self.command_join} \"example content\"")

        # option -end
        elif self.option in self.option_keywords['end']:
            if not is_line(self.length, self.option, self.line):
                return
            
            self.line = int(self.line)
            
            if self.length >= 4:
                if is_content(self.command_parts, 3):
                    self.writeend(self.current_open_file) # call write end function
            else:
                print(f"expected content after line: {self.command_join} \"example content\"")
        else:
            print(f"{self.option} is not a valid option")
            
    def clear_command_handler(self):
        # option -l
        if self.option in self.option_keywords['line']:
            if not is_line(self.length, self.option, self.line):
                return
            
            self.line = int(self.line)
            
            if self.length == 3:
                self.clearline(self.current_open_file) # call clear line function
            else:
                print(f"invalid length, expected: 'clear -l {self.line}'")

        # option -a
        elif self.option in self.option_keywords['all']:
            if self.length == 2:
                self.clearall(self.current_open_file) # call clear all function
            else:
                print(f"invalid length, expected: 'clear -a'")
        else:
            print(f"{self.option} is not a valid option")

    # this is just a redirect handler because the validation had already been done in start_microfilesys().
    def create_command_handler(self):
        self.create_file(self.current_file)
    def open_command_handler(self):
        self.open_file(self.current_file)
    def delete_command_handler(self):
        self.delete_file(self.current_file)

    # initialize all the variables needed
    def init_params(self):
        self.command_parts  = self.user_input.split()
        self.command_join   = ' '.join(self.command_parts)
        self.length         = len(self.command_parts) # base 0 indexing
        self.command        = self.command_parts[0]
        self.option         = self.command_parts[1] if self.length >= 2 else None
        self.content        = self.command_parts[3] if self.length >= 4 else None
        self.line           = self.command_parts[2] if self.length >= 3 else None
        self.current_file   = self.command_parts[1] if self.length == 2 else None
    
    # main program loop.
    def start_microfilesys(self):
        while True:
            try:
                # take the user input
                self.user_input = input(f"microfilesys-{self.current_open_file}[1/{file_length(self.current_open_file)}]: " if self.current_open_file else "microfilesys: ")
            except KeyboardInterrupt:
                # end the program when its set to file manager mode.
                if self.status == self.file_manager_mode:
                    return

                # prevent exiting the program when in file editor mode, just go back to file manager.
                print()
                self.current_open_file = None
                self.status = self.file_manager_mode
                continue   
            
            if not self.user_input:
                continue

            # quit keywords, same operation with 'except KeyboardInterrupt', just for quit input.
            if self.user_input in ['q', 'quit', 'exit']:
                if self.status == self.file_manager_mode:
                    return                
                
                self.current_open_file = None
                self.status = self.file_manager_mode
                continue

            self.init_params()

            # check if the command is invalid, I used 'self.expected_command_error' because its the only
            # dict with all of my commands together.
            
            if self.command not in self.expected_command_error:
                print(f"invalid command, '{self.command}' is not recognized as valid commmand.")
                continue
            
            # prepare the error of the command beforehand.
            expected_command = self.expected_command_error[self.command]

            # file operator command section
            if self.command in self.file_editor_command_handlers:
                if self.status != self.file_editor_mode:
                    print("status is currently in file manager, open a file first by typing 'open <file>'.")
                    continue

                if not self.option:
                    print(f"expected an option after '{self.command}'")
                    continue
                
                self.file_editor_command_handlers[self.command]()

            # file manager command section
            elif self.command in self.file_manager_command_handlers:
                if self.status != self.file_manager_mode:
                    print("status is currently in file editor, exit the mode first by entering 'q'.")
                    continue

                if not self.current_file:
                    print(f"invalid command syntax, {expected_command}")
                    continue
                    
                # Added 'create' command on the condition to prevent this error from executing when
                # the file argument of 'create' doesnt exist
                if self.command != 'create' and not is_file(self.current_file):
                    print(f"'{self.current_file}' doesnt exist in '{os.getcwd()}'")
                    continue

                self.file_manager_command_handlers[self.command]()

if __name__ == "__main__":
    mfs = Microfilesys()
    mfs.start_microfilesys()