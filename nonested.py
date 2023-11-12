class ArgumentParser:
    def __init__(self):
        # Initialize the ArgumentParser object.
        self.arguments = {}  # Dictionary to store argument information.
        self.show_help = False  # Flag to determine if the user wants to display help.

    def add_argument(self, names, value_type=str, default=None, help_text=""):
        # Define a new argument for the parser.
        # Arguments are defined with a name or a list of names, a value type, a default value, and help text.
        if isinstance(names, str):
            names = [names]  # Convert single string to list for consistency

        if any(isinstance(name, list) for name in names):
            raise ValueError("Nested lists are not allowed for argument names.")

        for name in names:
            self.arguments[name] = {
                'value_type': value_type,
                'default': default,
                'help_text': help_text,
                'value': None,
            }

    def parse_arguments(self, args):
        used_args = set()  # Set to keep track of used arguments.
        current_arg = None  # Initialize a variable to track the current argument being processed.

        for arg in args:
            if arg in ['-h', '--help']:
                # If the user provides the -h or --help option, set the show_help flag and exit parsing.
                self.show_help = True
                return

            if arg.startswith('-'):
                if current_arg is not None:
                    self._process_argument(current_arg, used_args)
                current_arg = arg

            else:
                if current_arg is not None:
                    self._process_argument(current_arg, used_args, arg)
                current_arg = None

        if current_arg is not None:
            self._process_argument(current_arg, used_args)

    def _process_argument(self, current_arg, used_args, value=True):
        if current_arg in used_args:
            raise ValueError(f"Duplicate use of argument: {current_arg}")
        used_args.add(current_arg)

        if self.arguments.get(current_arg):
            self.arguments[current_arg]['value'] = value

    def print_help(self):
        # Display help information for the defined arguments.
        print("Usage:")
        for arg_name, arg_info in self.arguments.items():
            value_type = arg_info['value_type'].__name__
            help_text = arg_info['help_text']
            default = arg_info['default']

            if default is not None:
                print(f"  {arg_name} [{value_type}]: {help_text} (default: {default})")
            else:
                print(f"  {arg_name} [{value_type}]: {help_text}")

    def get_value(self, arg_name):
        # Retrieve the value of the specified argument.
        return self.arguments[arg_name]['value'] if arg_name in self.arguments else None


if __name__ == '__main__':
    arguments = [
        ["-i", "--input", "-hello"],
        ["-o", "--output"],
        "-v"
    ]
    parser = ArgumentParser()
    parser.add_argument(arguments[0], int, help_text="Input number")
    parser.add_argument(arguments[1], str, default="output.txt", help_text="Output filename")
    parser.add_argument(arguments[2], bool, help_text="Enable verbose mode")

    while True:
        user_input = input("Enter command: ")
        if not user_input:
            break

        args = user_input.split()
        parser.parse_arguments(args)
        break

    if parser.show_help:
        parser.print_help()
    else:
        input_number = parser.get_value('-i')
        output_filename = parser.get_value('-o')
        verbose_mode = parser.get_value('-v')

        print(f"Input Number: {input_number}")
        print(f"Output Filename: {output_filename}")
        print(f"Verbose Mode: {verbose_mode}")
