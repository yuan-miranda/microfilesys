available_commands = [
    'read',
    'write',
    'clear',
    'help'
]

def read(command_parts):
    option = command_parts[1] if len(command_parts) in [2, 3] else None
    line = command_parts[2] if len(command_parts) == 3 and command_parts[2].isdigit() else None

    if option == "-ln":
        if len(command_parts) == 3:
            if line:
                line = command_parts[2]
                print(f"reading line {line}")
                return line
            else:
                line = command_parts[2]
                print(f"'{line}' is not a valid line argument")
        else:
            print(f"line argument expected after '-ln'")

    elif option == "-all":
        if len(command_parts) == 2:
            if not line:
                print("reading all line")
                return
                # read all file content
            else:
                print("doesnt need an line argument after '-all'")
        else:
            print("invalid argument length for read -all command'")
    else:
        print(f"option must be -ln or -all but instead its {option}")

def parse_command(args):
    command_parts = args.split()
    command = command_parts[0]
    if command not in available_commands:
        print("invalid command")
        return
    
    if command == "read":
        read(command_parts)

args = "read -ln 1"
result = parse_command(args)
print(result)