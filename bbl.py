class BBL:
    def __init__(self, borough, block, lot):
        self.borough = borough
        self.block = block
        self.lot = lot
        self.bbl_repr = long(borough*1000000000+block*10000+lot)
        
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.bbl_repr == other.bbl_repr)
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __cmp__(self, other):
        return self.bbl_repr - other.bbl_repr
        
    def __getitem__(self, name):
        return self.__dict__[name]
        
    def __repr__(self):
        return str(self.__dict__)
        
    def __str__(self):
        return str(self.borough) + '-' + str(self.block) + '-' + str(self.lot)
        
    def __hash__(self):
        return hash(self.bbl_repr)