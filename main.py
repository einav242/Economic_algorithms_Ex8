# This is a sample Python script.
from itertools import permutations
from typing import List


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def options(num) -> list():
    lst = list();
    for i in range(num):
        lst.append(i)
    return permutations(lst)


def fact(n):
    return 1 if (n == 1 or n == 0) else n * fact(n - 1);


def vcg(lst):
    maxValue = float('-inf')
    sumValue = 0
    end_list = []
    n = fact(len(lst[0]))
    m = len(lst)
    perm = options(m)
    for premotechion in list(perm):
        temp_list = []
        for nmegical_number in range(0, m):
            temp = premotechion[nmegical_number]
            temp_list.append((lst[temp][nmegical_number]))
        end_list.append(temp_list)

    index = 0
    lst_sum = []
    for lst in end_list:
        for i in lst:
            sumValue += i
        if sumValue > maxValue:
            maxValue = sumValue
            index = end_list.index(lst)
        lst_sum.append(sumValue)
        sumValue = 0

    lst_without = []
    for i in range(len(end_list)):
        temp_list2 = []
        for j in range(len(end_list[i])):
            temp_list2.append(lst_sum[i] - end_list[i][j])
        lst_without.append(temp_list2)


    lst_max_sum = []

    for i in range(m):
        maxValue = float('-inf')
        for j in range(n):
            if lst_without[j][i] > maxValue:
                maxValue = lst_without[j][i]
        lst_max_sum.append(maxValue)

    pay_lst = []
    value_lst = []
    benefit_lst = []

    for i in range(m):
        pay_lst.append(lst_max_sum[i] - lst_without[index][i])
        value_lst.append(end_list[index][i])
        benefit_lst.append(value_lst[i] - pay_lst[i])
        print("person number ", i+1, ":\npayment: ", lst_max_sum[i] - lst_without[index][i], "\nvalue: ",end_list[index][i],"\nbenefit: ",value_lst[i] - pay_lst[i],"\n")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    list1 = [[8, 4], [7, 2]]
    vcg(list1)
    list2 = [[4, 7, 9], [5, 4, 2], [8, 3, 5]]
    print(vcg(list2))
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
