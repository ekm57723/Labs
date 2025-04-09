import time


def memoize(func):
    cache = {}

    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    
    return wrapper


def recur_fibo(n):
    if n <= 1:
        return n
    return recur_fibo(n - 1) + recur_fibo(n - 2)


@memoize
def recur_fibo_memo(n):
    if n <= 1:
        return n
    return recur_fibo_memo(n - 1) + recur_fibo_memo(n - 2)


def main():
    n = 40

    print("Running plain recursive Fibonacci")
    start_plain = time.time()
    print(f"Result: {recur_fibo(n)}")
    end_plain = time.time()
    print(f"Time without memoization: {end_plain - start_plain:.4f} seconds\n")

    print("Running memoized Fibonacci")
    start_memo = time.time()
    print(f"Result: {recur_fibo_memo(n)}")
    end_memo = time.time()
    print(f"Time with memoization: {end_memo - start_memo:.4f} seconds")


if __name__ == "__main__":
    main()
