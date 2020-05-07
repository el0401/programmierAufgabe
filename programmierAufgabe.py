def findsequence(path_file, length, mintemp, maxtemp, distance):
    with open(path_file, 'r') as file:
        data = file.read().replace('\n', '')

    datalist = []
    for line in data:
        for c in line:
            datalist.append(c)

    totalnumb = len(datalist)

    primer1found = False
    primer2found = False
    primersfound = primer1found & primer2found
    acceptedlist = ['A', 'T', 'G', 'C']
    start = 0
    primer1 = []

    while not primer1found:

        for x in range(start, totalnumb, 1):
            if datalist[x] in acceptedlist:
                primer1.append(datalist[x])

                if len(primer1) == length:
                    temp = temperature(primer1)
                    if (temp >= mintemp) and (temp <= maxtemp):
                        primer1found = True
                        break
                    else:
                        primer1.clear()
                        start = start + 1
                        break
            else:
                primer1.clear()
                start = start + 1
                break

        if totalnumb - start - distance - 2 * length <= 0:
            primer1.clear()
            print('Keine Primerpaare gefunden')
            primersfound = False
            break
    print(primer1)


def temperature(primer):
    counterAT = 0
    counterGC = 0
    for x in primer:
        if (x == 'A') or (x == "T"):
            counterAT += 1
        if (x == 'G') or (x == "C"):
            counterGC += 1
    return (2 * counterAT) + (4 * counterGC)
