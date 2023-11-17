def parse_command(command_str):
    # Split the command string into tokens
    tokens = command_str.split()

    # Check if the command is "read"
    if tokens[0] != "read":
        raise ValueError("Invalid command. Expected 'read'.")

    # Check if there are enough tokens
    if len(tokens) < 2:
        raise ValueError("Invalid command. Missing options.")

    # Extract the options and values
    options = {}
    i = 1
    while i < len(tokens):
        option = tokens[i]
        if option == '-ln':
            # Check if there's a value after -ln
            if i + 1 < len(tokens):
                options['-ln'] = int(tokens[i + 1])
                i += 2
            else:
                raise ValueError("Invalid command. Missing value after -ln.")
        elif option == '-all':
            options['-all'] = True
            i += 1
        else:
            raise ValueError(f"Invalid option: {option}")

    return options

# Example usage
command_str = "read -all 1"
try:
    options = parse_command(command_str)
    print(options)
except ValueError as e:
    print(f"Error: {e}")
