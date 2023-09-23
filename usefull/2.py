mylist = []
for i in range(6):
    for j in range(1, 11):
        if j == 10:
            mylist.append(chr(97+i))
            #print(' ', chr(97 + i), end='')
        else:
            mylist.append(str(j))
            #print(j, end='')

print(''.join(mylist))