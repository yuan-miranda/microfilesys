def find_middle(input_list):
    # Calculate the index of the middle element
    middle_index = len(input_list) // 2

    # Retrieve the middle element
    middle_element = input_list[middle_index]

    return middle_element

# Example usage
input_list = [1, 2, 3]
middle_element = find_middle(input_list)
print("The middle element is:", middle_element)
