class Maquillajes():
    def __init__(self, labial, base, rimel, eyeliner, sombra):
        self.labial = labial
        self.base=base
        self.rimel= rimel
        self.eyeliner= eyeliner
        self.sombra= sombra
Carla=Maquillajes("amo Mac labiales","No uso", "Maybellin","NYx","no")
print(Carla.labial)