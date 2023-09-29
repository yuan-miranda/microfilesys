def is_column(column):
    if len(column) != 2:
        print("Invalid column input")
        return False
    
    valid_digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    if column[0].isalpha() and column[1] in valid_digits:
        print("Valid column input")
        return True
    else:
        print("Invalid column input")
        return False

def is_multi_column(column):
    if len(column) != 5:
        print("Invalid input length")
        return False
    
    elif column[2] == ':' and is_column(column[:2]) and is_column(column[3:]):
        print("Valid multi-column input")
        return True
    else:
        print("Invalid multi-column input")
        return False

is_multi_column("a1:a2")
