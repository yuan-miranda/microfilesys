class Urparser:
    def __init__(self) -> None:
        self.commands = {}
    
    def add_command(self, command_name, options=[], line_required=None, argument_required=None):
        if not isinstance(command_name, str):
            raise ValueError("String literal is only allowed for command name")
        
        self.commands[command_name] = {
            'options': options,
            'line': line_required,
            'argument': argument_required
        }

    def parse_argument(self, input_command):
        command_parts = input_command.split()
        command_name = command_parts[0]

        if command_name not in self.commands:
            print(f"Unknown command: {command_name}")
            return



    def get_value():
        pass


if 



parser = Urparser()
parser.add_command("read", options=[{'-ln': {'line_num': 0}}, '-all'])
parser.add_command("clear", options=[{'-ln': {'line_number': 0}}, '-all'])
parser.add_command("write", options=['-ln', '-all'], line_required=True, argument_required=True)
parser.parse_argument("read -ln 1")