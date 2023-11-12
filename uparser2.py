class CommandParser:
    def __init__(self):
        self.commands = {}

    def add_command(self, command_name, options=[], line=None, content=None):
        self.commands[command_name] = {'options': options, 'line': line, 'content': content}

    def parse_command(self, input_command):
        command_parts = input_command.split()

        if not command_parts:
            print("Error: Empty command")
            return

        command_name = command_parts[0]

        if command_name not in self.commands:
            print(f"Error: Unknown command '{command_name}'")
            return

        command_info = self.commands[command_name]

        # Parse options and arguments
        options = {}
        args = []

        i = 1  # Start from the second part (after the command name)
        while i < len(command_parts):
            part = command_parts[i]

            if part.startswith('-'):
                # Option
                if part in command_info['options']:
                    option_name = part
                    i += 1  # Move to the next part for the option value
                    option_value = command_parts[i] if i < len(command_parts) else None
                    options[option_name] = option_value
                else:
                    print(f"Error: Unknown option '{part}' for command '{command_name}'")
                    return
            else:
                # Argument
                args.append(part)

            i += 1

        # Validate and process the command
        self.process_command(command_name, options, args)

    def process_command(self, command_name, options, args):
        # Implement the logic for each command here
        # You can access the options and arguments as needed
        print(f"Processing command: {command_name}")
        print("Options:", options)
        print("Arguments:", args)


# Example usage:
parser = CommandParser()

# Add commands with their options and parameters
parser.add_command("read", options=['-ln', '-all'], line=1)
parser.add_command("write", options=['-ln', '-end'], line=1, content="write on file")
parser.add_command("clear", options=['-ln', '-all'], line=1)

# Parse input commands
parser.parse_command("write -end 1 'bruh'")
print("\n")
parser.parse_command("read -ln -ln")