flag = "w1{1wq8/7376j.:"
new = []

for i in range(len(flag)):
    if i % 2 == 0:
        new.append(chr(ord(flag[i]) - 5))
    else:
        new.append(chr(ord(flag[i]) + 2))

print("".join(new))
