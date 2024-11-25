class temp:
    def __init__(self, b):
        self.a = b + 1

    def show(self):
        print(self.a + 1)

    def __getstate__(self):
        return self.a

    def __setstate__(self, state):
        self.a = state

t = temp(111)
d = {
    "1": t
}

import pickle
# with open("tt", 'wb') as file:
#     pickle.dump(d, file)
# d["1"].show()
with open("tt", 'rb') as file:
    data = pickle.load(file)
data["1"].show()