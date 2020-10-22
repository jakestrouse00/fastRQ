class M:
    def __init__(self):
        self.j = 0


class O:
    def __init__(self, obj):
        self.obj = obj

    def mutate(self):
        self.obj.j = 5

r = M()
p = O(r)
p.mutate()
print(r.j)