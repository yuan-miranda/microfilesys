def get_content(command_parts, content_index):
    return ' '.join(command_parts[content_index:])[1:-1]

# check if the input is a content
def is_content(command_parts, content_index):
    string = ' '.join(command_parts[content_index:]) 
    content_start = string[0]
    content_end = string[-1]

    # early return if the content has more or less than double quotes on it
    # prevent: a", a"", '"a"'
    if content_start != '"' and string.count('"') != 2:
        print(f"missing \" on the start of the content: {string}")
        return False
    
    # prevent: "a, ""a, '"a"'
    if content_end != '"' and string.count('"') != 2:
        print(f"missing \" on the end of the content: {string}")
        return False
    
    if string.count('"') != 2:
        print(f"'{string}' is not a valid content, use pair of double quoation mark when enclosing a content i.e. \"some string\"")
        return False
    
    

    return True

def parse_command(command_input):
    command_parts = command_input.split()
    length = len(command_parts)

    command = command_parts[0]
    option  = command_parts[1] if length >= 2 else None
    line    = command_parts[2] if length >= 3 else None
    content = command_parts[3] if length >= 4 else None


    # read
    if command == "read":
        # no option provided
        if not option:
            print("no option provided")
            return
        
        # option is -l
        if option == '-l':
            # expected line after -l
            if length == 2:
                print("expexted line number after -l")
            # correct line format
            elif length == 3:
                # valid line
                if line and line.isdigit():
                    print("line")
                    pass # call read line
                # line is NaN
                else:
                    print("line not number")
            # invalid line format
            else:
                print("invalid line length")

        # option is -all
        elif option == '-all':
            # correct line format
            if length == 2:
                print("all")
                pass # call read all
            # invalid line format
            else:
                print("invalid all length")
        # invalid read option
        else:
            print("invalid option")
    
    # write
    elif command == "write":
        # no option provided
        if not option:
            print("no option provided")
            return

        # option is -l
        if option == '-l':
            # expected line after -l
            if length == 2:
                print("expexted line number after -l")
            # expected content
            elif length == 3:
                if line and line.isdigit():
                    print("expected content after line")
                else:
                    print("line not number")
                    
            elif length >= 4:
                if is_content(command_parts, 3):
                    print(get_content(command_parts, 3))
            else:
                print("invalid line length")

        elif option == '-end':
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
    arg = input()
    if arg:
        parse_command(arg)