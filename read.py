def ReadRules():
    with open("rules.txt", "r") as file:
        for line in file:
            print(line)

"""class Zingers:
    def __init__(self, jigglers):
        self.jigglers = jigglers

j = Zingers("nicholae")
g = Zingers("gicholae")

z = [j, g]

for i in range(0,len(z)):
    print(z[i].jigglers)
    i += 1"""