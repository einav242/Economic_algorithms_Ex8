import networkx as nx


def buildGraph(lst):
    g = nx.Graph()
    for i in range(len(lst)):
        g.add_node("item-" + str(i))
        g.add_node("person-" + str(i))

    for i in range(len(lst)):
        for j in range(len(lst[i])):
            node1 = "person-" + str(j)
            node2 = "item-" + str(i)
            g.add_weighted_edges_from([(node1, node2, lst[i][j])])
    return g


def vcg(lst):
    g = buildGraph(lst)
    max_matching = nx.max_weight_matching(g)
    max = 0
    for edge in max_matching:
        max += g.edges[edge]['weight']
    max_opt_without = []
    for edge in max_matching:
        max_opt_without.append(max - g.edges[edge]['weight'])
    max_without = []
    for edge in max_matching:
        new_g = g.copy()
        new_max = 0
        if edge[0][0] == 'p':
            new_g.remove_node(edge[0])
        else:
            new_g.remove_node(edge[1])
        new_max_matching = nx.max_weight_matching(new_g)
        for edge in new_max_matching:
            new_max += g.edges[edge]['weight']
        max_without.append(new_max)
    i = 0
    for edge in max_matching:
        pay = max_without[i] - max_opt_without[i]
        value = g.edges[edge]['weight']
        benefit = value - pay
        print("person number ", i + 1, ":\npayment: ", pay, "\nvalue: ",
              value, "\nbenefit: ", benefit, "\n")
        i += 1


if __name__ == '__main__':
    print("------2 people 2 item------")
    list1 = [[8, 4], [7, 2]]
    vcg(list1)
    print("------3 people 3 item------")
    list2 = [[4, 7, 9], [5, 4, 2], [8, 3, 5]]
    vcg(list2)
    print("------4 people 4 item------")
    list3 = [[4, 7, 9, 2], [5, 4, 2, 3], [8, 3, 5, 1], [1, 2, 3, 4]]
    vcg(list3)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
