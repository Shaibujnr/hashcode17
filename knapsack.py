import itertools
class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value


lot = [Item(2, 4), Item(3, 1), Item(4, 2), Item(6, 5)]
W = 10

def ssum(items,val):
    # result = [seq for i in range(len(items), 0, -1) for seq in itertools.combinations(items, i) if sum(seq) == val]
    result = []
    for i in range(len(items),0,-1):
        for seq in itertools.combinations([x.value for x in items],i):
            if sum(seq) == val:
                result.append(seq)
    return result
def subset_sum(items,val):
    result = []
    table = [[False]*(val+1) for x in range(len(items))]
    for i in range(len(table)):
        table[i][0] = True
    for row in range(len(table)):
        ci = items[row]
        for col in range(len(table[row])):
            som = col
            if ci.value == som:
                table[row][col] = True
            if ci.value > som and row > 0:
                table[row][col] = table[row-1][col]
            if ci.value < som and row > 0:
                table[row][col] = table[row-1][som-ci.value] or table[row-1][som]



    for row in table:
        print str(row)+"\n",

    while table[-1][-1] and sum(result) != val:
        for i in range(len(table)):
            for j in range(len(table[i])):
                pass


        x = val - result[-1]
        for i in range(len(table)):
            if table[i][x]:
                result.append(items[i].value)
                break

    print result





def knapsack(items):
    # items.sort(key=lambda x: x.weight)  # sort item in ascending order by weight
    table = [[-1 for x in range(W + 1)] for y in range(len(lot))]  # create knapsack table
    for row in range(len(table)):
        ci = items[row]
        for col in range(len(table[row])):
            mcw = col
            if ci.weight > mcw and row == 0:
                table[row][col] = 0
            if ci.weight > mcw and row > 0:
                table[row][col] = table[row - 1][col]
            if ci.weight <= mcw and row == 0:
                table[row][col] = ci.value
            if ci.weight <= mcw and row > 0:
                table[row][col] = max((ci.value + table[row - 1][mcw - ci.weight]), (table[row - 1][col]))

    return table[len(table) - 1][len(table[0]) - 1]


def main():
    print knapsack(lot)
    print ssum(lot,9)



if __name__ == "__main__":
    main()
