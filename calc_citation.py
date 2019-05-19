from pymongo import MongoClient, UpdateOne
from pymongo.database import Database
from pymongo.collection import Collection

def fetch_db(host:str) -> Database:
    return MongoClient(host, 9001)['uspto_patent']

def fetch_patent_all(db:Database) -> Collection:
    return db['patent_all']

if __name__ == "__main__":
    db = fetch_db('localhost')
    patent_all = fetch_patent_all(db)
    
    cit_in = {}
    cit_out = {}
    count = 0
    for doc in patent_all.find(no_cursor_timeout=True, projection=['number', 'citation']):
        count += 1
        if count % 10000 == 0:
            print(count)
        patent_id = doc['number']
        cit_out[patent_id] = 0
        for item in doc['citation']:
            if 'citation_id' in item:
                cit_out[patent_id] += 1
                citation_id = item['citation_id']
                cit_in.setdefault(citation_id, 0)
                cit_in[citation_id] += 1
    
    cit = {}
    sum_in = 0
    sum_out = 0
    count = 0
    for i in cit_out:
        cit[i] = cit_out[i]
        sum_out += cit_out[i]
        if i in cit_in:
            cit[i] += cit_in[i]
            sum_in += cit_in[i]
        if cit[i] > 0:
            count += 1
    print('cit_out:', len(cit_out))
    print('cit_in:', len(cit_in))
    print('cit:', count)
    print('sum_in:', sum_in, sum_in / count)
    print('sum_out:', sum_out, sum_out / count)

'''
cit_out: 6647699
cit_in: 8271669
cit: 6450458
sum_in: 75420603 11.692286501206581
sum_out: 94726688 14.68526544936809
'''