def loadCSV(filepath):
    """
    Methode, um Square aus der CSV-Datei einzulesen
    """
    table =[]
    file = open(filepath,"r")                              # Datei öffnen zum Lesen
    start = True                                                            # Variable, um erste Zeile ignorieren zu können
    for line in file:
        if start:                                                           # erste Zeile ignorieren
            start = not(start)
        else:
            a = line.rstrip().split(";") 
            table.append(a)                                  # Zeile in Feld auftrennen

    file.close
    return table