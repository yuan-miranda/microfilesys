# read all file content

def read_whole_file(file):
    with open(file, 'r') as f:
        return f.read() # read whole file

print(read_whole_file("../../todo"))