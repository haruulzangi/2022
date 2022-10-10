from random import randint


p = 333870410550569
g = 3
print('p =', p)
print('g =', g)

a = randint(2, p - 1)
x = pow(g, a, p)
print('g^a mod p =', x)
print('a = ?')
