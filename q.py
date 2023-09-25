filename = 'q.txt'

with open(filename, 'r') as file:
    lines = len(file.readlines())
    #line_count = len(lines)

print(f"The number of lines in '{filename}' is: {lines}")
