# FIX COMMAND HANDLING HERE 10/2 (done)
# STUDY ARGPARSE AND CONVENTION OF PROGRAMMING COMMAND LINE 10/3 (done)
# MAKE THE ALGORITHM FOR FINDING THE ENCLOSED DOUBLE QUOTE 10/5 (done)

import os

def file_length(file):
    with open(file, 'r') as f:
        return len(f.readlines())

def in_line_length(lines, line_number):
    if line_number > 0 and line_number <= len(lines):
        pass

# return the content
def get_content(content):
    return ' '.join(content)[1:-1]

# check if the input is a content
def is_content(content):
    string = ' '.join(content) 
    content_start = string[0]
    content_end = string[-1]

    # early return if the content has more or less than double quotes on it
    if string.count('"') != 2:
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

class Command:
    class help:
        @staticmethod
        # display_help()
        def file_editor():
            print("Usage:")
            print("\tread (-ln line=1 | -all)")
            print("\twrite (-ln | -end) line=1 content=\"str\"")
            print("\tclear (-ln line=1 | -all)")
        
        @staticmethod
        def file_manager():
            print("Usage:")
            print("\tcreate file")
            print("\tdelete file")
            print("\topen (-r | -w) file")

    class create:
        @staticmethod
        def file(file):
            if file in os.listdir():
                print(f"'{file}' already exist")
            else:
                with open(file, "w") as f:
                    print(f"'{file}' created")

    class delete:
        @staticmethod
        def file(file):
            if file not in os.listdir():
                print(f"'{file}' doesnt exist")
            else:
                os.remove(file)
                print(f"'{file}' deleted")
    
    class open:
        @staticmethod
        def file(file):
            if file not in os.listdir():
                print(f"'{file}' doesnt exist")
            else:
                file_editor(file)

    class read:
        @staticmethod
        def line(file, line):
            with open(file, 'r') as f:
                try:
                    print("____________________________________________________________")
                    print(f.readlines()[int(line) - 1].rstrip('\n'))
                    print("____________________________________________________________")
                except IndexError:
                    print(f"IndexError: '{file}' is only {file_length(file)} lines long not {line}.")
        
        @staticmethod
        def all(file):
            with open(file, 'r') as f:
                print("____________________________________________________________")
                print(f.read()) # read whole file
                print("____________________________________________________________")

    class write:
        @staticmethod
        def line(file, line_number, content): # 
            print("writeln")

        @staticmethod
        def end(file, line_number, content):
            # Read the file and split it into lines
            with open(file, 'r+') as f:
                lines = f.readlines()

                if line_number > 0 and line_number <= len(lines):
                    # Append text to the end of the specified line
                    lines[line_number - 1] = lines[line_number - 1].rstrip('\n') + content + '\n'
                    f.seek(0)
                    f.writelines(lines)
                else:
                    print(f"line must be in range of 1 to {len(lines)} not {line_number}")
        
    class clear():
        @staticmethod
        def line(file, line):
            print("clearln")

        @staticmethod
        def all(file):
            print("clearall")

file_editor_commands = ["help", "read", "write", "clear"]

file_editor_command_error = {
    "help": "Expected 'help -h'",
    "read": "Expected 'read (-ln line=1 | -all)'",
    "write": "Expected 'write (-ln | -end) line=1 content=\"string\"'",
    "clear": "Expected 'clear (-ln line=1 | -all)'"
}

file_editor_argument_length = {
    "help": {
        "-h": 2,
        "-help": 2
    },
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

flag_that_has_line = ["-ln", "-end"]

file_manager_commands = ["help", "delete", "create", "open"]
quit_command = ["quit", 'q', "exit", "ext"]

def file_editor(file):
    running = True
    while running:
        try:
            user_input = input(f"microfilesys-{file}: ")
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            return
    
        if not user_input:
            continue
        
        cmd_args = user_input.split()
        cmd_args_len = len(cmd_args)
        
        cmd = cmd_args[0]
        flag = cmd_args[1] if cmd_args_len >= 2 else False
        line = cmd_args[2] if cmd_args_len >= 3 else ""
        content = cmd_args[3:] if cmd_args_len >= 4 else False

        # end file_editor() operation command
        if cmd in quit_command:
            running = False
        
        # MAKE INVALID FLAG ERROR, USAGE OF THAT FLAG 7/10
        # MAKE DYNAMIC FILE LENGTH IDENTIFIER, SO I DONT NEED TO COMPARE EACH ITERATION 7/10
            # MAKE A HANDLER WHERE IT HAS AALL NESESSARY ARGUMENTS REQUIRED

        # if command is not a valid file editor command, thow invalid command error
        if cmd not in file_editor_commands:
            print(f"'{cmd}' is not a valid command in '{user_input}'")

        # if command argument length is less than 2 but is valid command, thow expected command error
        if cmd in file_editor_commands and cmd_args_len == 1:
            print('1')
            print(file_editor_command_error[cmd])
        
        # if line is not number, argument length >= 3 to ensure it has a line, and must be in flag that has line
        if not line.isdigit() and cmd_args_len == 3 and flag in flag_that_has_line:
            print(f"'{line}' is not a number to be a valid line")

        # help command
        elif cmd == "help":
            if cmd_args_len == 2 and flag in ["-h", "-help"]:
                Command.help.file_editor()
            else:
                print('3')
                print(file_editor_command_error[cmd])
                
        # read command
        elif cmd == "read":
            if cmd_args_len == 3 and flag == "-ln":
                Command.read.line(file, line)

            elif cmd_args_len == 2 and flag == "-all":
                Command.read.all(file)
            else:
                print('3')
                print(file_editor_command_error[cmd])

        # write command
        elif cmd == "write":
            if cmd_args_len >= 4 and flag == "-ln" and is_content(content):
                Command.write.line(get_content(content))

            elif cmd_args_len >= 4 and flag == "-end" and is_content(content):
                Command.write.end(file, int(line), get_content(content))
            else:
                print('3')
                print(file_editor_command_error[cmd])
        # clear command
        elif cmd == "clear":
            if cmd_args_len == 3 and flag == "-ln":
                Command.clear.line(file, line)

            elif cmd_args_len == 2 and flag == "-all":
                Command.clear.all(file)
            else:
                print('3')
                print(file_editor_command_error[cmd])

def file_manager():
    running = True
    while running:
        try:
            user_input = input("microfilesys: ")
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            exit()

        if not user_input:
            continue

        cmd_args = user_input.split()
        cmd_args_len = len(cmd_args)
        cmd = cmd_args[0]
        flag = cmd_args[1] if cmd_args_len >= 2 else None
        file = cmd_args[1] if cmd_args_len >= 2 else None
        
        if cmd in quit_command:
            running = False

        if cmd not in file_manager_commands:
            print(f"'{cmd}' is not a valid command in '{user_input}'")

        elif cmd == "help":
                if cmd_args_len == 2 and flag in ["-h", "-help"]:
                    Command.help.file_manager()
                else:
                    print("Expected 'help -h")

        # create command
        elif cmd == "create":
            if cmd_args_len == 2:
                Command.create.file(file)
            else:
                print(f"Expected 'create file'")

        # delete command
        elif cmd == "delete":
            if cmd_args_len == 2:
                Command.delete.file(file)
            else:
                print(f"Expected 'delete file'")
        
        # open command
        elif cmd == "open":
            if cmd_args_len == 2:
                Command.open.file(file)
            else:
                print(f"Expected 'open file'")

def main():
    file_manager()
        
if __name__ == "__main__":
    main()