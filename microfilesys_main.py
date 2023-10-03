# FIX COMMAND HANDLING HERE 10/2 (done)

import os

class Command:
    def create_file(file):
        if file in os.listdir():
            print(f"'{file}' already exist")
        else:
            with open(file, "w") as f:
                print(f"'{file}' created")

    def delete_file(file):
        if file not in os.listdir():
            print(f"'{file}' doesnt exist")
        else:
            os.remove(file)
            print(f"'{file}' deleted")

    def open_file(file, mode):
        if mode not in ["-r", "-w"]:
            print(f"'{mode}' is not a valid file access mode, use '-r' for read and '-w' for write")
            return
    
        mode = "r" if mode == "-r" else "r+"
        file_editor(file, mode)

    def readln(): # read -ln | -all 1
        print("readln")
    def readall():
        print("readall")

    def writeln(): # write -ln | -end 2 "Hello"
        print("writeln")
    def writeend():
        print("writeend")

    def clearln():  # clear -ln | -all 2
        print("clearln")
    def clearall():
        print("clearall")

def file_editor(file, mode):
    running = True
    with open(file, mode) as f:
        while running:
            try:
                user_input = input(f"microfilesys-{file}: ")
                if not user_input:
                    continue
                command_args = user_input.split()
                command_args_len = len(command_args)
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                return

            cmd = command_args[0]
        
            if cmd in ["exit", "quit", 'q']:
                running = False
            elif cmd == "help":
                if command_args_len == 2 and command_args[1] in ["-h", "-help"]:
                    print("Usage:")
                    print("\tread (-ln line=1 | -all)")
                    print("\twrite (-ln | -end) line=1 content=\"string\"")
                    print("\tclear (-ln line=1 | -all)")

            elif cmd == "read":
                if command_args_len == 2 and command_args[1] == "-all":
                    Command.readall
                elif command_args_len == 3 and command_args[1] == "-ln":
                    Command.readln()
                else:
                    print(f"Expected 'read (-ln line=1 | -all)'")

            elif cmd == "write":
                if command_args_len == 4 and command_args[1] == "-end":
                    Command.writeend()
                elif command_args_len == 4 and command_args[1] == "-ln":
                    Command.writeln()
                else:
                    print(f"Expected 'write (-ln | -end) line=1 content=\"string\"'") # STUDY ARGPARSE AND CONVENTION OF PROGRAMMING COMMAND LINE 10/3

            elif cmd == "clear":
                if command_args_len == 2 and command_args[1] == "-all":
                    Command.readall
                elif command_args_len == 3 and command_args[1] == "-ln":
                    Command.readln()
                else:
                    print(f"Expected 'clear (-ln line=1 | -all)'")
    
            else:
                print("Invalid Input")
def file_manager():
    running = True
    while running:
        try:
            user_input = input("microfilesys: ")
            if not user_input:
                continue
            command_args = user_input.split()
            length_of_command_args = len(command_args)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            exit()

        cmd = command_args[0]
        
        if cmd in ["exit", "quit", 'q']:
            running = False

        elif cmd == "create":
            if length_of_command_args == 2:
                Command.create_file(command_args[1])
            else:
                print(f"Expected 'create filename'")

        elif cmd == "delete":
            if length_of_command_args == 2:
                Command.delete_file(command_args[1])
            else:
                print(f"Expected 'delete filename'")

        elif cmd == "open":
            if length_of_command_args == 3:
                Command.open_file(command_args[2], command_args[1])
            else:
                print(f"Expected 'open -mode filename'")
        else:
            print("Invalid Input")

def main():
    file_manager()
        
if __name__ == "__main__":
    main()