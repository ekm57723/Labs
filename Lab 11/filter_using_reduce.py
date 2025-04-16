from functools import reduce

#f returns True or False
#sequence input list to filter
#returns a list of elements where f(element) is True

def filter_with_reduce(f, sequence):
    
    return reduce(
        lambda acc, x: acc + [x] if f(x) else acc,
        sequence,
        []
    )

print(filter_with_reduce(lambda x: x % 2 == 0, [1, 2, 3, 4, 5]))