from multiprocessing import Pool
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from datetime import datetime

def fetch_db(host:str) -> Database:
    return MongoClient(host, 9001)['uspto_patent']

def fetch_patent_all(db:Database) -> Collection:
    return db['patent_all']

def gen_list(start):
    start *= 1000
    db = fetch_db('localhost')
    patent_all = fetch_patent_all(db)
    print(datetime.now(), 'Start:', start)
    patent_target = {}
    corpus = set()
    for doc in patent_all.find({'date': {'$gte': datetime.strptime(r'2015-01-01', r'%Y-%m-%d')}}, projection=['number', 'citation', 'date']).skip(start).limit(1000):
        number = doc['number']
        patent_target[number] = {
            'date': doc['date'],
            'citation': []
        }
        corpus.add(number)
        for item in doc['citation']:
            citation_id = item['citation_id']
            if patent_all.count_documents({'number': citation_id}) > 0:
                corpus.add(citation_id)
                patent_target[number]['citation'].append(citation_id)
    print(datetime.now(), 'End:', start)
    return patent_target, corpus

if __name__ == "__main__":
    db = fetch_db('localhost')
    patent_all = fetch_patent_all(db)

    patent_target = {}
    corpus = set()

    total = patent_all.count_documents({'date': {'$gte': datetime.strptime(r'2015-01-01', r'%Y-%m-%d')}})
    with Pool() as p:
        for a_target, a_corpus in p.map(gen_list, range(int(total / 1000) + 1)):
            patent_target.update(a_target)
            corpus.update(a_corpus)            
    
    with open('patent_target.pyobj', 'w', encoding='utf-8') as fout:
        fout.write(str(patent_target))
    with open('corpus.pyobj', 'w', encoding='utf-8') as fout:
        fout.write(str(corpus))
    print('patent_target:', len(patent_target))
    print('corpus:', len(corpus))

'''
patent_target: 1158994
corpus: 3881549
'''