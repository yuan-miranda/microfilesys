# read specified line

def read_line_file(file, line):
    with open(file, 'r') as f:
        return f.readlines()[line - 1] # indexing
    
print(read_line_file("../../todo", 3))