pyramidSize = 10

for y in range(pyramidSize):
    for x in range(pyramidSize):
        if x < pyramidSize - y - 1:
            print(" ", end="")
        else:
            print("# ", end="")
    print()

for y in range(pyramidSize):
    for x in range(pyramidSize):
        if x < pyramidSize - y - 1:
            print(" ", end="")
        else:
            if y == 0:
                print("^", end="")
            elif x == pyramidSize - y - 1:
                print("/#", end="")
            elif x == pyramidSize - 1:
                print("\\ ", end="")
            else:
                print("##", end="")
    print()
