## Micropython File Editor System (microfilesys)
A basic console-like file editor program designed for the Raspberry Pi Pico, capable of performing basic file operations such as creating and deleting files, as well as reading and writing to a file.

> [microfilesys.py](https://github.com/yuan-miranda/microfilesys/blob/main/microfilesys.py) source code of the program.<br>

## Usage
List the files and directories in the specified directory. If no directory is provided, it lists the files and directories in the current directory.
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
make <--file | --directory | --path> <filename>
```
Delete file/directory/path.
```
delete <--file | --directory | --path> <filename>
```
Read the contents of the specified line or the entire file. If --indicator is provided, it displays line numbers.
```
read [--line <line> | --all] [--indicator]
```
Write string to the specified line or at the end of the file. If no line is specified, it writes to the current line. If --all is provided, it overwrites the entire file.
```
write [--line <line> | --end [line] | --all] ["string"]
```
Clear the contents of the specified line or the entire file.
```
clear <--line <line> | --all>
```
Remove the specified line or all lines from the file.
```
remove <--line <line> | --all>
```
Exit the program.
```
q, quit, exit
```
Display the help text.
```
h, help, ?
```
Display the program's version.
```
v, version
```
Close the currently opened file.
```
close
```
Undo the last edit operation.
```
undo
```
Redo the last undo edit operation.
```
redo
```

## Example Commands
| Command                           | Operation                                             |
|-----------------------------------|-------------------------------------------------------|
| `ls`                              | List the current directory                            |
| `cd ..`                           | Go to the parent directory                            |
| `open file.txt`                   | Open a file named file.txt (must exists)              |
| `make file.txt`                   | Create a file named "file.txt                         |
| `make somefolder`                 | Create a folder named "somefolder"                    |
| `delete file.txt`                 | Delete a file                                         |
| `read --line 1`                   | Read the first line of the file                       |
| `read --all --indicator`          | Read all the content of the file with line number     |
| `write --end 1 "Hello, World!"`   | Write "Hello, World!" on the first line of the file   |
| `write --all ""`                  | Clears all the content of the file                    |
| `clear --line 1`                  | Clear the content of the first line of the file       |
| `remove --line 1`                 | Remove the first line of the file                     |
| `q, quit, exit`                   | Exit the program                                      |
| `h, help, ?`                      | Display the help text                                 |
| `v, version`                      | Display the program's version                         |
| `close`                           | Close the currently opened file                       |
| `undo`                            | Undo the last edit operation                          |
| `redo`                            | Redo the last undo edit operation                     |

## Setup
Packages used here come by default so no need for additional package installation, but if you insist:
```
pip install os sys
```