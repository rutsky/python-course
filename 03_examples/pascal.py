def pascal(n):
    row = [1]
    for i in xrange(n):
        print row

        # calc next row
        next_row = [1]
        #j = 0
        for j, elem in enumerate(row[:-1]):
            next_row.append(row[j] + row[j + 1])
            #j += 1
        next_row.append(1)

        row = next_row

pascal(7)
