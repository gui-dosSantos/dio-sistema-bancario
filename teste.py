# lista = [{1: 11, 2: 12, 3:13}, {1: 21, 2: 22, 3: 23}]

# def x():
#     nova_lista = [lista[1]]
#     return nova_lista

# a = x()

# print(len([]) == 0)

y = 1

def x(*, y):
    return y + 1

print(x(y=y))