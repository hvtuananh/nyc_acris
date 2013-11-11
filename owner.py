import re
p = re.compile(r'[^0-9a-z]')

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
        result = '\tName:\n\t\t' + str(self['name'])
        result += '\n\tAddress:\n\t\t' + str(self['addr1']).strip() + ', ' + str(self['addr2']).strip() + ', ' + str(self['city']) + ', ' + str(self['state']) + ', ' + str(self['zip'])
        return result
        
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
        
    def similarity(self, other):
        # Min = 0, Max = 2
        if not isinstance(other, self.__class__):
            return 0
        
        # Don't need to compare the same entity
        if self is other:
            return 0
        
        # If they are exactly the same, then give 1        
        if self == other:
            return 1
            
        return self.name_similarity(other) + self.addr_similarity(other)
        
    def name_similarity(self, other):
        self_name = set(filter(None, p.split(self['name'].lower())))
        other_name = set(filter(None, p.split(other['name'].lower())))
        try:
            score = float(len(self_name & other_name)) / len(self_name | other_name)
        except ZeroDivisionError:
            return 0
            
        if score > 0.5:
            return score
        else:
            return 0 
        
    def addr_similarity(self, other):
        if str(self['state']).lower() != str(other['state']).lower():
            return 0
            
        if self['zip'] != '' and other['zip'] != '':
            #if int(str(self['zip'])[0:5]) != int(str(other['zip'])[0:5]):
            if int(str(self['zip'])[0:3]) != int(str(other['zip'])[0:3]):
                return 0
            
        # Now only need to consider address matching
        self_addr = set(p.split(self['addr1'].lower()))
        other_addr = set(p.split(other['addr1'].lower()))
        return float(len(self_addr & other_addr)) / len(self_addr | other_addr)