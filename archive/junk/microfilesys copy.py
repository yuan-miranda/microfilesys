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

class Write:
    def write_end():
        pass
    def write_specific():
        pass
class Modify():
    def modify_specific():
        pass
    def modify_all():
        pass
    def modify_all_specific():
        pass
class Remove:
    def remove_substring():
        pass
    def remove_specific():
        pass
    def remove_all_specific():
        pass
class Clear:
    def clear_line():
        pass
    def clear_all():
        pass
class Read:
    def read_line():
        pass
    def read_all():
        pass
class Close:
    def close():
        pass
class Create:
    def create():
        pass
class Open:
    def open():
        pass
class Delete:
    def delete():
        pass

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

class Commands:
    # flag line column content replace

    def write(user_input):
        flag = user_input[1]

        if len(user_input) == 4 and flag in ["-we", "--write-end"]: # flag line content
            line = user_input[2]
            content = user_input[3]
            Write.write_end(line, content)
            print(flag, line, content)

        elif len(user_input) == 5 and flag in ["-ws", "--write-specific"]: # flag line column content
            line = user_input[2]
            column = user_input[3]
            content = user_input[4]
            Write.write_specific(flag, line, column, content)
            print(flag, line, column, content)

        else:
            print(Errors.write(flag))

    def modify(user_input):
        flag = user_input[1]

        if len(user_input) == 5 and flag in ["-ms", "--modify-specific"]: # flag line column content
            line = user_input[2]
            column = user_input[3]
            content = user_input[4]
            Modify.modify_specific(flag, line, column, content)
            print(flag, line, column, content)

        elif len(user_input) == 4 and flag in ["-ma", "--modify-all"]: # flag line content
            line = user_input[2]
            content = user_input[3]
            Modify.modify_all(flag, line, column, content)
            print(flag, line, column, content)
                
        elif len(user_input) == 5 and flag in ["-mas", "--modify-all-specific"]: # flag line content replace
            line = user_input[2]
            content = user_input[3]
            replace_to = user_input[4]
            Modify.modify_all_specific(flag, line, column, content, replace_to)
            print(flag, line, column, content, replace_to)

        else:
            print(Errors.modify(flag))
    
    def remove(user_input):
        flag = user_input[1]
        # Remove.rmsub
        if len(user_input) == 4 and flag in ["-rmsub", "--remove-substring"]: # flag line content
            line = user_input[2]
            content = user_input[3]
            Remove.remove_substring(flag, line, content)
            print(flag, line, content)

        elif len(user_input) == 4 and flag in ["-rms", "--remove-specific"]: # flag line column
            line = user_input[2]
            column = user_input[3]
            Remove.remove_specific(flag, line, column)
            print(flag, line, column)

        elif len(user_input) == 4 and flag in ["-rmas", "--remove-all-specific"]: # flag line content
            line = user_input[2]
            content = user_input[3]
            Remove.remove_all_specific(flag, line, column, content)
            print(flag, line, column, content)

        else:
            print(Errors.remove(flag))
    
    def clear(user_input):
        flag = user_input[1]

        if len(user_input) == 3 and flag in ["-cl", "--clear-line"]: # flag line
            line = user_input[2]
            Clear.clear_line(flag, line)
            print(flag, line)

        elif len(user_input) == 2 and flag in ["-ca", "--clear-all"]: # flag
            Clear.clear_all(flag)
            print(flag)

        else:
            print(Errors.clear(flag))
    
    def read(user_input):
        flag = user_input[1]

        if len(user_input) == 3 and flag in ["-rl", "--read-line"]: # flag line
            line = user_input[2]
            Read.read_line(flag, line)
            print(flag, line)

        elif len(user_input) == 2 and flag in ["-ra", "--read-all"]: # flag
            Read.read_all(flag)
            print(flag)

        else:
            print(Errors.read(flag))
    
    def close(user_input):
        flag = user_input[1]

        if len(user_input) == 2 and flag in ["-c", "--close"]: # flag
            Close.close(flag)
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
            Create.create(file)
            with open(file, "w") as f:
                print("created")
    
    def open(user_input): # MAKE CLASS?
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
            Delete.delete(file)
            os.remove(file)
            print("deleted")

        else:
            print("file doesnt exist")

# idk how to explain this but I use this when I need to
# iterate on commands and call them in their proper operation
file_editor_cmd_handler = {
    "write":  Commands.write,
    "modify": Commands.modify,
    "remove": Commands.remove,
    "clear":  Commands.clear,
    "read":   Commands.read,
    "close":  Commands.close,
}

file_manager_cmd_handler = {
    "create": Commands.create,
    "open":   Commands.open,
    "delete": Commands.delete
}

# make the input into a list
def make_list(text):
    return text.split()

# manage the file editing logic
def file_editor(filepath, mode):
    with open(filepath, mode) as f:
        while True:
            try:
                user_input = input(f"microfilesys-{filepath}: ")
                user_input_formatted = make_list(user_input)
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                return
            except Exception as error:
                print("An error occured: ", error)

            # ignore input if its empty
            if not user_input:
                continue
            
            cmd = user_input_formatted[0]

            # check if user want to quit
            if user_input in ["quit", "exit"]:
                exit()

            # prompt to use the command manual if input is valid command but
            # only the command is being called
            elif len(user_input_formatted) == 1 and cmd in file_editor_cmd_handler: # MAKE THIS ACCEPT 1 or MORE INPUT FOR file_editor
                print(Errors.error_messages["invalid command"][cmd])

            # throw an error if user type a non-command input
            elif not cmd in file_editor_cmd_handler:
                print(f"'{' '.join(user_input_formatted)}' is not a valid file editor command")
            
            # note: user_input[1] is the flag
            # throw an error if the command's flag is incorrect
            elif not user_input[1] in command_flags[cmd]:
                print(Errors.error_messages["invalid flag"][cmd])

            # call the appopriate command when it pass all the conditions above
            else:
                file_editor_cmd_handler[cmd](user_input_formatted)

# manage the file operation logic
def file_manager():
    running = True
    while running:
        try:
            user_input = input("microfilesys: ")
            user_input_formatted = make_list(user_input)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            exit()
        except Exception as error:
            print("An error occured: ", error)

        # ignore input if its empty
        if not user_input:
            continue
        
        cmd = user_input_formatted[0]

        # check if user want to quit
        if user_input in ["quit", "exit"]:
            exit()
        
        # prompt to use the command manual if input is valid command but
        # only the command is being called
        elif len(user_input_formatted) == 1 and cmd in file_manager_cmd_handler: # MAKE THIS ACCEPT 1 or MORE INPUT FOR file_editor
            print(Errors.error_messages["invalid command"][cmd])
        
        # throw an error if user type a non-command input
        elif not cmd in file_manager_cmd_handler:
            print(f"'{' '.join(user_input_formatted)}' is not a valid file manager command")
        
        # call the appopriate command when it pass all the conditions above
        else:
            file_manager_cmd_handler[cmd](user_input_formatted)


def main():
    file_manager()

if __name__ == "__main__":
    main()