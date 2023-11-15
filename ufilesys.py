import os

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

# Blessed are thy people who will read this code in the future.
class Microfilesys:
    def __init__(self):
        self.command_parts  = None
        self.command_join   = None
        self.length         = None
        self.file_opetation_command_handlers = {
            'read' : self.handle_read_command,
            'write': self.handle_write_command,
            'clear': self.handle_clear_command
        }
        self.manage_file_command_handlers = {
            'create': self.handle_create_command,
            'open': self.handle_open_command,
            'delete': self.handle_delete_command
        }
        
        self.command    = None
        self.filename   = None
        self.option     = None
        self.line       = None
        self.content    = None
    
    def read():
        pass
    def write():
        pass
    def clear():
        pass
    def create():
        pass
    def open():
        pass
    def delete():
        pass

    def handle_read_command(self):
        # option -l
        if self.option == '-l':
            if self.length == 2:
                print("expexted line number after -l")
            elif self.length == 3:
                if self.line and self.line.isdigit():
                    print("line")
                    pass # call read line
                else:
                    print("line not number")
            else:
                print("invalid line length")

            # option -a
        elif self.option == '-a':
            if self.length == 2:
                print("all")
                pass # call read all
            else:
                print("invalid all length")
        else:
            print(f"{self.option} is not a valid option")

    def handle_write_command(self):
        # option -l
        if self.option == '-l':
            if self.length == 2:
                print("expexted line number after -l")
            elif self.length == 3:
                if self.line and self.line.isdigit():
                    print(f"expected content after line: {self.command_join} \"example content\"")
                else:
                    print("line not number")
                    
            elif self.length >= 4:
                if is_content(self.command_parts, 3):
                    print(get_content(self.command_parts, 3))
                    pass # call write line
            else:
                print("invalid line length")

        # option -end
        elif self.option == '-e':
            if self.length == 2:
                print("expexted line number after -e")
            elif self.length == 3:
                if self.line and self.line.isdigit():
                    print(f"expected content after line: {self.command_join} \"example content\"")
                else:
                    print("line not number")
            elif self.length >= 4:
                if is_content(self.command_parts, 3):
                    print(get_content(self.command_parts, 3))
                    pass # call write line
            else:
                print("invalid line length")
        else:
            print(f"{self.option} is not a valid option")

    def handle_clear_command(self):
        # option -l
        if self.option == '-l':
            if self.length == 2:
                print("expexted line number after -l")
            elif self.length == 3:
                if self.line and self.line.isdigit():
                    print("line")
                    pass # call read line
                else:
                    print("line not number")
            else:
                print("invalid line length")

        # option -a
        elif self.option == '-a':
            if self.length == 2:
                print("all")
                pass # call read all
            else:
                print("invalid all length")
        else:
            print(f"{self.option} is not a valid option")

    def handle_create_command(self):
        if is_file(self.filename):
            print(f"'{self.filename}' already exist")

        else:
            with open(self.filename, "w") as file:
                print(f"'{self.filename}' created successfully")

    def handle_open_command(self):
        if not is_file(self.filename):
            print(f"'{self.filename}' doesnt exist")

        else:
            self.file_operator()

    def handle_delete_command(self):
        if not is_file(self.filename):
            print(f"'{self.filename}' doesnt exist")
        
        else:
            os.remove(self.filename)
            print(f"'{self.filename}' deleted successfully")

    def start_microfilesys(self):
        running = True
        while running:
            try:
                command_input = input(f"microfilesys-{self.filename}: " if self.filename else "microfilesys: ")
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                return
            
            if not command_input:
                continue
            
            # initialize all the variable
            self.command_parts   = command_input.split()
            self.command_join    = ' '.join(self.command_parts)
            self.length          = len(self.command_parts)

            self.command    = self.command_parts[0]
            self.filename   = self.command_parts[1] if self.length == 2 else None
            self.option     = self.command_parts[1] if self.length >= 2 else None
            self.line       = self.command_parts[2] if self.length >= 3 else None
            self.content    = self.command_parts[3] if self.length >= 4 else None

            # if no files are open but is using file editor command
            if self.command in self.file_opetation_command_handlers:
                print(f"open a file first first before using {self.command} command")
        
            # check if is using file manager command
            elif self.command in self.manage_file_command_handlers:
                if self.filename:
                    self.file_manager()
                else:
                    print("file name couldnt be empty")
                    
            else:
                print("invalid command")

parser = Microfilesys()
parser.start_microfilesys()