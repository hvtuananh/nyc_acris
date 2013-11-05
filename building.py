class Building:
    def __init__(self, bbl, primary = None, secondary = None, hpd = None, tax = None, dos = None):
        self.bbl = bbl
        self.primary = primary
        self.secondary = secondary
        self.hpd = hpd
        self.tax = tax
        self.dos = dos
        self.linkedbbls = None
        
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.bbl.bbl_repr == other.bbl.bbl_repr)
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __cmp__(self, other):
        return self.bbl.bbl_repr - other.bbl.bbl_repr
        
    def __repr__(self):
        return str(self.__dict__)
        
    def __str__(self):
        return str(self.__dict__)
        
    def __hash__(self):
        return hash(self.bbl.bbl_repr)