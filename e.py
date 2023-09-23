def is_column(column):
    if len(column) != 2:
        print("not 2")
        return False
    
    elif column[0].isalpha() and column[1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        print(f"{column} is valid")
        return True
    else:
        print(f"{column} is not valid")
        return False

def is_multi_column(column):
    if len(column) != 5:
        print("not 5")
        return False
    
    elif is_column(column[:2]) and is_column(column[3:]): # RUN THIS AND CHECK IF ITS
        print(f"{column} multi-column")
        return True
    else:
        print(f"{column} not multi-column")
        return False
    
is_multi_column("a9:a2")