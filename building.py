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
        result = 'BBL:\n\t' + str(self.bbl)
        if self.primary is not None:
            result += '\nPrimary Owner:\n' + str(self.primary)
        if self.secondary is not None:   
            result += '\nSecondary Owners:\n' + '\n'.join(map(str, self.secondary))
        if self.hpd is not None: 
            result += '\nHPD Contacts:\n' + '\n'.join(map(str, self.hpd))
        if self.tax is not None: 
            result += '\nDOF Tax Information:\n' + '\n'.join(map(str, self.tax))
        return result
        
    def __hash__(self):
        return hash(self.bbl.bbl_repr)
        
    def get_owners(self):
        results = set()
        if self.primary is not None:
            results.add(self.primary)
        if self.secondary is not None:
            results |= self.secondary
        if self.hpd is not None:
            results |= self.hpd
        if self.tax is not None:
            results |= self.tax
        if self.dos is not None:
            results |= self.dos
        return results
        
    def similarity(self, other):
        if not isinstance(other, self.__class__):
            return 0
        
        # No need to match with its own    
        if self.bbl == other.bbl:
            return 0
            
        # Will need to implement bunch of address here, together with its weight.
        # However, at this stage, every owner will have the same weight 1
        self_owners = self.get_owners()
        other_owners = other.get_owners()
        
        overall_score = 0
        for owner1 in self_owners:
            for owner2 in other_owners:
                overall_score += owner1.similarity(owner2)
                
        return overall_score / (len(self_owners)*len(other_owners))