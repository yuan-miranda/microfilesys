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


# Blessed are thy people who will read this code in the future
def parse_command(command_input):
    command_parts = command_input.split()
    command_join = ' '.join(command_parts)
    length = len(command_parts)

    command = command_parts[0]
    option  = command_parts[1] if length >= 2 else None
    line    = command_parts[2] if length >= 3 else None
    content = command_parts[3] if length >= 4 else None

    # no option provided
    if not option:
        print("no option provided")
        return

    # command read
    if command == "read":
        # option -l
        if option == '-l':
            if length == 2:
                print("expexted line number after -l")
            elif length == 3:
                if line and line.isdigit():
                    print("line")
                    pass # call read line
                else:
                    print("line not number")
            else:
                print("invalid line length")

        # option -a
        elif option == '-a':
            if length == 2:
                print("all")
                pass # call read all
            else:
                print("invalid all length")
        else:
            print("invalid option")
    
    # command write
    elif command == "write":
        # option -l
        if option == '-l':
            if length == 2:
                print("expexted line number after -l")
            elif length == 3:
                if line and line.isdigit():
                    print(f"expected content after line: {command_join} \"example content\"")
                else:
                    print("line not number")
                    
            elif length >= 4:
                if is_content(command_parts, 3):
                    print(get_content(command_parts, 3))
                    pass # call write line
            else:
                print("invalid line length")

        # option -end
        elif option == '-e':
            if length == 2:
                print("expexted line number after -e")
            elif length == 3:
                if line and line.isdigit():
                    print(f"expected content after line: {command_join} \"example content\"")
                else:
                    print("line not number")
            elif length >= 4:
                if is_content(command_parts, 3):
                    print(get_content(command_parts, 3))
                    pass # call write line
            else:
                print("invalid line length")
        else:
            print("invalid option")

    # command clear
    elif command == "clear":
        # option -l
        if option == '-l':
            if length == 2:
                print("expexted line number after -l")
            elif length == 3:
                if line and line.isdigit():
                    print("line")
                    pass # call read line
                else:
                    print("line not number")
            else:
                print("invalid line length")

        # option -a
        elif option == '-a':
            if length == 2:
                print("all")
                pass # call read all
            else:
                print("invalid all length")
        else:
            print("invalid option")
    else:
        print("invalid command")

while True:
    try:
        arg = input()
    except KeyboardInterrupt:
        exit()
    if arg:
        parse_command(arg)