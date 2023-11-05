import os

def file_length(filename):
    """
    returns the file length of the specified file.
    """
    with open(filename, 'r') as file:
        return len(file.readlines())
    
def in_line_length(lines, line_number):
    """
    idk whats this.
    """
    if line_number > 0 and line_number <= len(lines):
        pass

def get_content(content):
    """
    concatenates the array list of content into one string.
    """
    return ' '.join(content)[1:-1]

def is_content(content):
    """
    check if the content has opening and closing double quote.
    """
    content_start = content[0]
    content_end = content[-1]
    
    # early return if the content has no opening and closing double quote.
    if content.count('"') != 2:
        print("use pair of '\"' to enclose the content ex: \"content\"")
        return False
    
    # prevent: a", a"", '"a"'
    if content_start != '"':
        print("missing '\"' on the start of the content")
        return False
    
    # prevent: "a, ""a, '"a"'
    if content_end != '"':
        print("missing '\"' on the end of the content")
        return False

    return True

def is_file(filename):
    """
    check if the file exist on the directory.
    """
    return filename in os.listdir()

class Command:
    """
    all of the commands available are here.
    """
    class help:
        """
        all help related functions.
        """
        @staticmethod
        def display_help():
            """
            display the help guide on the console.
            """
            print("file editor commands")
            print("Usage:")
            print("\tread (-ln line=1 | -all)")
            print("\twrite (-ln | -end) line=1 content=\"str\"")
            print("\tclear (-ln line=1 | -all)")

            print("file manager commands")
            print("Usage:")
            print("\tcreate file")
            print("\tdelete file")
            print("\topen file")

    class create:
        """
        all create related functions.
        """
        @staticmethod
        def file(filename):
            """
            create a file.
            """
            if is_file(filename):
                print(f"'{filename}' already exist")
                
            else:
                with open(filename, "w") as file:
                    print(f"'{filename}' created")
        @staticmethod
        def optional(filename):
            choice = input(f"'{filename}' doesnt exist. Do you want to create it? (Y/N) ? [Default=N]: ").strip().upper()
            if choice == 'Y':
                Command.create.file(filename)
                Command.open.file(filename)
            elif not choice or choice == 'N':
                pass

    class delete:
        """
        all delete related functions.
        """
        @staticmethod
        def file(filename):
            """
            delete a file.
            """
            if not is_file(filename):
                print(f"'{filename}' doesnt exist")
                
            else:
                os.remove(filename)
                print(f"'{filename}' deleted")

    class open:
        """
        all open related functions.
        """
        @staticmethod
        def file(filename):
            """
            open a file.
            """
            if not is_file(filename):
                print(f"'{filename}' doesnt exist")

            else:
                file_editor(filename)

    class read:
        """
        all read related functions.
        """
        def line(filename, line):
            """
            read a single line on the file and print it.
            """
            with open(filename, 'r') as file:
                try:
                    print("____________________________________________________________")

                    # read specified line
                    print(file.readlines()[int(line) - 1].rstrip('\n'))

                    print("____________________________________________________________")

                # if the input line is not in range of file lines
                except IndexError:
                    print(f"IndexError: '{file}' is only {file_length(file)} lines long not {line}.")

        @staticmethod
        def all(filename):
            """
            reads all the lines on the file and print it.
            """
            with open(filename, 'r') as file:
                print("____________________________________________________________")

                # read whole file
                print(file.read())
                
                print("____________________________________________________________")

    class write:
        """
        all write related functions.
        """
        @staticmethod
        def line(filename, line, content):
            """
            write on the line.
            """
            print("writeln")

        @staticmethod
        def end(filename, line_length, content):
            """
            write at the end of the specified line.
            """
            with open(filename, 'r+') as file:
                lines = file.readlines()
                
                # check if input line is in range of file lines
                if line_length > 0 and line_length <= len(lines):

                    # write at the end of the line using this
                    lines[line_length - 1] = lines[line_length - 1].rstrip('\n') + content + '\n'
                    file.seek(0)
                    file.writelines(lines)

                else:
                    print(f"line must be in range of 1 to {len(lines)}")
    
    class clear():
        """
        all clear related functions.
        """
        @staticmethod
        def line(filename, line):
            """
            clear a line on the file
            """
            print("clear line")
        @staticmethod
        def all(filename):
            """
            clear all the file content
            """
            # wtf is this
            Command.delete.file(filename)
            Command.create.file(filename)

# file editor commands
editor_command = ["help", "read", "write", "clear"]

# file manager commands
manager_command = ["help", "delete", "create", "open"]

# command errors
command_error = {
    "help": "Expected 'help'",
    "read": "Expected 'read (-ln line=1 | -all)'",
    "write": "Expected 'write (-ln | -end) line=1 content=\"string\"'",
    "clear": "Expected 'clear (-ln line=1 | -all)'"
}

# expected argument length using these flags
flag_length = {
    "read": {
        "-ln": 3,
        "-all": 2
    },
    "write": {
        "-ln": 4,
        "-end": 4
    },
    "clear": {
        "-ln": 3,
        "-all": 2
    }
}

# flag that needs a line argument after
flag_with_line = ["-ln", "-end"]

# quit command keyword
quit_command = ["q", "quit", "exit"]

def file_editor(filename):
    pass

def file_manager():
    """
    handle all the file managing i.e. creating, deleting, opening files.
    """
    running = True # sole purpose is to make the while loop readable lol

    while running:
        try:
            user_input = input("microfilesys: ")
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            exit()
        
        if not user_input:
            continue

        if user_input in quit_command:
            exit()

        command_argument = user_input.split()
        argument_length = len(command_argument)

        command = command_argument[0]
        file = command_argument[1] if argument_length == 2 else None
        
        if command not in manager_command:
            print(f"'{command}' is not a valid command in '{user_input}'")
            continue

        elif command == "help":
            if argument_length == 1:
                Command.help.display_help()
            else:
                print("Expected 'help")

        elif command == "create":
            if argument_length == 2:
                Command.create.file(file)
            else:
                print(f"Expected 'create file'")

        elif command == "delete":
            if argument_length == 2:
                Command.delete.file(file)
            else:
                print(f"Expected 'delete file'")
        
        elif command == "open":
            if argument_length == 2:
                # prompt if the user wants to create the non existing file
                if is_file(file):
                    Command.open.file(file)
                else:
                    Command.create.optional(file)
            else:
                print(f"Expected 'open file'")

def main():
    file_manager()

if __name__ == "__main__":
    main()