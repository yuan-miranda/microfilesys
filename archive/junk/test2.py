class commands:
    def write(flag=None, line=None, column=None, content=None, replace_to=None):
        if flag == ["-we", "--write-end"]:
            print(content)
        else:
            print(column, content)
    def modify(flag=None, line=None, column=None, content=None, replace_to=None):
        print(flag, line, column, content, replace_to)
    def remove(flag=None, line=None, column=None, content=None, replace_to=None):
        print(flag, line, column, content, replace_to)
    def clear(flag=None, line=None, column=None, content=None, replace_to=None):
        print(flag, line, column, content, replace_to)
    def read(flag=None, line=None, column=None, content=None, replace_to=None):
        print(flag, line, column, content, replace_to)
    def create(content=None):
        print(content)
    def open(flag=None, line=None, column=None, content=None, replace_to=None):
        print(flag, line, column, content, replace_to)
    def close(flag=None, line=None, column=None, content=None, replace_to=None):
        print(flag, line, column, content, replace_to)
    def delete(flag=None, line=None, column=None, content=None, replace_to=None):
        print(flag, line, column, content, replace_to)

command_flags = {
    "write":  ["-we", "--write-end",                # 4     ####
               "-ws", "--write-specific"],          # 5     #####
    "modify": ["-ms", "--modify-specific",          # 5     #####
               "-ma", "--modify-all",               # 4     ####
               "-mas", "--modify-all-specific"],    # 4 1   #####
    "remove": ["-rmsub", "--remove-substring",      # 4     ####
               "-rms", "--remove-specific",         # 4     ####
               "-rmas", "--remove-all-specific"],   # 4     ####
    "clear":  ["-cl", "--clear-line",               # 3     ###
               "-ca", "--clear-all"],               # 2     ##
    "read":   ["-rl", "--read-line",                # 3     ###
               "-ra", "--read-all"],                # 2     ##
    "create": [],                                   # 2     ##
    "open":   ["-r", "--read",                      # 3     ###
               "-w", "--write",                     # 3     ###
               "-cp", "--copy"],                    # 3     ###
    "close":  ["-c", "--close"],                    # 3     ###
    "delete": ["-d", "--delete"],                   # 3     ###
}

command_handler = {
    "write":  commands.write,
    "modify": commands.modify,
    "remove": commands.remove,
    "clear":  commands.clear,
    "read":   commands.read,
    "create": commands.create,
    "open":   commands.open,
    "close":  commands.close,
    "delete": commands.delete
}

while True:
    user_input = input("microfilesys: ").split()
    
    # continue when theres no input
    if not user_input:
        print("empty input, try again")
        continue
    elif len(user_input) == 1 and user_input[0] in ["quit", "exit"]:
        exit()
    
    user_command = user_input[0]
    # seperate all the parameter list lenght
    if len(user_input) == 2 and user_input[0] == "create":
        command_handler[user_command](user_input[1])
    elif len(user_input) == 3 and user_input[0] in ["clear", "read"] and user_input[1] in command_flags.get(user_input[0], []):
        command_handler[user_command](user_input[1], user_input[2], user_input[3], user_input[4], user_input[5])



    elif len(user_input) >=  len(user_input) <= 6 and user_input[1] in command_flags.get(user_input[0], []):
        command_handler[user_command](user_input[1], user_input[2], user_input[3], user_input[4], user_input[5])
    else:
        print("command incorrect")