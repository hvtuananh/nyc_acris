from pymongo import MongoClient
from datetime import datetime
from owner import Owner

class BBLQuery:
    def __init__(self, host, port):
        client = MongoClient('localhost', 40000)
        self.db = client.furman
        
    def normalize_str(self, string):
        return string.replace('|', ',')
        
    def query_lots(self, borough, block):
        '''
        This part is used to get all lots associated with a borough and block
        '''
        bbl_records = list(self.db.lot_records.find({'borough':borough,'block':block}, {'lot':1}))
        print "Found", len(bbl_records), "BBL in this area..."
        lots = set()
        for bbl_record in bbl_records:
            lots.add(bbl_record['lot'])
        return lots
        
    def match_owner(self, owner1, owner2):
        '''
        Each owner is a record of name and address
        '''
        
    def query_bbl(self, borough, block, lot):
        #bbl = borough (from args) + block (from args) + lot (either from args or db)
    
        print "BBL:", borough, block, lot
        bbl = long(borough*1000000000+block*10000+lot)

        # Each BBL has only 1 record
        '''
        lots = lot_records.find({'borough':borough,'block':block,'lot':lot})
        for lot_record in lots:
            print lot_record
        '''
        print "STEP 1:"
        lot_records = list(self.db.lot_records.find({'borough':borough,'block':block,'lot':lot}))
        print "Found", len(lot_records), "records in lot_records..."
        # We should get all keys here, just in case
        '''
        lot_record = lot_records[0]
        unique_key = lot_record['key']
        '''
        unique_keys = list()
        for lot_record in lot_records:
            unique_keys.append(lot_record['key'])

        master_records = list(self.db.master_records.find({'key':{'$in':unique_keys}}))
        print "Found", len(master_records), "records in master_records..."
        latest_unique_key = None
        latest_doc_date = datetime.strptime('1970-01-01', '%Y-%m-%d')
        for master_record in master_records:
            if master_record['doc_date'] == "":
                continue
            if master_record['doc_type'][0:4] == 'DEED':
                if datetime.strptime(master_record['doc_date'], '%Y-%m-%d') > latest_doc_date:
                    latest_unique_key = master_record['key']
                    latest_doc_date = datetime.strptime(master_record['doc_date'], '%Y-%m-%d')

        if latest_unique_key is None:
            print "Nothing found!"
            return None
        elif str(latest_unique_key)[0:3] == "BK_" or str(latest_unique_key)[0:3] == "FT_":
            print "Latest UK is", latest_unique_key
            print "We're not interested in this type of property!"
            return None
        else:
            print "Latest UK is", latest_unique_key

        #FINISH STEP 1

        print "STEP 2:"
        party_records = list(self.db.party_records.find({'key':latest_unique_key}))
        print "Found", len(party_records), "records in party_records..."
        primary_party = None
        for party_record in party_records:
            if party_record['party_type'] == 2:
                primary_party = Owner({
                    'name': self.normalize_str(party_record['name']),
                    'addr1': self.normalize_str(party_record['addr1']),
                    'addr2': self.normalize_str(party_record['addr2']),
                    'city': party_record['city'],
                    'state': party_record['state'],
                    'zip': party_record['zip']
                })

        if primary_party is None:
            print "No name found!"
            return None
        else:
            print "Primary party is ", primary_party['name']
    
        print primary_party
    
        #FINISH STEP 2

        print "STEP 3:"
        secondary_unique_keys = list()
        for master_record in master_records:
            if master_record['doc_date'] == "":
                continue
            if datetime.strptime(master_record['doc_date'], '%Y-%m-%d') < latest_doc_date:
                continue
            if master_record['doc_type'][0:4] == 'MTGE' or master_record['doc_type'][0:4] == 'AGMT':
                secondary_unique_keys.append(master_record['key'])
        
        print "Found", len(secondary_unique_keys), "secondary UKs: ", secondary_unique_keys

        #FINISH STEP 3

        print "STEP 4:"
        party_records = list(self.db.party_records.find({'key':{'$in': secondary_unique_keys}}))
        print "Found", len(party_records), "records in party_records..."
        secondary_parties = set()
        for party_record in party_records:
            if party_record['party_type'] == 1:
                secondary_party = Owner({
                    'name': self.normalize_str(party_record['name']),
                    'addr1': self.normalize_str(party_record['addr1']),
                    'addr2': self.normalize_str(party_record['addr2']),
                    'city': party_record['city'],
                    'state': party_record['state'],
                    'zip': party_record['zip']
                })
                secondary_parties.add(secondary_party)
        
        print "Found", len(secondary_parties), "secondary parties..."
        for secondary_party in secondary_parties:
            print "Name:", secondary_party['name']
    
        print secondary_parties
    
        #FINISH STEP 4

        print "STEP 5:"
        lot_records = list(self.db.lot_records.find({'key':{'$in': secondary_unique_keys}}))
        print "Found", len(lot_records), "records in lot_records..."
        print "These are secondary BBLs:"
        cache_bbls = list([bbl])
        for lot_record in lot_records:
            if borough != lot_record['borough'] or block != lot_record['block'] or lot != lot_record['lot']:
                secondary_bbl = long(lot_record['borough']*1000000000+lot_record['block']*10000+lot_record['lot'])
                if secondary_bbl not in cache_bbls:
                    cache_bbls.append(secondary_bbl)
                    print lot_record['borough'], lot_record['block'], lot_record['lot']
        
        #FINISH STEP 5

        print "STEP 6: HPD"
        hpd_records = list(self.db.hpd.find({'bbl':bbl}))
        print "Found", len(hpd_records), "records in hpd..."
        #Get the first one
        if len(hpd_records) == 0:
            print "No HPD records!"
            return None

        hpd_record = hpd_records[0]
        hpd_reg_id = hpd_record['RegistrationID']

        #FINISH STEP 6

        print "STEP 7: HPD Contacts"
        hpd_contact_records = list(self.db.hpd_contact.find({'RegistrationID': hpd_reg_id}))
        print "Found", len(hpd_contact_records), "records in hpd_contacts..."
        hpd_parties = set()
        for hpd_contact_record in hpd_contact_records:
            hpd_party = Owner({
                'name': hpd_contact_record['LastName'] + ', ' + hpd_contact_record['FirstName'],
                'addr1': str(hpd_contact_record['BusinessHouseNumber']) + ' ' + hpd_contact_record['BusinessStreetName'],
                'addr2': hpd_contact_record['BusinessApartment'],
                'city': hpd_contact_record['BusinessCity'],
                'state': hpd_contact_record['BusinessState'],
                'zip': hpd_contact_record['BusinessZip'],
                'description': hpd_contact_record['ContactDescription'],
                'corporation_name': hpd_contact_record['CorporationName']
            })
            hpd_parties.add(hpd_party)
    
        print hpd_parties
        #Extract information

        #FINISH STEP 7

        print "STEP 8: DOF Tax Bills"
        tax_records = list(self.db.dof_taxes.find({'ws-out-id-boro':borough, 'ws-out-id-block':block, 'ws-out-id-lot':lot}))
        print "Found", len(tax_records), "records in DOF tax bills..."
        #Extract information
        tax_parties = set()
        for tax_record in tax_records:
            tax_party = Owner({
                'name': tax_record['ws-out-nm-recipient-1'] + ' ' + tax_record['ws-out-nm-recipient-2'] + ' ' + tax_record['ws-out-ad-name-attention'],
                'addr1': str(tax_record['ws-out-ad-street-no']) + ' ' + tax_record['ws-out-ad-street-1'],
                'addr2': tax_record['ws-out-ad-street-2'],
                'city': tax_record['ws-out-ad-city'],
                'state': tax_record['ws-out-cd-addr-state'],
                'zip': tax_record['ws-out-cd-addr-zip']
            })
            tax_parties.add(tax_party)

        print tax_parties

        #FINISH STEP 8

        print "STEP 9: DOS"
        #Need to do it fuzzily by matching name?