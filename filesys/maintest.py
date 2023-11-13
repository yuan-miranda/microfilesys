class ArgumentParser:
    def __init__(self):
        # Initialize the ArgumentParser object.
        self.arguments = {}  # Dictionary to store argument information.
        self.show_help = False  # Flag to determine if the user wants to display help.

    def add_argument(self, name, value_type=str, default=None, help_text=""):
        # Define a new argument for the parser.
        # Arguments are defined with a name, a value type, a default value, and help text.
        self.arguments[name] = {
            'value_type': value_type,  # Type of value expected for the argument.
            'default': default,  # Default value for the argument.
            'help_text': help_text,  # Description of the argument.
            'value': None,  # The actual value provided by the user (initialized as None).
        }

    def parse_arguments(self, args):
        current_arg = None  # Initialize a variable to track the current argument being processed.

        for arg in args:
            if arg == '-h' or arg == '--help':
                # If the user provides the -h or --help option, set the show_help flag and exit parsing.
                self.show_help = True
                return

            if arg.startswith('-'):
                if current_arg is not None:
                    # If an argument was already in progress, and the current_arg is not None...
                    if self.arguments.get(current_arg):
                        self.arguments[current_arg]['value'] = True
                    # ...mark it as a flag (e.g., -v, -o) by setting its value to True.

                current_arg = arg  # Update the current argument being processed.

            else:
                if current_arg is not None:
                    # If there was a current argument and the current arg is not None...
                    if self.arguments.get(current_arg):
                        self.arguments[current_arg]['value'] = arg
                    # ...set its value to the value provided by the user.

                current_arg = None  # Reset the current argument to None as a new argument may start.

        if current_arg is not None:
            if self.arguments.get(current_arg):
                self.arguments[current_arg]['value'] = True

    def get_value(self, name):
        # Get the value associated with a specific argument name.
        return self.arguments.get(name, {}).get('value')

    def print_help(self):
        # Display help information for the defined arguments.
        print("Usage:")
        for arg_name, arg_info in self.arguments.items():
            value_type = arg_info['value_type'].__name__
            help_text = arg_info['help_text']
            default = arg_info['default']

            if default is not None:
                # If a default value is specified, display it.
                print(f"  {arg_name} [{value_type}]: {help_text} (default: {default})")
            else:
                # If no default value is specified, display the argument without a default value.
                print(f"  {arg_name} [{value_type}]: {help_text}")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', int, help_text="Input number")
    parser.add_argument('-o', str, default="output.txt", help_text="Output filename")
    parser.add_argument('-v', bool, help_text="Enable verbose mode")

    while True:
        user_input = input("enter command: ")
        args = user_input.split()
        if not args:
            continue

        parser.parse_arguments(args)
        break

    if parser.show_help:
        # If the show_help flag is set, display the help message and exit.
        parser.print_help()
    else:
        # Retrieve the values of the parsed arguments.
        input_number = parser.get_value('-i')
        output_filename = parser.get_value('-o')
        verbose_mode = parser.get_value('-v')

        # Display the parsed argument values.
        print(f"Input Number: {input_number}")
        print(f"Output Filename: {output_filename}")
        print(f"Verbose Mode: {verbose_mode}")
