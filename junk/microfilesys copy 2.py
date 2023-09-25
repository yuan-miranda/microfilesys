import os

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

class Errors:
    error_messages = {
        "invalid command": {
            command: f"invalid command: use 'man {command}' for {command} command usage"
            for command in command_flags.keys()
        },

        "invalid flag": {
            command: f"invalid flag: {command} only use '" + ', '.join(command_flags[command]) + "'"
            for command in command_flags.keys()
        }
    }

    def write(flag):
        if flag in ["-we", "--write-end"]:
            return f"invalid syntax: expected 'write {flag} line \"content\"'"
            
        elif flag in ["-ws", "--write-specific"]:
            return f"invalid syntax: expected 'write {flag} line column \"content\"'"

    def modify(flag):
        if flag in ["-ms", "--modify-specific"]:
            return f"invalid syntax: expected 'modify {flag} line column \"content\"'"
            
        elif flag in ["-ma", "--modify-all"]:
            return f"invalid syntax: expected 'modify {flag} line \"content\"'"
            
        elif flag in ["-mas", "--modify-all-specific"]:
            return f"invalid syntax: expected 'modify {flag} line \"content\" \"replace to\"'"

    def remove(flag):
        if flag in ["-rmsub", "--remove-substring"]:
            return f"invalid syntax: expected 'remove {flag} line \"content\"'"
            
        elif flag in ["-rms", "--remove-specific"]:
            return f"invalid syntax: expected 'remove {flag} line column'"
            
        elif flag in ["-rmas", "--remove-all-specific"]:
            return f"invalid syntax: expected 'remove {flag} line column \"content\"'"
        
    def clear(flag):
        if flag in ["-cl", "--clear-line"]:
            return f"invalid syntax: expected 'clear {flag} line'"
            
        elif flag in ["-ca", "--clear-all"]:
            return f"invalid syntax: expected 'clear {flag}'"

    def read(flag):
        if flag in ["-rl", "--read-line"]:
            return f"invalid syntax: expected 'read {flag} line'"
            
        elif flag in ["-ra", "--read-all"]:
            return f"invalid syntax: expected 'read {flag}'"

    def close(flag):
        return f"invalid syntax: expected 'close {flag}'"

    def create(error_type):
        return "invalid syntax: expexted 'create file.py'"

    def open(flag=None):
        if flag in ["-r", "--read"]:
            return f"invalid syntax: expected 'open {flag} \"file.py\"'"

        elif flag in ["-rw", "--read-write"]:
            return f"invalid syntax: expected 'open {flag} \"file.py\"'"

    def delete(error_type):
        return "invalid syntax: expected 'delete file.py'"

def is_line(line):
    return line.isdigit()

def is_multi_column(column):
    pass
def is_column(column):
    pass
    #is_correct_length = True if len(column) == 5 else False
    #is_correct_format = True if 

    # logic
    # check if input <= input length (it needs to check the input first) then run the logic below
    # if "a1" make "a1"
    # if "a1:a2" make "a1:a2"

    # write commnand
    # a1        a1
    # modify and remove command
    # a1:a2      a1:a2
    #

    # FIX FLAGS PARAMAETER 9.20
def is_flag_correct(input, length, flag):
    return True if len(input) != len and flag in ["-rmsub", "--remove-substring"] else True
