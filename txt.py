command_input = "read -l 1"

command_parts = command_input.split()
command_length = len(command_parts)

command = command_parts[0]
# valid option length and option format          = command_parts[1] (valid option)
# valid option length and invalid option format  = command_parts[1] (invalid option)
# all invalid                                     = None            (no option)
option = command_parts[1] if command_length in [2, 3] and command_parts[1].startswith('-') else command_parts[1]\
                          if command_length in [2, 3] else ""

# valid length and is number          = command_parts[2] (valid line)
# valid length nan                    = command_parts[2] (invalid line)
# all invalid                         = None             (no line)
line = command_parts[2]   if command_length == 3 and command_parts[2].isdigit() else command_parts[2]\
                          if command_length == 3 else None

if option == '-l':
    print("-l")
else:
    print("not -l")
