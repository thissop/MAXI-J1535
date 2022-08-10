ret = 'IDs.txt'
doc = 'pipeline.txt'
key = 'key.txt'
def screen():
    x = []
    with open (doc, 'r') as f:
        for line in f:
            eline = line[1:ep]
            if term == eline: 
                line = line[0:10] + '\n'
                x.append(line)            
        x = sorted(x)
        y = str(len(x))
        with open(ret,'a') as a:
            heading = '#Identifier: '+ iden +'  Search term: '+term+'  Nobs: '+ y + '\n'
            a.write(heading)
            for elem in x:
                a.write(elem)

with open(key,'r') as k:
    names = []
    identifiers = []
    for line in k:
        if '#' not in line:
            linearray = line.split(",")
            #print(linearray)
            name = linearray[0]
            identifier = linearray[1]
            identifier = identifier.replace("X","")
            ep = 10-int(linearray[3])
            names.append(name)
            identifiers.append(identifier)
        nn = len(names)-1
        while nn >= 0:
            term = identifiers[nn]
            iden = names[nn]
            screen()
            nn -= 1