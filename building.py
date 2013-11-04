class Building:
    def __init__(self, bbl, primary = None, secondary = None, hpd = None, tax = None, dos = None):
        self.bbl = bbl
        self.primary = primary
        self.secondary = secondary
        self.hpd = hpd
        self.tax = tax
        self.dos = dos
        self.linkedbbls = None
        
    def __str__(self):
        return str(self.__dict__)