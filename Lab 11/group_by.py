from functools import reduce

def group_by(f, target_list):
   
    return reduce(
        lambda acc, x: {**acc, f(x): acc.get(f(x), []) + [x]},
        target_list,
        {}
    )

print(group_by(len, ["hi", "dog", "me", "bad", "good"]))