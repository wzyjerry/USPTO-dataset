from multiprocessing import Pool
from pymongo import MongoClient, UpdateOne
from pymongo.database import Database
from pymongo.collection import Collection
from datetime import datetime

def fetch_db(host:str) -> Database:
    return MongoClient(host, 9001)['uspto_patent']

def fetch_patent(db:Database) -> Collection:
    return db['patent']

def fetch_patent_assignee(db:Database) -> Collection:
    return db['patent_assignee']

def fetch_assignee(db:Database) -> Collection:
    return db['assignee']

def fetch_patent_inventor(db:Database) -> Collection:
    return db['patent_inventor']

def fetch_inventor(db:Database) -> Collection:
    return db['inventor']

def fetch_ipcr(db:Database) -> Collection:
    return db['ipcr']

def fetch_brf_sum_text(db:Database) -> Collection:
    return db['brf_sum_text']

def fetch_claim(db:Database) -> Collection:
    return db['claim']

def fetch_uspatentcitation(db:Database) -> Collection:
    return db['uspatentcitation']

def fetch_patent_all(db:Database) -> Collection:
    return db['patent_all']

def insert(i):
    i *= 1000
    print(datetime.now(), 'Start:', i)
    db = fetch_db('localhost')
    patent = fetch_patent(db)
    patent_all = fetch_patent_all(db)
    patent_assignee = fetch_patent_assignee(db)
    assignee = fetch_assignee(db)
    patent_inventor = fetch_patent_inventor(db)
    inventor = fetch_inventor(db)
    ipcr = fetch_ipcr(db)
    brf_sum_text = fetch_brf_sum_text(db)
    claim = fetch_claim(db)
    uspatentcitation = fetch_uspatentcitation(db)

    documents = []
    for doc in patent.find(no_cursor_timeout=True, projection=['number', 'date', 'abstract', 'title']).limit(1000).skip(i):
        patent_id = doc['number']
        ass = []
        for id_doc in patent_assignee.find({'patent_id': patent_id}, projection=['assignee_id']):
            if 'assignee_id' in id_doc:
                ass.append(assignee.find_one({'id': id_doc['assignee_id']}))
        doc['assignee'] = ass
        inv = []
        for id_doc in patent_inventor.find({'patent_id': patent_id}, projection=['inventor_id']):
            if 'inventor_id' in id_doc:
                inv.append(inventor.find_one({'id': id_doc['inventor_id']}))
        doc['inventor'] = inv
        ipc = set()
        for ipcr_doc in ipcr.find({'patent_id': patent_id}, projection=['section', 'ipc_class', 'subclass']):
            if 'section' in ipcr_doc and 'ipc_class' in ipcr_doc and 'subclass' in ipcr_doc:
                ipc_class = ''.join([ipcr_doc['section'], ipcr_doc['ipc_class'], ipcr_doc['subclass']])
                if len(ipc_class) == 4:
                    ipc.add(ipc_class)
        doc['ipcr'] = list(ipc)
        sum_text = brf_sum_text.find_one({'patent_id': patent_id}, projection=['text'])
        if sum_text is not None:
            if 'text' in sum_text:
                doc['brf_sum_text'] = sum_text['text']
        claims = []
        for claim_doc in claim.find({'patent_id': patent_id}, projection=['text', 'sequence']):
            claims.append(claim_doc)
        claims = sorted(claims, key=lambda x: x['sequence'])
        claim_text = []
        for item in claims:
            if 'text' in item:
                claim_text.append(item['text'])
        doc['claim'] = ' '.join(claim_text)
        citation = []
        for citation_doc in uspatentcitation.find({'patent_id': patent_id}, projection=['citation_id', 'category']):
            citation.append(citation_doc)
        doc['citation'] = citation
        documents.append(doc)
    patent_all.insert_many(documents, ordered=False, bypass_document_validation=False)
    print(datetime.now(), 'End:', i)

if __name__ == "__main__":
    db = fetch_db('localhost')
    patent = fetch_patent(db)

    total = patent.count_documents({})
    print('total:', total)

    with Pool() as pool:
        pool.map(insert, range(int(total / 1000) + 1))
