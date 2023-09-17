import os

# command flags
command_flags = {
    "write":  ["-we", "--write-end",
               "-ws", "--write-specific"],
    "modify": ["-ms", "--modify-specific",
               "-ma", "--modify-all",
               "-mas", "--modify-all-specific"],
    "remove": ["-rmsub", "--remove-substring",
               "-rms", "--remove-specific",
               "-rmas", "--remove-all-specific"],
    "clear":  ["-cl", "--clear-line",
               "-ca", "--clear-all"],
    "read":   ["-rl", "--read-line",
               "-ra", "--read-all"],
    "close":  ["-c", "--close"],

    "create": [],
    "open":   ["-r", "--read",
               "-rw", "--read-write"],
    "delete": [],
}

# class of all the commands available
class Errors:
    error_messages = {
        "invalid command": {
            command: f"invalid command: use 'man {command}' for {command} command usage"
            for command in command_flags.keys()
        },

        "invalid flag": {
            command: f"invalid flag: {command} only use '" + ', '.join(command_flags[command]) + "'"
            for command in command_flags.keys()
        },
        "invalid syntax": {
            "write": {

            }
        }
    }

    def write(error_type, flag):
            if flag in ["-we", "--write-end"]:
                return f"invalid syntax: expected 'write {flag} line \"content\"'"
            
            elif flag in ["-ws", "--write-specific"]:
                return f"invalid syntax: expected 'write {flag} line column \"content\"'"

    # modify function
    def modify(error_type, flag):
            if flag in ["-ms", "--modify-specific"]:
                return f"invalid syntax: expected 'modify {flag} line column \"content\"'"
            
            elif flag in ["-ma", "--modify-all"]:
                return f"invalid syntax: expected 'modify {flag} line \"content\"'"
            
            elif flag in ["-mas", "--modify-all-specific"]:
                return f"invalid syntax: expected 'modify {flag} line \"content\" \"replace to\"'"

    # remove function
    def remove(error_type, flag):
            if flag in ["-rmsub", "--remove-substring"]:
                return f"invalid syntax: expected 'remove {flag} line \"content\"'"
            
            elif flag in ["-rms", "--remove-specific"]:
                return f"invalid syntax: expected 'remove {flag} line column'"
            
            elif flag in ["-rmas", "--remove-all-specific"]:
                return f"invalid syntax: expected 'remove {flag} line column \"content\"'"
        
    # clear function
    def clear(error_type, flag):
        if error_type == "invalid syntax":
            if flag in ["-cl", "--clear-line"]:
                return f"invalid syntax: expected 'clear {flag} line'"
            
            elif flag in ["-ca", "--clear-all"]:
                return f"invalid syntax: expected 'clear {flag}'"

    # read function
    def read(error_type, flag):
        if error_type == "invalid syntax":
            if flag in ["-rl", "--read-line"]:
                return f"invalid syntax: expected 'read {flag} line'"
            
            elif flag in ["-ra", "--read-all"]:
                return f"invalid syntax: expected 'read {flag}'"

    # close function
    def close(error_type, flag):
        if error_type == "invalid syntax":
            return f"invalid syntax: expected 'close {flag}'"

    # create function
    def create(error_type):
        if error_type == "invalid syntax":
            return "invalid syntax: expexted 'create file.py'"

    # open function
    def open(error_type, flag=None):
        if error_type == "invalid syntax":
            if flag in ["-r", "--read"]:
                return f"invalid syntax: expected 'open {flag} \"file.py\"'"

            elif flag in ["-rw", "--read-write"]:
                return f"invalid syntax: expected 'open {flag} \"file.py\"'"

    # delete function
    def delete(error_type):
        if error_type == "invalid syntax":
            return "invalid syntax: expected 'delete file.py'"

