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

## Setup
Packages used here come by default so no need for additional package installation, but if you insist:
```
pip install os sys
```