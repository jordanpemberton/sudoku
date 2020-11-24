def make_order_list(size):
    order = []
    end = size
    mid = size // 2 + 1
    for i in range(mid):
        order.append((i, i))
        if end - i - 1 != i:
            order.append((end - i - 1, end - i - 1))
        for j in range(i):
            order.append((i, j))
            order.append((j, i))
            order.append((end - i - 1, end - j - 1))
            order.append((end - j - 1, end - i - 1))
    print(order)
    return order

if __name__ == '__main__':
    make_order_list(9)
