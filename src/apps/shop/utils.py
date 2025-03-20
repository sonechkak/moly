from random import randint


def get_random_products(product, products):
    data = []
    for i in range(6):
        random_index = randint(0, len(products) - 1)
        random_item = products[random_index]
        if random_item not in data and str(random_item) != product.title:
            data.append(random_item)

    return data
