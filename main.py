from itertools import permutations


def options(num) -> list():
    lst = list();
    for i in range(num):
        lst.append(i)
    return permutations(lst)


def fact(n):
    return 1 if (n == 1 or n == 0) else n * fact(n - 1);


def vcg(lst):
    maxValue = float('-inf')  # maximum sum among all possibilities
    sumValue = 0
    index = 0  # the index of the maximum sum among all possibilities

    option_list = []  # list of all the option with value
    lst_sum = []  # a list of the sums of the values of each option
    lst_without = []  # a list of the sums of the values of each option without player number i
    lst_max_sum = []  # the maximum amount of each option without player i

    n = fact(len(lst[0]))  # number of option
    m = len(lst)  # number of people
    perm = options(m)  # list of all the permeation 1...m

    for p in list(perm):
        temp_list = []
        for number in range(0, m):
            temp = p[number]
            temp_list.append((lst[temp][number]))
        option_list.append(temp_list)

    for lst in option_list:
        for i in lst:
            sumValue += i
        if sumValue > maxValue:
            maxValue = sumValue
            index = option_list.index(lst)
        lst_sum.append(sumValue)
        sumValue = 0

    for i in range(len(option_list)):
        temp_list2 = []
        for j in range(len(option_list[i])):
            temp_list2.append(lst_sum[i] - option_list[i][j])
        lst_without.append(temp_list2)

    for i in range(m):
        maxValue = float('-inf')
        for j in range(n):
            if lst_without[j][i] > maxValue:
                maxValue = lst_without[j][i]
        lst_max_sum.append(maxValue)

    pay_lst = []
    value_lst = []
    benefit_lst = []

    # print the result
    for i in range(m):
        pay_lst.append(lst_max_sum[i] - lst_without[index][i])
        value_lst.append(option_list[index][i])
        benefit_lst.append(value_lst[i] - pay_lst[i])
        print("person number ", i + 1, ":\npayment: ", lst_max_sum[i] - lst_without[index][i], "\nvalue: ",
              option_list[index][i], "\nbenefit: ", value_lst[i] - pay_lst[i], "\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    list1 = [[8, 4], [7, 2]]
    vcg(list1)
    list2 = [[4, 7, 9], [5, 4, 2], [8, 3, 5]]
    print(vcg(list2))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
