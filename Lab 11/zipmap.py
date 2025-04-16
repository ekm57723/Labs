
from functools import reduce

#If override=True, later keys override earlier duplicates.
#If override=False, returns None if key_list has duplicates.
#If key_list is longer, missing values are set to None.
#If key_list is shorter, extra values are discarded.

def zipmap(key_list: list, value_list: list, override=False):
    
    if not override and len(key_list) != len(set(key_list)):
        return None
    
    adjusted_values = (
    value_list[:len(key_list)] if len(value_list) >= len(key_list)
    else value_list + [None] * (len(key_list) - len(value_list))
    )
    
    result = dict(map(lambda k, v: (k, v), key_list, adjusted_values))
    return result

print(zipmap(['a', 'b', 'c'], [1, 2, 3])) 
print(zipmap([1, 2, 3, 2], [4, 5, 6, 7], True)) 
print(zipmap([1, 2, 3, 2], [4, 5, 6, 7], False)) 
print(zipmap([1, 2, 3], [4, 5, 6, 7, 8]))
print(zipmap([1, 3, 5, 7], [2, 4, 6]))  