

# path_file im format: C:\..\..\.fasta
# length, temp und distance in int
def find_sequence(path_file, length, mintemp, maxtemp, distance):

    primer1found = False
    primer2found = False
    primersfound = primer1found & primer2found
    # Liste der akzeptierten Buchstaben um ungewollte Zeichen in Primern zu verhindern
    acceptedlist = ['A', 'T', 'G', 'C']
    primer1 = []
    primer2 = []

    # speichern der Daten in eine List zur einfacheren Weiterverwendeung
    with open(path_file, 'r') as file:
        data = file.read().replace('\n', '')
    datalist = []
    for line in data:
        for c in line:
            datalist.append(c)
    totalnumb = len(datalist)

    # Schleife zur Überprüfung ob Suchvorgang beendet ist
    while not primersfound:
        start = 0
        # Schleife in der vom ersten Zeichen solange ein Primer gesucht wird, bis dieser die Länge length erreicht hat
        # mit den erlaubten Zeichen und im Temperaturbereich liegt
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

            # Abbruch der Schleife falls nicht genügend Zeichen übrig bleiben unter Beachtung von legnth, distance
            # und bereits abgesuchten Zeichen
            if totalnumb - start - distance - 2 * length <= 0:
                primer1.clear()
                print('Keine Primerpaare gefunden')
                primer1found = False
                break

        # Abbruch der Schleife falls kein Primer gefunden wurde
        if not primer1found:
            break

        # Schleife um 2. Primer zu finden ab Primer1 plus distance
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

    if primersfound:
        # Zeichen im Titel der Fasta Datei
        file = open(path_file)
        stringList = file.readlines()
        lengthList = []
        for line in stringList:
            lengthList.append(len(line))
        # -1 für Zeilenumbruch
        chars_in_first_line = lengthList[0]-1

        # Ausgabe
        print("Primer 1: "+''.join(primer1)+" an Position "+str(start-chars_in_first_line)+", Schmelztemperatur: "+str(temp))
        print("Primer 2: "+''.join(reverse_complement(primer2))+" an Position "+str(start2-chars_in_first_line)+", Schmelztemperatur: "+str(temp2))


# Funktion zur Berechnung der Temperatur
def temperature(primer):
    counter_at = 0
    counter_gc = 0
    for x in primer:
        if (x == 'A') or (x == "T"):
            counter_at += 1
        if (x == 'G') or (x == "C"):
            counter_gc += 1
    return (2 * counter_at) + (4 * counter_gc)


# Funktion zum Umwandeln des 2. Primers (revers-komplementär)
def reverse_complement(primer):
    complement_dict = {"A": "T", "T": "A", "G": "C", "C": "G"}
    count = 0
    for x in primer:
        primer[count] = complement_dict[x]
        count += 1

    return list(reversed(primer))

