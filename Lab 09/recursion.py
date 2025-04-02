def product_of_digits(x):
    """Returns the product of the digits of an integer using recursion."""
    x = abs(x)  #x must be positive
    if x < 10:
        return x  #Base case - single-digit number
    return (x % 10) * product_of_digits(x // 10)


def array_to_string(a, index=0):
    """Returns a string representation of a list of integers separated by commas using recursion."""
    if index >= len(a):
        return ""  #Base case - end of the list
    if index == len(a) - 1:
        return str(a[index])  #Last element
    return str(a[index]) + "," + array_to_string(a, index + 1)


def log(base, value):
    """Computes the floored logarithm using recursion."""
    if value <= 0 or base <= 1:
        raise ValueError("Value must be greater than 0 and base must be greater than 1.")
    if value < base:
        return 0  #Base case - value is smaller than base
    return 1 + log(base, value // base)


#Testing
if __name__ == "__main__":
    print('Task 1, Product of Digits (test 1):', product_of_digits(1224))  #Change number to test task 1
    print('Task 1, Product of Digits (test 2):', product_of_digits(-136))  #Change number to test task 1
    
    print('Task 2, Array to String:', array_to_string([0, 4, 2, 0, 0, 9, 0, 5, 2, 0, 0, 4]))  #Change numbers to test task 2
    
    print('Task 3, Logarithm (test 1):', log(10, 123456789))  #Change numbers to test task 3
    print('Task 3, Logarithm (test 2):', log(2, 2048))  #Change number to test task 3