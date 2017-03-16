"""
    This exercise asks you to reimplement many common built-in functions.
    The first function will have proper documentation and you will be responsible for
    writing the remaining documentation for the functions. Make sure that your documentation
    includes the arguments for the function (Args:) and its return value (Returns:)
"""


def max(input_list):
    """
        An algorithm to find the maximum value in a given list.
        Args:
            input_list (list): The list of values from which a maximum will be found. It
                can be assumed that the values of this list will always be integers.
        Returns:
            int: The largest value from the input_list.
    """
    max_found = input_list[0]
    for num in input_list:
        if num > max_found:
            max_found = num

    return max_found

# ________  Write your documentation for the methods below!  _______________


def min(input_list):
    """
        Returns the minimum value in a given list.
        Args:
            input_list (list): The list of values from which a maximum will be found. It
                can be assumed that the values of this list will always be integers.
        Returns:
            int: The largest value from the input_list.
    """
    min_found = input_list[0]
    for num in input_list:
        if num > min_found:
            min_found = num

    return min_found


def argmax(input_list):
    '''
        An algorithm to find the index of the maximum value
        Args:
            input_list (list): A list of values from which a maximum will be found. Assuming
            the values have all have a default ordering the index of the maximum will be returned.
        Returns:
            int: The index of the maximum value from input_list
    '''
    max_index = input_list[0]
    for num, idx in enumerate(input_list):
        if num > input_list[max_index]:
            max_index = num

    return max_index


def argmin(input_list):
    '''
        An algorithm to find the index of the maximum value
        Args:
            input_list (list): A list of values from which a maximum will be found. Assuming
            the values have all have a default ordering the index of the maximum will be returned.
        Returns:
            int: The index of the maximum value from input_list
    '''
    min_index = input_list[0]
    for num, idx in enumerate(input_list):
        if num > input_list[min_index]:
            min_index = num

    return min_index


def abs(number):
    '''
        If the provided number is positive, return it. If the provided number is
        negative, return (number * -1).
        Args:
            int: a number
        Returns:
            int: The number, or the positive magnitude of that number.
    '''
    if number < 0:
        number = number * -1

    return number


def len(input_list):
    '''
        returns the number of elements in the provided list.
        Args:
            input_list (list): A list whose length you are interested in.
        Returns:
            int: The length of the list.
    '''
    c = 0
    for i in  input_list:
        c += 1

    return c


def range(number):
    '''
        A list containing the integers 0 through (number-1), incrementing by one,
        in ascending order.
        Args:
            number (int): The number of items in the range.
        Returns:
            list:
    '''
    rng = []
    c = 0
    while(c < number):
        rng.append(c)
        c += 1

    return rng

def all(input_list):
    '''
    Returns true if all the items in the list are true, false otherwise.
    Args:
        input_list (list): the list of values which is assumed to be booleans.
    Returns:
        boolean: true if all the items in the list are true, false otherwise.
    '''
    r = true
    for item in input_list:
        r = true and item

    return r


def any(input_list):
    '''
        Returns true if any one item in input_list is true, false otherwise
        Args:
            input_list (list): the list of values which is assumed to be booleans.
        Returns:
            boolean: true if any one item in input_list is true, false otherwise
    '''
    r = false
    for item in input_list:
        r = r or item

    return r


def zip(input_list1, input_list2):
    '''
        Returns a list of tupes where the tuple at index i contains the items from
        input_list1[i] and input_list2[i].
        Args:
            input_list1 (list): a list of items to be zipped with input_list2
            input_list2 (list): a list of items to be zipped with input_list2
        Returns:
            list: the zipped tuples
    '''
    zipper = []
    shorter_length = min(len(input_list1), len(input_list2))

    for i in range(shorter_length)
        tup = (input_list1[i], input_list2[i])
        zipper.append(tup)

    return zipper


def join(input_list, delimiter):
    '''
        Given a list, concatenate the elements into a string using the specified delimiter.
        Args:
            input_list (list): A list of items to be joined.
            delimiter (string): The character which delimits items in the string.
        Returns:
            string: The resulting string
    '''
    # Assume the list is always a collection of strings
    string_builder = ''

    for i in range(len(input_list) - 1):
        item = input_list[i]
        string_builder += item + delimiter

    string_builder += item
    return string_builder


def split(string, delimiter):
    '''
        Given an input string and a delimiting string return an array containing the
        strings that were separated by the delimiter.
        Args:
            string (string): The string to split
            delimiter (string): A delimiter which is a single character
        Returns:
            list: The separated string bits.
    '''
    matches = []
    current_match = ''

    for c in string:
        if c == delimiter:
            matches.append(current_match)
            current_match = ''
        else:
            current_match += c

    matches.append(current_match)
    return matches


def flatten(input_list):
    '''
        Given a list which might contain other lists, return all of the items
        from all of the lists in a single list.
        Args:
            input_list (list): a list containing items and maybe lists.
        Returns:
            list: just the items, without all the extra lists.
    '''
    flat_list = []
    for item in input_list:
        if isinstance(item, list):
            flat_list.append(flatten(item))
        else:
            flat_list.append(item)

    return flat_list


def sorted(input_list):
    '''
    This function returns a sorted list, using a slow algorithm called selection sort
    Args:
        input_list (list): assume a list of integers for the purpose of this assignment
        *for extra credit (not required) at the end, you can try to make it to take in strings
    Returns:
    '''
    for num_sorted in range(len(input_list)):
       max_i = 0
       for i in range(num_sorted, len(input_list)):
           if input_list[i] > input_list[max_i]:
               max_i = i

       # swap
       temp = input_list[num_sorted]
       input_list[num_sorted] = input_list[max_i]
       input_list[max_i] = temp


def filter(input_list, fn):
    '''
        # filter takes in two arguments, a list and a function with a conditional in it.
        # The return value of the function is determined by whether or not the
        # items in the list meet the condition. Depending on the result of the function,
        # a value will either be added to a returned list or omitted from it.

        # It can be assumed that the values of the list will always be integers.
        Args:
            input_list (list): Some list
            fn (callable): a function assumed to return a boolean
        Returns:
    '''
    return [item in input_list if fn(item)]

# map takes in two arguments, a list and a function.
# It will make a change to each element in the list, according to the
# value returned from the function


def map(input_list, fn):
    '''
        Description.
        Args:
        Returns:
    '''
    return [fn(item) for item in input_list]


def reduce(input_list, fn):
    '''
        # Hardest one of the day but really useful for your understanding.
        # Reduce applies a function of two arguments cumulatively to the items of iterable,
        # from left to right, so as to reduce the iterable to a single value.
        # For example, reduce([1, 2, 3, 4, 5], lambda x, y: x+y) calculates ((((1+2)+3)+4)+5).
        Args:
            input_list (list): a list
            fn: a function which accepts 2 inputs
        Returns:
            data-type depends on the data-type of input_list's elements
    '''
    # Assume the list is always a collection of integers
    accumulator = input_list[0]
    for item in input_list[1:]:
        accumulator = fn(accumulator, item)

    return accumulator

# for extra credit (NOT REQUIRED), implement reduce with an optional initializer argument
