def find_sequence(path_file, length, mintemp, maxtemp, distance):
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
    primer1 = []
    primer2 = []

    while not primersfound:
        start = 0
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
                primer1found = False
                break

        if not primer1found:
            break

        start2 = start + distance
        while not primer2found:
            for x in range(start2, totalnumb, 1):
                if datalist[x] in acceptedlist:
                    primer2.append(datalist[x])

                    if len(primer2) == length:
                        temp2 = temperature(primer2)
                        if (temp2 >= mintemp) and (temp2 <= maxtemp):
                            primer2found = True
                            break
                        else:
                            primer2.clear()
                            start2 = start2 + 1
                            break
                else:
                    primer2.clear()
                    start2 = start2 + 1
                    break

            if totalnumb - start2 - length <= 0:
                primer2.clear()
                print('Keine Primerpaare gefunden')
                primer2found = False
                break

        if not primer2found:
            break
        else:
            primersfound = True

    print("Primer 1: "+''.join(primer1)+" an Position "+start+", Schmelztemperatur: "+temp)
    print(reverse_complement(primer2))


def temperature(primer):
    counter_at = 0
    counter_gc = 0
    for x in primer:
        if (x == 'A') or (x == "T"):
            counter_at += 1
        if (x == 'G') or (x == "C"):
            counter_gc += 1
    return (2 * counter_at) + (4 * counter_gc)


def reverse_complement(primer):
    complement_dict = {"A": "T", "T": "A", "G": "C", "C": "G"}
    count = 0
    for x in primer:
        primer[count] = complement_dict[x]
        count += 1

    return list(reversed(primer))

