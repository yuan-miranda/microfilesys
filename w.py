def length(input, op, length):
    """
    Compare the length of the input with a specified length using a given operator.

    Parameters:
    input (str): The input string to measure the length.
    op (str): Comparison operator, e.g., '==', '!=', '>', '<', '>=', '<='.
    length (int): The length to compare against.

    Returns:
    bool: True if the comparison is true, False otherwise.
    """

    return (op == '==' and len(input) == length) or (op == '!=' and len(input) != length) or (op == '>' and len(input) > length) or (op == '<' and len(input) < length) or (op == '>=' and len(input) >= length) or (op == '<=' and len(input) <= length)

# Example usage
input_str = "mom"
desired_length = 3
length(input_str, '==', 3)
