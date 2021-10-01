# There is a given list of numbers. The only thing you know about it is that those numbers are sorted in ascending
# You don't know the len of this list, if it contains negative, positive or both types of values or zero.
# There is a given number too.
#
# Your task:
# Find every two numbers from the list their sum is equal to given number and print it.
# Use max one for cycle in your code.

# Few (not all possible!) list to try your solution:
list_negative_long = [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
list_negative_short = [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
list_negative_too_short = [-4, -3, -2, -1, 0]
list_positive = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
list_from_zero = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
list_big_number = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
list_irregular = [-4, -3, 0, 2, 3, 4, 5, 6, 7, 8, 10, 11]
list_too_short = [2]
list_two_numbers = [5, 10]

# Choose teh list to try on:
list = list_negative_long
# Try with different numbers in different lists:
given_number = 1

# Solution:
# 1) Check if the list contains at least two numbers:
if len(list) < 2:
    print("The list is too short.")
    quit()

# 2) If the list contains just two numbers, we may just sum it without the necessity to run for cycle:
elif len(list) == 2:
    count = list[0] + list[-1]
    if count == given_number:
        element_1 = str(list[0])
        element_2 = str(list[-1])
        print(f"The pair of numbers we are looking for is " + element_1 + " and " + element_2 + ".")
        quit()

# In case the list contains more than two numbers, we run the for cycle:
else:
    for number in list:

        index_number = list.index(number)
        index_second_number = (index_number + 1)

        while ((number <= list[-1]) & (index_second_number <= (len(list) - 1))):
            second_number = list[index_second_number]
            result = number + second_number
            if result == given_number:
                element_1 = str(number)
                element_2 = str(second_number)
                print(f"The pair of numbers we are looking for is " + element_1 + " and " + element_2 + ".")
                printed = True
            index_second_number += 1

# If we haven't found any pair, let's print this information out:
try: printed
except NameError: printed = None
if printed is None:
    given_number = str(given_number)
    print(f"There is not a pair of numbers in the list whose sum is equal to " + given_number + " .")