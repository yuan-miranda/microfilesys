# Micropython File Editor System (microfilesys)

A basic console-like file editor program designed for the Raspberry Pi Pico, capable of performing basic file operations such as creating and deleting files, as well as reading and writing to a file.

![image](https://github.com/user-attachments/assets/b67d947a-f671-4d86-82c8-3840b41149a0)

## Install

Clone the repository and run the script

```
git clone https://github.com/yuan-miranda/microfilesys.git
```

```
cd microfilesys
```

```
python .\main.py
```

## Usage

> **NOTE:** This script was developed for RPI PIco W using MicroPython, but it can be run on Windows, Linux, and Mac. Run the `main.py` first to open the repl.

```
python .\main.py
```

### For a generic help page

> You can also call the command name alone and it will print its usage description.

```
h, help, ?
```

List the files and directories in the specified directory.

> If no directory is provided, it lists the content of the current directory.

```
ls [directory]
```

Change current directory.

```
cd <directory>
```

Open file for editing.

```
open <file>
```

Create file/directory/path.

```
make <--file | --directory | --path> <filename>...
```

Delete file/directory/path.

```
delete <--file | --directory | --path> <filename>...
```

Read the contents of the file.

> If --indicator is specified it prints the lines with preceeding line numbers.

```
read [--line <line> | --all] [--indicator]
```

Write to the file.

> If text is not encased with i.e '"Hello, World!"' or not specified, it does nothing.

```
write [--line <line> | --end [line] | --all] ["string"]
```

Clear the contents of the file.

```
clear <--line <line> | --all>
```

Remove the contents of the file.

```
remove <--line <line> | --all>
```

Close the currently opened file.

```
close
```

Undo the last text operation.

```
undo
```

Redo the last undo action.

```
redo
```

Exit the program.

```
q, quit, exit
```

## Example Commands

| Command                       | Operation                                           |
| ----------------------------- | --------------------------------------------------- |
| ls                            | List the current directory                          |
| cd ..                         | Go to the parent directory                          |
| open file.txt                 | Open a file named file.txt (must exists)            |
| make --file file.txt          | Create a file named "file.txt                       |
| make --directory somefolder   | Create a folder named "somefolder"                  |
| delete --file file.txt        | Delete a file                                       |
| read --line 1                 | Read the first line of the file                     |
| read --all --indicator        | Read all the content of the file with line number   |
| write --end 1 "Hello, World!" | Write "Hello, World!" on the first line of the file |
| write --all ""                | Clears all the content of the file                  |
| clear --line 1                | Clear the content of the first line of the file     |
| remove --line 1               | Remove the first line of the file                   |
| q, quit, exit                 | Exit the program                                    |
| h, help, ?                    | Display the help text                               |
| close                         | Close the currently opened file                     |
| undo                          | Undo the last edit operation                        |
| redo                          | Redo the last undo edit operation                   |

## Contributing

PRs accepted.
