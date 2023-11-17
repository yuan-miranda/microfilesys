import os

class commands:
    def write(text):
        print(text)
    def modify(text):
        print(text)
    def remove(text):
        print(text)
    def clear(text):
        print(text)
    def read(text):
        print(text)
    def create(text):
        print(text)
    def open(text):
        print(text)
    def close(text):
        print(text)
    def delete(text):
        print(text)

flags = {
    "write":  [commands.write, "-we", "--write-end", "-ws", "--write-specific"],
    "modify": [commands.modify, "-ms", "--modify-specific", "-ma", "--modify-all", "-mas", "--modify-all-specific"],
    "remove": [commands.remove, "-rmsub", "--remove-substring", "-rms", "--remove-specific", "-rmas", "--remove-all-specific"],
    "clear":  [commands.clear, "-cl", "--clear-line", "-ca", "--clear-all"],
    "read":   [commands.read, "-rl", "--read-line", "-ra", "--read-all"],
    "create": [commands.create],
    "open":   [commands.open, "-r", "--read", "-w", "--write", "-cp", "--copy"],
    "close":  [commands.close, "-c", "--close"],
    "delete": [commands.delete, "-d", "--delete"],
}

# Returns True if input_command is a flags key
def is_command(input_command):
    return input_command in flags
# 
def make_list(text):
    return text.split()
def validate_command_flag(input):
    return input[1] in flags.get(input[0], []) if is_command(input[0]) else False

while True:
    user_input = make_list(input("microfilesys: "))

    if not user_input:
        continue
    elif len(user_input) == 1 and (user_input[0] == "quit" or user_input[0] == "q" or user_input[0] == "exit"):
        exit()
    command = user_input[0]

    if len(user_input) == 1 and user_input[0] == "create":
        flags[command][0](user_input)
    elif len(user_input) > 1 and validate_command_flag(user_input):
        flags[command][0](user_input)
    else:
        print("command inccorrect")





command_flags = {
    "write":  ["-we", "--write-end", "-ws", "--write-specific"],
    "modify": ["-ms", "--modify-specific", "-ma", "--modify-all", "-mas", "--modify-all-specific"],
    "remove": ["-rmsub", "--remove-substring", "-rms", "--remove-specific", "-rmas", "--remove-all-specific"],
    "clear":  ["-cl", "--clear-line", "-ca", "--clear-all"],
    "read":   ["-rl", "--read-line", "-ra", "--read-all"],
    "create": [],
    "open":   ["-r", "--read", "-w", "--write", "-cp", "--copy"],
    "close":  ["-c", "--close"],
    "delete": ["-d", "--delete"],
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
    if len(user_input) == 2 and user_input[0] == "create":
        command_handler[user_command](user_input[1])
    
    elif len(user_input) > 1 and user_input[1] in command_flags.get(user_input[0], []):
        command_handler[user_command]()
    elif len(user_input) ==
    else:
        print("command incorrect")