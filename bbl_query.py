from pymongo import MongoClient
from datetime import datetime
from owner import Owner
from bbl import BBL
from building import Building

class BBLQuery:
    def __init__(self, host, port):
        client = MongoClient(host, port)
        self.db = client.furman
        
    def normalize_str(self, string):
        return string.replace('|', ',')
        
    def query_lots(self, bbl):
        '''
        This part is used to get all lots associated with a borough and block
        '''
        borough = bbl.borough
        block = bbl.block
        
        bbl_records = list(self.db.lot_records.find({'Borough':borough,'Block':block}, {'Lot':1}))
        print "Found", len(bbl_records), "BBL in this area..."
        lots = set()
        for bbl_record in bbl_records:
            lots.add(bbl_record['Lot'])
        return lots
        
    def get_bbls(self, bbl):
        '''
        This part will construct ALL bbls for a given borough and block
        '''
        lots = self.query_lots(bbl)
        bbls = set()
        for lot in lots:
            bbls.add(BBL(bbl.borough, bbl.block, lot))
        return bbls
        
    def get_blocks(self, borough):
        block_records = list(self.db.lot_records.find({'Borough':borough}, {'Block':1}))
        blocks = set()
        for block_record in block_records:
            blocks.add(block_record['Block'])
        return blocks
        
    def match_owner(self, owner1, owner2):
        '''
        Each owner is a record of name and address
        '''
        
    def query_bbl(self, bbl):
        borough = bbl.borough
        block = bbl.block
        lot = bbl.lot
        bbl_repr = bbl.bbl_repr
        print "BBL:", bbl
        
        #This is the output
        building = Building(bbl)
        
        print "=== STEP 1: ==="
        lot_records = list(self.db.lot_records.find({'Borough':borough,'Block':block,'Lot':lot}))
        print "Found", len(lot_records), "records in lot_records..."
        unique_keys = list()
        for lot_record in lot_records:
            unique_keys.append(lot_record['Unique_Key'])

        master_records = list(self.db.master_records.find({'Unique_Key':{'$in':unique_keys}}))
        print "Found", len(master_records), "records in master_records..."
        latest_unique_key = None
        latest_doc_date = datetime.strptime('1970-01-01', '%Y-%m-%d')
        for master_record in master_records:
            if master_record['Document_Date'] == "":
                continue
            if master_record['Doc_type'][0:4] == 'DEED':
                if datetime.strptime(master_record['Document_Date'], '%Y-%m-%d') > latest_doc_date:
                    latest_unique_key = master_record['Unique_Key']
                    latest_doc_date = datetime.strptime(master_record['Document_Date'], '%Y-%m-%d')

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

        print "=== STEP 2: ==="
        party_records = list(self.db.party_records.find({'Unique_Key':latest_unique_key}))
        print "Found", len(party_records), "records in party_records..."
        primary_party = None
        for party_record in party_records:
            if party_record['Party_type'] == 2:
                primary_party = Owner({
                    'name': self.normalize_str(party_record['Name']),
                    'addr1': self.normalize_str(party_record['Addr1']),
                    'addr2': self.normalize_str(party_record['Addr2']),
                    'city': party_record['City'],
                    'state': party_record['State'],
                    'zip': party_record['Zip']
                })

        if primary_party is None:
            print "No name found!"
            return None
        else:
            print "Primary party is ", primary_party['name']
        print primary_party
        
        building.primary = primary_party
    
        #FINISH STEP 2

        print "=== STEP 3: ==="
        secondary_unique_keys = list()
        for master_record in master_records:
            if master_record['Document_Date'] == "":
                continue
            if datetime.strptime(master_record['Document_Date'], '%Y-%m-%d') < latest_doc_date:
                continue
            #if master_record['doc_type'][0:4] == 'MTGE' or master_record['doc_type'][0:4] == 'AGMT':
            if master_record['Doc_type'][0:4] == 'MTGE': #Not consider AGMT right now
                secondary_unique_keys.append(master_record['Unique_Key'])
        
        print "Found", len(secondary_unique_keys), "secondary UKs: ", secondary_unique_keys

        #FINISH STEP 3

        print "=== STEP 4: ==="
        party_records = list(self.db.party_records.find({'Unique_Key':{'$in': secondary_unique_keys}}))
        print "Found", len(party_records), "records in party_records..."
        secondary_parties = set()
        for party_record in party_records:
            if party_record['Party_type'] == 1:
                secondary_party = Owner({
                    'name': self.normalize_str(party_record['Name']),
                    'addr1': self.normalize_str(party_record['Addr1']),
                    'addr2': self.normalize_str(party_record['Addr2']),
                    'city': party_record['City'],
                    'state': party_record['State'],
                    'zip': party_record['Zip']
                })
                secondary_parties.add(secondary_party)
        
        print "Found", len(secondary_parties), "secondary parties..."
        for secondary_party in secondary_parties:
            print "Name:", secondary_party['name']
    
        print secondary_parties
        
        building.secondary = secondary_parties
    
        #FINISH STEP 4

        print "=== STEP 5: ==="
        lot_records = list(self.db.lot_records.find({'Unique_key':{'$in': secondary_unique_keys}}))
        print "Found", len(lot_records), "records in lot_records..."
        cache_bbls = set([bbl])
        for lot_record in lot_records:
            secondary_bbl = BBL(lot_record['Borough'], lot_record['Block'], lot_record['Lot'])
            cache_bbls.add(secondary_bbl)
            
        secondary_bbls = cache_bbls.difference(set([bbl]))
        print "These are secondary BBLs:"
        for secondary_bbl in secondary_bbls:
            print secondary_bbl
            
        building.linkedbbls = secondary_bbls
        
        #FINISH STEP 5

        print "=== STEP 6: HPD ==="
        hpd_records = list(self.db.hpd.find({'bbl':bbl_repr}))
        print "Found", len(hpd_records), "records in hpd..."
        #Get the first one
        if len(hpd_records) == 0:
            print "No HPD records!"
        else:
            hpd_record = hpd_records[0]
            hpd_reg_id = hpd_record['RegistrationID']
            #FINISH STEP 6

            print "=== STEP 7: HPD Contacts ==="
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
            
            building.hpd = hpd_parties

        #FINISH STEP 7

        print "=== STEP 8: DOF Tax Bills ==="
        tax_records = list(self.db.dof_taxes.find({'id-boro':borough, 'id-block':block, 'id-lot':lot}))
        print "Found", len(tax_records), "records in DOF tax bills..."
        #Extract information
        tax_parties = set()
        for tax_record in tax_records:
            tax_party = Owner({
                'name': tax_record['nm-recipient-1'] + ' ' + tax_record['nm-recipient-2'] + ' ' + tax_record['ad-name-attention'],
                'addr1': str(tax_record['ad-street-no']) + ' ' + tax_record['ad-street-1'],
                'addr2': tax_record['ad-street-2'],
                'city': tax_record['ad-city'],
                'state': tax_record['cd-addr-state'],
                'zip': tax_record['cd-addr-zip']
            })
            tax_parties.add(tax_party)

        print tax_parties
        
        building.tax = tax_parties

        #FINISH STEP 8

        print "STEP 9: DOS"
        #Need to do it fuzzily by matching name?
        
        return building