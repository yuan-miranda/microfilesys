import os

# NOTE TO CHANGE
# convert self.line to int 11/16
#   writeend()
#   line not number error
#   get_content to just auto deetect not index specified

# TODO FIX:
# writeend() having double quotes on content

# return a string literal of the content in the specific location
def get_content(command_parts, content_index):
    return ' '.join(command_parts[content_index:])[1:-1]

# check if the input is a content
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

        self.command            = None
        self.option             = None
        self.content            = None

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
        def write_to_specific_line(file_path, line_number, new_content):
        # Read the existing content of the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Modify the desired line
        if 1 <= line_number <= len(lines):
            lines[line_number - 1] = new_content + '\n'  # Adjusting for 0-based indexing

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.writelines(lines)
        else:
            print(f"Line number {line_number} is out of range.")

    def writeend(self):
        with open(self.open_file, 'r+') as file:
                lines = file.readlines()
                self.line = int(self.line)
                
                # check if input line is in range of file lines
                if self.line > 0 and self.line <= len(lines):

                    # write at the end of the line using this
                    lines[self.line - 1] = lines[self.line - 1].rstrip('\n') + get_content(self.command_parts, 3) + '\n'
                    file.seek(0)
                    file.writelines(lines)

                else:
                    print(f"line must be in range of 1 to {len(lines)}")

    def clearline(self):
        pass
    def clearall(self):
        pass

    def create(self):
        pass
    def open(self):
        pass
    def delete(self):
        pass

    def handle_read_command(self):
        # option -l
        if self.option in self.option_keywords['line']:
            if self.length == 2:
                print(f"expexted line number after {self.option}")
            elif self.length == 3:
                if self.line and self.line.isdigit():
                    self.readline() # call read line function
                else:
                    print("line not number")
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
                if self.line and self.line.isdigit():
                    print(f"expected content after line: {self.command_join} \"example content\"")
                else:
                    print("line not number")
                    
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
                if self.line and self.line.isdigit():
                    print(f"expected content after line: {self.command_join} \"example content\"")
                else:
                    print("line not number")
            elif self.length >= 4:
                if is_content(self.command_parts, 3):
                    print(get_content(self.command_parts, 3))
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
                if self.line and self.line.isdigit():
                    print("line")
                    self.clearline() # call clear line function
                else:
                    print("line not number")
            else:
                print("invalid line length")

        # option -a
        elif self.option in self.option_keywords['all']:
            if self.length == 2:
                print("all")
                self.clearall() # call clear all function
            else:
                print("invalid all length")
        else:
            print(f"{self.option} is not a valid option")

    def handle_create_command(self):
        if is_file(self.current_file):
            print(f"'{self.current_file}' already exist")

        else:
            with open(self.current_file, "w") as file:
                print(f"'{self.current_file}' created successfully")

    def handle_open_command(self):
        if not is_file(self.current_file):
            print(f"'{self.current_file}' doesnt exist")

        else:
            self.open_file = self.current_file
            self.status = self.file_operator_mode

    def handle_delete_command(self):
        if not is_file(self.current_file):
            print(f"'{self.current_file}' doesnt exist")
        
        else:
            os.remove(self.current_file)
            print(f"'{self.current_file}' deleted successfully")

    def start_microfilesys(self):
        running = True
        while running:
            try:
                command_input = input(f"microfilesys-{self.open_file}: " if self.open_file else "microfilesys: ")
                
                # quit keywords, same operation as the 'except KeyboardInterrupt' below
                if command_input in ['q', 'quit', 'exit']:
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
                
            
            if not command_input:
                continue

            # initialize all the variable
            self.command_parts  = command_input.split()
            self.command_join   = ' '.join(self.command_parts)
            self.length         = len(self.command_parts)
        
            self.command        = self.command_parts[0]
            self.option         = self.command_parts[1] if self.length >= 2 else None
            self.content        = self.command_parts[3] if self.length >= 4 else None
            self.line           = self.command_parts[2] if self.length >= 3 else None
            
            self.current_file   = self.command_parts[1] if self.length == 2 else None

            # if no files are open but is using file editor command
            if self.command in self.file_opetator_command_handlers:
                if self.status == self.file_operator_mode:
                    if self.option:
                        self.file_opetator_command_handlers[self.command]()
                    else:
                        print("expected an option")
                else:
                    print("status is currently in file manager, open a file first")

            # check if is using file manager command
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