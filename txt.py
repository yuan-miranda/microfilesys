def get_content(command_parts, content_index):
    return ' '.join(command_parts[content_index:])[1:-1]

arg = 'hello world "this"'
argsplit = arg.split()
print(get_content(argsplit, 2))