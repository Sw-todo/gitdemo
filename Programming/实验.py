def f(a, L=[]):
    print(hex(id(L)))
    L.append(a)
    return L
def outer(x):
    b=[x] #python 2.x
    def inner(y):
        nonlocal x #python 3.x
        x+=y
        return x
    return inner
f=outer(1)
print(f(1))
print(f(6))
