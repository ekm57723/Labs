#make_set(data)

data = [1, 2, 3, 3, 4, 4, 5, 6, 7, 7, 7, 8, 8, 9, 10]

def make_set(data):

    i = 0
    j = 0
    result = []

    for i in range(0, len(data) - 1):

        if data[i] > data[i+1]:
    
            x = data[i]
            y = data[i + 1]
            data[i] = y
            data[i +1] = x
        

    for j in range(0, len(data) - 1):

        if data[j] != data[j + 1]:
            result.append(data[j])

    if data[len(data) - 2] != data[len(data) - 1]:

        result.append(data[len(data)-1])
    
    return result
    

result = make_set(data)

print(result)

def is_set(result):

    i = 0

    for i in range(0, len(result)-1):

        if result[i] == result[i+1]:

            x = 'False'
            break

        elif result [i] != result [i+1]:

            x = 'True'

    if result[len(result) - 2] == result[len(result) - 1]:

        x = 'False'
    
    return x

x = is_set(result)

print(x)

setA = [1, 2]
setB = [2, 3]

def unions(setA, setB):

    i = 0
    j = 0
    k = 0
    l = 0
    m = 0
    w = 0
    union = []
    union1 = []
    var = 1
    x = setA[0]
    z = setB[0]

    if setA == []:

        setA[0] = z

    if setB == []:

        setB[0] = x

    for i in range(0, len(setA) - 1):

        if setA[i] > setA[i+1]:
    
            x = setA[i]
            y = setA[i + 1]
            setA[i] = y
            setA[i + 1] = x

    if setA[len(setA) - 2] > setA[len(setA) - 1]:

        x = setA[i]
        y = setA[i + 1]
        setA[i] = y
        setA[i + 1] = x

    for i in range(0, len(setB) - 1):

        if setB[i] > setB[i+1]:
    
            x = setB[i]
            y = setB[i + 1]
            setB[i] = y
            setB[i + 1] = x

    if setB[len(setB) - 2] > setB[len(setB) - 1]:

        x = setB[i]
        y = setB[i + 1]
        setB[i] = y
        setB[i + 1] = x

    for j in range(0, len(setA) - 1):

        if setA[j] != setA[j + 1]:

            union.append(setA[j])

        elif setA == []:

            w = 0

        else:
            
            var = 2

    for k in range(0, len(setB) - 1):

        if setB[k] != setB[k + 1]:

            union.append(setB[k])

        elif setB == []:

            w = 0
        
        else:
            
            var = 2

    if setA[len(setA) - 2] != setA[len(setA) - 1]:

        union.append(setA[len(setA)-1])

    elif setA == []:

        w = 0

    else:

        var = 2

    if setB[len(setB) - 2] != setB[len(setB) - 1]:

        union.append(setB[len(setB)-1])


    elif setB == []:

        w = 0


    else:

        var = 2

    for l in range(0, len(union) - 1):

        if union[l] > union[l+1]:
    
            x = union[l]
            y = union[l + 1]
            union[l] = y
            union[l + 1] = x

    if union[len(union) - 2] > union[len(union) - 1]:

        x = union[len(union) - 2]
        y = union[len(union) - 1]
        union[len(union) - 2] = y
        union[len(union) - 1] = x

    for m in range(0, len(union) - 1):

        if union[m] != union[m + 1]:

            union1.append(union[m])
    
    if union[len(union) - 2] != union[len(union) - 1]:

        union1.append(union[len(union)-1])

    if var == 2:

        union1 = []

    return union1


union1 = unions(setA, setB)

print(union1)

def intersection(setA, setB):

    i = 0
    j = 0
    k = 0
    l = 0
    intersect = []

    for i in range(0, len(setA) - 1):

        if setA[i] > setA[i+1]:
    
            x = setA[i]
            y = setA[i + 1]
            setA[i] = y
            setA[i + 1] = x

    if setA[len(setA) - 2] > setA[len(setA) - 1]:

        x = setA[i]
        y = setA[i + 1]
        setA[i] = y
        setA[i + 1] = x

    for i in range(0, len(setB) - 1):

        if setB[i] > setB[i+1]:
    
            x = setB[i]
            y = setB[i + 1]
            setB[i] = y
            setB[i + 1] = x

    if setB[len(setB) - 2] > setB[len(setB) - 1]:

        x = setB[i]
        y = setB[i + 1]
        setB[i] = y
        setB[i + 1] = x

    for k in range(0, len(setA)):

        for l in range(0, len(setB)):

            if setA[k] == setB[l]:
                
                intersect.append(setA[k])

    return intersect

intersect = intersection(setA, setB)

print(intersect)
