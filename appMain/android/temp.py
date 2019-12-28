i = 0
for j in range(1000):
    if j%3 == 0 or j % 5 == 0:
        i += j

print(i)