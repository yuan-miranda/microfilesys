### Micropython File Editor System (microfilesys)
A basic console-like file editor program designed for the Raspberry Pi Pico, capable of performing basic file operations such as creating and deleting files, as well as reading and writing to a file.

> [microfilesys.py](https://github.com/yuan-miranda/microfilesys/blob/main/microfilesys.py) source code of the program.<br>

### Usage

```
Syntax:
    create <file>                                   Create a file in the current directory.
    open <file>                                     Open a file (used to access file editor mode).
    delete <file>                                   Delete a file in the current directory.

    read <-l line=int | -a>                         Read the content from the file.
    write <-l | -e> <line=int content="string">     Write content to the file.
    clear <-l line=int | -a>                        Clear the content of from the file but keep the lines.
    remove <-l line=int | -a>                       Remove line of the file.

    q quit exit                                     exit the program or go back to file manager mode when in file edior mode.
    h help man manual                               prints out the help page.
    ls list                                         list current directory and files.

Options:
    -l --line l line                                Specify the line of the file (available: read, write, clear).
    -a --all a all                                  Select all the content of the file (available: read, clear).
    -e --end e end                                  Move the content to the end of the line (available: write).
    
Argument:
    line=int                                        Specify the line number to work on, i.e. 1, 10, 69.
    content="string"                                Specify a string to be written to the file, i.e. "example string".
```
### Example

Write 'print("Hello, World!")' at the first line of the file (must open a file first).
```Shell
write --line 1 "print("Hello, World!")"
```
Read the content of line 10 of the file.
```Shell
read -l 10
```
Delete the file named "example.txt".
```Shell
delete example.txt
```