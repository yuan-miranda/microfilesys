# return the content
def get_content(content, content_index):
    return ' '.join(content[content_index:])[1:-1]

# check if the input is a content
def is_content(content, content_index):
    string = ' '.join(content[content_index:]) 
    content_start = string[0]
    content_end = string[-1]

    # early return if the content has more or less than double quotes on it
    if string.count('"') != 2:
        print("use pair of '\"' to enclose the content ex: \"content\"")
        return False
    
    # prevent: a", a"", '"a"'
    if content_start != '"':
        print("missing '\"' on the start of the content")
        return False
    
    # prevent: "a, ""a, '"a"'
    if content_end != '"':
        print("missing '\"' on the end of the content")
        return False

    return True

input_string = input("Enter: ")
#quotes = input_string.find('"') # FIND ALL THE QUOTES
# Extract the desired substring
#desired_substring = get_content(input_string.split(), 3)
#print(desired_substring)

#print(quotes)
if is_content(input_string.split(), 1):
    print(get_content(input_string.split(), 1))
#print(is_content(input_string.split(), 1))