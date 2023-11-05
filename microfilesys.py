import os

def file_length(filename):
    """
    returns the file length of the specified file.
    """
    with open(filename, 'r') as file:
        return len(file.readlines())
    
def in_line_length(lines, line_number):
    """
    idk whats this.
    """
    if line_number > 0 and line_number <= len(lines):
        pass

def get_content(content):
    """
    concatenates the array list of content into one string.
    """
    return ' '.join(content)[1:-1]

def is_content(content):
    """
    check if the content has opening and closing double quote.
    """
    content_start = content[0]
    content_end = content[-1]
    
    # early return if the content has no opening and closing double quote.
    if content.count('"') != 2:
        print("use pair of '\"' to enclose the content ex: \"content\"")
        return False
    
    # prevent: a", a"", '"a"'
    if content_start != '"':
        print("missing '\"' on the start of the content")
        return False
    
    # prevent: "a, ""a, '"a"'
    if content_end != '"':
        print("missing '\"' on the end of the content")
        return False

    return True

def is_file(filename):
    return filename in os.listdir()

class Command:
    class help:
        @staticmethod
        def display_help():
            print("file editor commands")
            print("Usage:")
            print("\tread (-ln line=1 | -all)")
            print("\twrite (-ln | -end) line=1 content=\"str\"")
            print("\tclear (-ln line=1 | -all)")

            print("file manager commands")
            print("Usage:")
            print("\tcreate file")
            print("\tdelete file")
            print("\topen file")

    class create:
        @staticmethod
        def file(filename):
            if is_file(filename):
                print(f"'{filename}' already exist")
            else:
                with open(file, "w") as file:
                    print(f"'{filename}' created")
    
    class delete:
        @staticmethod
        def file(filename):
            if not is_file(filename):
                print(f"'{filename}' doesnt exist")
            else:
                os.remove(filename)
                print(f"'{filename}' deleted")

    class open:
        @staticmethod
        def file(filename):
            if not is_file(filename):
                print(f"'{filename}' doesnt exist")
            else:
                file_editor(filename)

    class read:
        def line(filename, line):
            with open(filename, 'r') as file:
                try:
                    print("____________________________________________________________")
                    print(f.readlines()[int(line) - 1].rstrip('\n')) # read specified line
                    print("____________________________________________________________")
                except IndexError:
                    print(f"IndexError: '{file}' is only {file_length(file)} lines long not {line}.")

        @staticmethod
        def all(filename):
            with open(filename, 'r') as file:
                print("____________________________________________________________")
                print(f.read()) # read whole file
                print("____________________________________________________________")

    class write:
        @staticmethod
        def line(filename, line, content):
            print("writeln")

        @staticmethod
        def end(filename, line_length, content):
            with open(filename, 'r+') as file:
                line = file.readlines()

                if line_length > 0 and line_length <= len(line):
                    pass
                else:
                    pass

def file_editor(filename):
    pass
def file_manager(filename):
    pass
def main():
    file_manager()

if __name__ == "__main__":
    main()