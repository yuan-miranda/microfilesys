## Micropython File Editor System (microfilesys)
A basic console-like file editor program designed for the Raspberry Pi Pico, capable of performing basic file operations such as creating and deleting files, as well as reading and writing to a file.

> [microfilesys.py](https://github.com/yuan-miranda/microfilesys/blob/main/microfilesys.py) source code of the program.<br>

## Usage
List the files and directories in the specified directory.
> If no directory is provided, it lists the files and directories in the current directory.
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
> If 'string' is not specified, it does nothing.
```
write [--line <line> | --end [line] | --all] [string]
```
Clear the contents of the file.
```
clear <--line <line> | --all>
```
Remove the contents of the file.
```
remove <--line <line> | --all>
```
Exit the program.
```
q, quit, exit
```
Display the help text.
> You can also call the command name alone and it will print its usage description.
```
h, help, ?
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
| Command                         | Operation                                             |
|---------------------------------|-------------------------------------------------------|
| ls                              | List the current directory                            |
| cd ..                           | Go to the parent directory                            |
| open file.txt                   | Open a file named file.txt (must exists)              |
| make --file file.txt            | Create a file named "file.txt                         |
| make --directory somefolder     | Create a folder named "somefolder"                    |
| delete --file file.txt          | Delete a file                                         |
| read --line 1                   | Read the first line of the file                       |
| read --all --indicator          | Read all the content of the file with line number     |
| write --end 1 "Hello, World!"   | Write "Hello, World!" on the first line of the file   |
| write --all ""                  | Clears all the content of the file                    |
| clear --line 1                  | Clear the content of the first line of the file       |
| remove --line 1                 | Remove the first line of the file                     |
| q, quit, exit                   | Exit the program                                      |
| h, help, ?                      | Display the help text                                 |
| close                           | Close the currently opened file                       |
| undo                            | Undo the last edit operation                          |
| redo                            | Redo the last undo edit operation                     |

## Installation:
**Note: You must have `Git` and `Python 3` or above installed prior to this setup.**
1. Clone the repository on your machine:
> Note: No need to clone the repository, you can even just download or copy the contents of [microfilesys.py](https://github.com/yuan-miranda/microfilesys/blob/main/microfilesys.py) and it will still work fine.<br>
```
git clone https://github.com/yuan-miranda/microfilesys.git
```
2. Modules used here come by default so no need for additional module installation, but if you insist:
```
pip install os sys
```
3. Run the script by executing the command below:
```
python microfilesys.py
```
