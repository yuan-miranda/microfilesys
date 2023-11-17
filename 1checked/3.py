def find_indices_of_char(string, char):
    indices = []
    for i in range(len(string)):
        if string[i] == char:
            indices.append(i)
    return len(indices)

# Example usage
string = '"""""""'
char_to_find = '"'
indices = find_indices_of_char(string, char_to_find)

print(f'Indices of {char_to_find} in the string: {indices}')







file_editor_command_handler = {
    "help": [],
    "read": {
        "-ln": Command.read.line,
        "-all": Command.read.all
    },
    "write": {
        "-ln": Command.write.line,
        "-end": Command.write.end
    },
    "clear": {
        "-ln": Command.clear.line,
        "-all": Command.clear.all
    }
}

snek = {
    "help": [],
    "read": {
        "-ln": 3,
        "-all": 2
    },
    "write": {
        "-ln": 4,
        "-end": 4
    },
    "clear": {
        "-ln": 3,
        "-all": 2
    }
}