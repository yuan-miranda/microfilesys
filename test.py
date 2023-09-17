command_flags = {
    "write":  ["-we", "--write-end",
               "-ws", "--write-specific"],
    "modify": ["-ms", "--modify-specific",
               "-ma", "--modify-all",
               "-mas", "--modify-all-specific"],
    "remove": ["-rmsub", "--remove-substring",
               "-rms", "--remove-specific",
               "-rmas", "--remove-all-specific"],
    "clear":  ["-cl", "--clear-line",
               "-ca", "--clear-all"],
    "read":   ["-rl", "--read-line",
               "-ra", "--read-all"],
    "close":  ["-c", "--close"],

    "create": [],
    "open":   ["-r", "--read",
               "-rw", "--read-write"],
    "delete": [],
}

class E:
    error_messages = {
        "invalid command usage": {
            command: f"invalid command: use 'man {command}' for {command} command usage"
            for command in command_flags.keys()
        }
    }

print(E.error_messages["invalid command usage"]["delete"])