## Micropython File Editor System (microfilesys)
A basic console-like file editor program designed for the Raspberry Pi Pico, capable of performing basic file operations such as creating and deleting files, as well as reading and writing to a file.

> [microfilesys.py](https://github.com/yuan-miranda/microfilesys/blob/main/microfilesys.py) source code of the program.<br>

## Usage
```
Syntax:
    open <-f path="file.txt">                       Open a file for editing (used to access file editor mode).
    create <-f | -d> <path="file.txt">              Create a file or folder in the specified path.
    delete <-f | -d> <path="file.txt">              Delete a file or folder in the specified path.

    read <-l line=int | -a | -af>                   Read the content from the file.
    write <-l | -e> <line=int content="string">     Write content to the file.
    clear <-l line=int | -a>                        Clear the content of from the file but keep the lines.
    remove <-l line=int | -a>                       Remove a line from the file.

    q quit exit                                     Exit the program or go back to file manager mode when in file editor mode.
    h help man manual                               Print out the help page.
    ls list                                         Lis current directory where this script is located and the contents of it.
    v ver version                                   Print out the version of the Microfilesys currently running.

Options:
    -l --line l line                                Specify the line of the file (available: read, write, clear).
    -a --all a all                                  Select all the content of the file (available: read, clear).
    -e --end e end                                  Move the content to the end of the line (available: write).
    -af --all-fast af all-fast                      Used in read command to print the entile file faster (available: read).

    -f --file f file                                Specify that the file argument is an file (available: opem, create, delete).
    -d -dir --directory d dir directory             Specify that the file argument is an folder (available: create, delete).

Argument:
    line=int                                        Specify the line number to work on, i.e. 1, 10, 69.
    content="string"                                Specify a string to be written to the file, i.e. "example string".
    path="file.txt"                                 Specify the path.
```

## Example commands

| Command                     | Operation                            | Description                                                                       |
|-----------------------------|--------------------------------------|-----------------------------------------------------------------------------------|
| `open --file example.txt`   | open file                            | Open the file named "example.txt" for file editing.                               |
| `create --file file.txt`    | create file                          | Create a new file named "file.txt" on the current directory.                      |
| `create --directory folder` | create directory                     | Create a new directory (folder) named "folder" on the current directory.          |
| `delete --file file.txt`    | delete file                          | Delete the file named "file.txt" on the current directory.                        |
| `delete --directory folder` | delete directory (recursively)       | Delete the directory named "folder" and its content on the current directory.     |
| `read --line 1`             | read line 1                          | Read and display the contents of the first line of the file with line number.     |
| `read --all`                | read all lines                       | Read and display the entire contents of the file with line number indicator.      |
| `read --all-fast`           | read all lines (without line number) | Read and display the entire contents of the file quickly without the line number. |
| `write --line 1 "Lorem"`    | overwrite line                       | Write the string "Lorem" to the first line of the file.                           |
| `write --end 1 " Ipsum"`    | append line end                      | Append the string " Ipsum" to the end of the first line in the file.              |
| `clear --line 1`            | clear line                           | Clear the content of the first line but keep the lines of the file.               |
| `clear --all`               | clear all lines                      | Clear the entire content of the file but keep the lines.                          |
| `remove --line 1`           | remove line                          | Remove the first line from the file.                                              |
| `remove --all`              | remove all lines                     | Remove all lines from the file.                                                   |
