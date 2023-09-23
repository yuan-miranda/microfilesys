def generate_string(length):
    if length < 1 or length > 240:
        return f"{length} is not invalid, only 1-240"

    mylist = ['a'] # I forgot why 'a' is here, now God only knows why
    ourlist= ['a']

    for i in range(length - 1):
        j = i % 10 + 1
        if j == 10:
            mylist.append(chr(97 + (i//9)))
        else:
            mylist.append(str(j))
            ourlist.append(str(j)) # PRINT LETTERS

    return ''.join(mylist), ''.join(ourlist)








while True:
    try:
        desired_length = int(input("Enter length: "))
    except ValueError:
        print("hasto be number try again")
        continue

    resulting_string1, resulting_string2 = generate_string(desired_length)

    print(resulting_string1)
    print(resulting_string2)
    print(len(resulting_string1))
    print(len(resulting_string2))
