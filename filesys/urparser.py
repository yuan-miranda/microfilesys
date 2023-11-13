"""A Minimalist MicroPython(u) REPL Parser

This module is inspired by argparse and is made with the use of GPT-3.
"""

class Urparser:
    def __init__(self):
        self.arguments = {} # keeps track of argument names
        self.display_help = False

    def add_argument(self, arg_names, value_type=str, default_value=None, description=""):
        """adds a new argument for the parser.\n
        Parameters:
        - arg_names - argument name (no shit).
        - value_type - argument value datatype.
        - default_value - argument default value (default=None).
        - description - describe the argument.

        Restrictions:
        - argument names must be string literal.
        - nested list is not supported as a argument name.
        - use string/list for single argument i.e. "-i", ["-i"].
        - use list for multi argument i.e. ["-i", "--input"].
        """

        # store single argument to a list for consistency.
        if isinstance(arg_names, str):
            arg_names = [arg_names]
        
        # throw a ValueError when user tries to pass a nested list as a argument.
        if any(isinstance(argument_name, list) for argument_name in arg_names):
            raise ValueError("Nested lists are not allowed for argument names.")

        # store each argument_name on self.arguments dict where argument_name is the key.
        for arg_name in arg_names:
            self.arguments[arg_name] = {
            "value_type": value_type,
            "default_value": default_value,
            "description": description,
            "value": None
        }

    def parse_argument(self, args):
        """parse the argument.\n
        Parameters:
        - args - user provided input.

        Restrictions:
        - flags can repeat, last flag would take value precedence.
        - flag cant store another flag as a value i.e. "-o -i 20".
        """

        # store previous flag.
        previous_flag_option = None

        for current_arg in args:
            # print help page.
            if current_arg == '-h' or current_arg == '--help':
                self.show_help = True
                return

            # example: "-i 20"

            # current_arg is a flag.
            if current_arg.startswith('-'):

                # check if theres a previous flag.
                if previous_flag_option is not None:
                    
                    # check if the previous_flag_option is a key to self.arguments dictionary.
                    if self.arguments.get(previous_flag_option):
                        # if theres a flag before this flag that has no value provided.

                        # example: "-i -i 20"
                        # {'-i': {'value': True}, '-i': {'value': None}}
                        self.arguments[previous_flag_option]['value'] = True
                
                # store the current_arg in previous_flag_option.
                previous_flag_option = current_arg

            # current_arg is not a flag.
            else:
                if previous_flag_option is not None:

                    if self.arguments.get(previous_flag_option):
                        # pass current_arg as a value of the previous flag.

                        # example: {'-i': {'value': 20}}
                        self.arguments[previous_flag_option]['value'] = current_arg

                # clear the previous_flag_option because current_arg is not a flag to store.
                previous_flag_option = None 
        
        # handle cases where the last argument is a flag without value.
        if previous_flag_option is not None:
            if self.arguments.get(previous_flag_option):
                self.arguments[previous_flag_option]['value'] = True
    
    def get_value(self, arg_name):
        return self.arguments.get(arg_name, {}).get('value')
    
    def print_help(self):
        # Display help information for the defined arguments.
        print("Usage:")
        for arg_name, arg_info in self.arguments.items():
            value_type = arg_info['value_type'].__name__
            description = arg_info['description']
            default_value = arg_info['default_value']

            if default_value is not None:
                print(f"  {arg_name} [{value_type}]: {description} (default: {default_value})")
            else:
                print(f"  {arg_name} [{value_type}]: {description}")