class commands:
    # flag line column content replace

    def write(user_input):
        flag = user_input[1]

        if not flag in command_flags["write"]:
            print(Errors.error_messages["invalid flag"]["write"])

        elif len(user_input) == 4 and flag in ["-we", "--write-end"]: # flag line content
            line = user_input[2]
            content = user_input[3]
            print(flag, line, content)

        elif len(user_input) == 5 and flag in ["-ws", "--write-specific"]: # flag line column content
            line = user_input[2]
            column = user_input[3]
            content = user_input[4]
            print(flag, line, column, content)

        else:
            print(Errors.write(flag))

    def modify(user_input):
        flag = user_input[1]

        if not flag in command_flags["modify"]:
            print(Errors.error_messages["invalid flag"]["modify"])
            
        elif len(user_input) == 5 and flag in ["-ms", "--modify-specific"]: # flag line column content
            line = user_input[2]
            column = user_input[3]
            content = user_input[4]
            print(flag, line, column, content)

        elif len(user_input) == 4 and flag in ["-ma", "--modify-all"]: # flag line content
            line = user_input[2]
            content = user_input[3]
            print(flag, line, column, content)
                
        elif len(user_input) == 5 and flag in ["-mas", "--modify-all-specific"]: # flag line content replace
            line = user_input[2]
            content = user_input[3]
            replace_to = user_input[4]
            print(flag, line, column, content, replace_to)

        else:
            print(Errors.modify(flag))
    
    def remove(user_input):
        flag = user_input[1]

        if not flag in command_flags["remove"]:
            print(Errors.error_messages["invalid flag"]["remove"])

        elif len(user_input) == 4 and flag in ["-rmsub", "--remove-substring"]: # flag line content
            line = user_input[2]
            content = user_input[3]
            print(flag, line, content)

        elif len(user_input) == 4 and flag in ["-rms", "--remove-specific"]: # flag line column
            line = user_input[2]
            column = user_input[3]
            print(flag, line, column)

        elif len(user_input) == 4 and flag in ["-rmas", "--remove-all-specific"]: # flag line content
            line = user_input[2]
            content = user_input[3]
            print(flag, line, column, content)

        else:
            print(Errors.remove(flag))
    
    def clear(user_input):
        flag = user_input[1]

        if not user_input[1] in command_flags["clear"]:
            print(Errors.error_messages["invalid flag"]["clear"])

        elif len(user_input) == 3 and flag in ["-cl", "--clear-line"]: # flag line
            line = user_input[2]
            print(flag, line)

        elif len(user_input) == 2 and flag in ["-ca", "--clear-all"]: # flag
            print(flag)

        else:
            print(Errors.clear(flag))
    
    def read(user_input):
        flag = user_input[1]

        if not flag in command_flags["read"]:
            print(Errors.error_messages["invalid flag"]["read"])

        elif len(user_input) == 3 and flag in ["-rl", "--read-line"]: # flag line
            line = user_input[2]
            print(flag, line)

        elif len(user_input) == 2 and flag in ["-ra", "--read-all"]: # flag
            print(flag)

        else:
            print(Errors.read(flag))
    
    def close(user_input):
        flag = user_input[1]

        if not flag in command_flags["close"]:
            print(Errors.error_messages["invalid flag"]["close"])

        elif len(user_input) == 2 and flag in ["-c", "--close"]: # flag
            print(flag)

        else:
            print(Errors.close(flag))

    def create(user_input):
        file = user_input[1]

        if len(user_input) != 2:
            print(Errors.create("invalid syntax"))
            
        elif file in os.listdir():
            print("file already exist")

        else:
            with open(file, "w") as f:
                print("created")
    
    def open(user_input):
        if not user_input[1] in command_flags["open"]:
            print(Errors.error_messages["invalid flag"]["open"])
            return
        
        flag = user_input[1]

        if len(user_input) != 3:
            print(Errors.open(flag))
            return

        file = user_input[2]

        if file in os.listdir():
            if flag in ["-r", "--read"]:
                file_editor(file, "r")

            elif flag in ["-rw", "--read-write"]:
                file_editor(file, "r+")

        else:
            print("file doesnt exist")

    def delete(user_input):
        file = user_input[1]
            
        if len(user_input) != 2:
            print(Errors.delete("invalid syntax"))
                
        elif file in os.listdir():
            os.remove(file)
            print("deleted")

        else:
            print("file doesnt exist")

minor_command_handler = {
    "write":  commands.write,
    "modify": commands.modify,
    "remove": commands.remove,
    "clear":  commands.clear,
    "read":   commands.read,
    "close":  commands.close,
}

major_command_handler = {
    "create": commands.create,
    "open": commands.open,
    "delete": commands.delete
}

def file_editor(filepath, mode):
    with open(filepath, mode) as f:
        while True:
            try:
                user_input = input(f"microfilesys-{filepath}: ").split()
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                return
            except Exception as error:
                print("An error occured: ", error)

            if not user_input:
                continue

            elif len(user_input) == 1 and user_input[0] in ["quit", "exit"]:
                exit()
                    
            command = user_input[0]

            if not command in minor_command_handler:
                print(f"'{' '.join(user_input)}' is not a valid file editor command")

            elif len(user_input) == 1:
                print(Errors.error_messages["invalid command"][command])
            else:
                minor_command_handler[command](user_input)

def file_manager():
    while True:
        try:
            user_input = input("microfilesys: ").split()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            exit()

        if not user_input:
            continue

        command = user_input[0]

        if len(user_input) == 1 and command in ["quit", "exit"]:
            exit()

        elif len(user_input) == 1 and command in major_command_handler: # MAKE THIS ACCEPT 1 or MORE INPUT FOR file_editor
            print(Errors.error_messages["invalid command"][command])
        elif not command in major_command_handler:
            print(f"'{' '.join(user_input)}' is not a valid file manager command")
        else:
            major_command_handler[command](user_input)

if __name__ == "__main__":
    file_manager()