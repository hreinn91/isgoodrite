
def fibonacci_sequence(n):
    """
    Generate a list containing the first n numbers in the Fibonacci sequence.

    Parameters:
    n (int): The number of terms in the Fibonacci sequence to generate.

    Returns:
    list: A list containing the Fibonacci sequence.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    # Initialize the first two Fibonacci numbers
    fib_sequence = [0, 1]

    # Generate the rest of the sequence
    for i in range(2, n):
        next_value = fib_sequence[i - 1] + fib_sequence[i - 2]
        fib_sequence.append(next_value)

    return fib_sequence

# Example usage:
num_terms = 10
print(f"Fibonacci sequence with {num_terms} terms: {fibonacci_sequence(num_terms)}")