class commands:
    # write function
    def write(user_input):
        flag = user_input[1]

        if not flag in command_flags["write"]:
            print(Errors.error_messages["invalid flag"]["write"])

        elif len(user_input) == 4 and flag in ["-we", "--write-end"]:
            line = user_input[2]
            content = user_input[3]
            print(flag, line, content)

        elif len(user_input) == 5 and flag in ["-ws", "--write-specific"]:
            line = user_input[2]
            column = user_input[3]
            content = user_input[4]
            print(flag, line, column, content)

        else:
            print(Errors.write("invalid syntax", flag))

    # modify function
    def modify(user_input):
        flag = user_input[1]

        if not flag in command_flags["modify"]:
            print(Errors.error_messages["invalid flag"]["modify"])
            
        elif len(user_input) == 5 and flag in ["-ms", "--modify-specific"]:
            line = user_input[2]
            column = user_input[3]
            content = user_input[4]
            print(flag, line, column, content)

        elif len(user_input) == 4 and flag in ["-ma", "--modify-all"]:
            line = user_input[2]
            content = user_input[3]
            print(flag, line, column, content)
                
        elif len(user_input) == 5 and flag in ["-mas", "--modify-all-specific"]:
            line = user_input[2]
            content = user_input[3]
            replace_to = user_input[4]
            print(flag, line, column, content, replace_to)

        else:
            print(Errors.modify("invalid syntax", flag))
    
    # remove function
    def remove(user_input):
        flag = user_input[1]

        if not flag in command_flags["remove"]:
            print(Errors.error_messages["invalid flag"]["remove"])

        elif len(user_input) != 4 and flag in ["-rmsub", "--remove-substring"]:
            line = user_input[2]
            content = user_input[3]
            print(flag, line, content)

        elif len(user_input) != 4 and flag in ["-rms", "--remove-specific"]:
            line = user_input[2]
            column = user_input[3]
            print(flag, line, column)

        elif len(user_input) != 4 and flag in ["-rmas", "--remove-all-specific"]:
            line = user_input[2]
            content = user_input[3]
            print(flag, line, column, content)

        else:
            print(Errors.remove("invalid syntax", flag))
    
    # clear function
    def clear(user_input):
        flag = user_input[1]

        if not user_input[1] in command_flags["clear"]:
            print(Errors.error_messages["invalid flag"]["clear"])

        elif len(user_input) == 3 and flag in ["-cl", "--clear-line"]:
            line = user_input[2]
            print(flag, line)

        elif len(user_input) == 2 and flag in ["-ca", "--clear-all"]:
            print(flag)

        else:
            print(Errors.clear("invalid syntax", flag))
    
    # read function
    def read(user_input):
        flag = user_input[1]

        if not flag in command_flags["read"]:
            print(Errors.error_messages["invalid flag"]["read"])

        elif len(user_input) == 3 and flag in ["-rl", "--read-line"]:
            line = user_input[2]
            print(flag, line)

        elif len(user_input) == 2 and flag in ["-ra", "--read-all"]:
            print(flag)

        else:
            print(Errors.read("invalid syntax", flag))
    
    # close function
    def close(user_input):
        flag = user_input[1]

        if not flag in command_flags["close"]:
            print(Errors.error_messages["invalid flag"]["close"])

        elif flag in ["-c", "--close"]:
            print(flag)

        else:
            print(Errors.close("invalid syntax"))

    # create function
    def create(user_input):
        file = user_input[1]

        if len(user_input) != 2:
            print(Errors.create("invalid syntax"))
            
        elif file in os.listdir():
            print("file already exist")

        else:
            with open(file, "w") as f:
                print("created")
    
    # open function
    def open(user_input):
        if not user_input[1] in command_flags["open"]:
            print(Errors.error_messages["invalid flag"]["open"])
            return
        
        flag = user_input[1]

        if len(user_input) != 3:
            print(Errors.open("invalid syntax", flag))
            return

        file = user_input[2]

        if file in os.listdir():
            if flag in ["-r", "--read"]:
                file_editor(file, "r")

            elif flag in ["-rw", "--read-write"]:
                file_editor(file, "r+")

        else:
            print("file doesnt exist")

    # delete function
    def delete(user_input):
        file = user_input[1]
            
        if len(user_input) != 2:
            print(Errors.delete("invalid syntax"))
                
        elif file in os.listdir():
            os.remove(file)
            print("deleted")

        else:
            print("file doesnt exist")

# commands for file editing operation
minor_command_handler = {
    "write":  commands.write,
    "modify": commands.modify,
    "remove": commands.remove,
    "clear":  commands.clear,
    "read":   commands.read,
    "close":  commands.close,
}

# command for file creation
major_command_handler = {
    "create": commands.create,
    "open": commands.open,
    "delete": commands.delete
}

# manage the commands for file editing
def file_editor(filepath, mode):
    try:
        with open(filepath, mode) as f:
            while True:
                # get user input in list form
                user_input = input(f"microfilesys-{filepath}: ").split()

                # check if empty
                if not user_input:
                    continue

                # exit the program
                elif len(user_input) == 1 and user_input[0] in ["quit", "exit"]:
                    exit()
                    
                command = user_input[0]

                # FIX CONTINUITY
                if not command in minor_command_handler:
                    print(f"{user_input} is not a valid file editor command")

                elif len(user_input) == 1:
                    #print(minor_error_handler[command]("invalid command", None))
                    print(Errors.error_messages["invalid command"][command])
                else:
                    minor_command_handler[command](user_input)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        return
    except Exception as error:
        print("An error occured: ", error)

# manage the commands for file opening, creation and deletetion
def file_manager():
    while True:
        try:
            # get user input in list form
            user_input = input("microfilesys: ").split()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            exit()

        # check if the input is empty
        if not user_input:
            continue

        command = user_input[0]

        # quit the program
        if len(user_input) == 1 and command in ["quit", "exit"]:
            exit()

        # FIX THE LENGHT ISSUE
        if len(user_input) == 1:
            #print(major_error_handler[command]("invalid command"))
            print(Errors.error_messages["invalid command"][command])
        elif not command in major_command_handler:
            print("invalid command: '" + ''.join(user_input) + "' is not a valid file manager command")
        else:
            major_command_handler[command](user_input)

# prevent from using the program as a import
if __name__ == "__main__":
    file_manager()