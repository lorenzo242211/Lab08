from model.model import Model
from model.nerc import Nerc

model = Model()
n = Nerc(_id= 6, _value="troio")
lista = model.EventiCondizione(n, 1)
for e in lista:
    print(e.id)