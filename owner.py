class Owner:
    def __init__(self, item):
        self.item = item
        
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.transform() == other.transform())
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __getitem__(self, name):
        return self.item[name]
        
    def __repr__(self):
        return str(self.item)
        
    def __str__(self):
        return str(self.item)
        
    def __hash__(self):
        return hash(self.item['name']) ^ hash(self.item['addr1']) ^ hash(self.item['addr2']) ^ hash(self.item['city']) ^ hash(self.item['state']) ^ hash(self.item['zip'])
        
    def transform(self):
        item = {
            'name': self.item['name'],
            'addr1': self.item['addr1'],
            'addr2': self.item['addr2'],
            'city': self.item['city'],
            'state': self.item['state'],
            'zip': self.item['zip']
        }
        return item