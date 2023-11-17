import os

command_flags = {                                   # 2   3   4   5
    "write":  ["-we", "--write-end",                        # 4     
               "-ws", "--write-specific"],                      # 5     
    
    "modify": ["-ms", "--modify-specific",                      # 5    
               "-ma", "--modify-all",                       # 4     
               "-mas", "--modify-all-specific"],                # 5
    
    "remove": ["-rmsub", "--remove-substring",              # 4     
               "-rms", "--remove-specific",                 # 4     
               "-rmas", "--remove-all-specific"],           # 4     
    
    "clear":  ["-cl", "--clear-line",                   # 3     
               "-ca", "--clear-all"],               # 2     
    
    "read":   ["-rl", "--read-line",                    # 3  
               "-ra", "--read-all"],                # 2    
    
    "create": [],                                   # 2   
    
    "open":   ["-r", "--read",                          # 3     
               "-w", "--write",                         # 3    
               "-cp", "--copy"],                        # 3    
    
    "close":  ["-c", "--close"],                        # 2
    
    "delete": ["-d", "--delete"],                       # 3     
}

class commands:
    def write(param): # done
        try:
            flag = param[1]
            line= param[2]
            # lenght of param MUST DO
            if len(param) == 4 and flag in ["-we", "--write-end"]:
                content = param[3]
                print(flag, line, content)
            elif len(param) == 5 and flag in ["-ws", "--write-specific"]:
                column = param[3]
                content = param[4]
                print(flag, line, column, content)
        except Exception as error:
            print("An error occured: ", error)
    def modify(param): # done
        try:
            flag = param[1]
            line = param[2]
            if len(param) == 5 and flag in ["-ms", "--modify-specific"]:
                column = column[3]
                content = param[4]
                print(flag, line, column, content)
            elif len(param) == 4 and flag in ["-ma", "--modify-all"]:
                content = param[3]
                print(flag, line, column, content)
            elif len(param) == 5 and flag in ["-mas", "--modify-all-specific"]:
                content = param[3]
                replace_to = param[4]
                print(flag, line, column, content, replace_to)
        except Exception as error:
            print("An error occured: ", error)
    def remove(param): # done
        try:
            flag = param[1]
            line = param[2]
            if len(param) == 4 and flag in ["-rmsub", "--remove-substring"]:
                content = param[3]
                print(flag, line, content)
            elif len(param) == 4 and flag in ["-rms", "--remove-specific"]:
                column = param[3]
                print(flag, line, column)
            elif len(param) == 4 and flag in ["-rmas", "--remove-all-specific"]:
                content = param[3]
                print(flag, line, column, content)
        except Exception as error:
            print("An error occured: ", error)
    def clear(param): # done
        try:
            flag = param[1]
            if len(param) == 3 and flag in ["-cl", "--clear-line"]:
                line = param[2]
                print(flag, line)
            elif len(param) == 2 and flag in ["-ca", "--clear-all"]:
                print(flag)
        except Exception as error:
            print("An error occured: ", error)
    def read(param): # done
        try:
            flag = param[1]
            if len(param) == 3 and flag in ["-rl", "--read-line"]:
                line = param[2]
                print(flag, line)
            elif len(param) == 2 and flag in ["-ra", "--read-all"]:
                print(flag)
        except Exception as error:
            print("An error occured: ", error)
    def close(param): # done
        try:
            flag = param[1]
            if len(param) == 2 and flag in ["-c", "--close"]:
                print(flag)
        except Exception as error:
            print("An error occured: ", error)
command_handler = {
    "write":  commands.write,
    "modify": commands.modify,
    "remove": commands.remove,
    "clear":  commands.clear,
    "read":   commands.read,
    #"create": commands.create,
    #"open":   commands.open,
    "close":  commands.close
    #"delete": commands.delete
}
def run(filepath, mode):
    try:
        with open(filepath, mode) as file:
            while True:
                user_input = input(f"microfilesys-{filepath}: ").split()
                # check if empty
                if not user_input:
                    continue
                # less than or only one input
                elif len(user_input) < 2:
                    print("not long")
                    continue
                
                command = user_input[0]
                flag = user_input[1]
                if len(user_input) <= 5 and user_input[1] in command_flags.get(user_input[0], []):
                    command_handler[command](user_input)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        return
    except Exception as error:
        print("An error occured: ", error)

def main():
    while True:
        try:
            user_input = input("microfilesys: ").split()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            exit()

        # check if the input is empty
        if not user_input:
            continue

        # quit the program
        elif len(user_input) == 1 and user_input[0] in ["quit", "exit"]:
            exit()


        # create a file
        elif len(user_input) == 2 and user_input[0] == "create":
            try:
                if not user_input[1] in os.listdir():
                    with open(user_input[1], "w") as file:
                        print("created")
                else:
                    print("file already exist")
            except Exception as error:
                print("An error occurred: ", error)

        # delete file
        elif len(user_input) == 2 and user_input[0] == "delete":
            try:
                if user_input[1] in os.listdir():
                    os.remove(user_input[1])
                    print("deleted")
                else:
                    print("file doesnt exist")
            except Exception as error:
                print("An error occurred: ", error)

        # open a file
        elif len(user_input) == 3 and user_input[0] == "open":
            if user_input[2] in os.listdir():
                if user_input[1] in ["-r", "--read"]:
                    run(user_input[2], "r")
                elif user_input[1] in ["-w", "--write"]:
                    run(user_input[2], "r+")

                # create copy here later
                #elif user_input[2] in ["-cp", "--copy"]:
                #    open(user_input[3] + "_copy.py", "r+")
            else:
                print("file doesnt exist")
        else:
            print("invalid input")
if __name__ == "__main__":
    main()