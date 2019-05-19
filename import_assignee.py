from multiprocessing import Pool
from pymongo import MongoClient, UpdateOne
from pymongo.database import Database
from pymongo.collection import Collection
from datetime import datetime

def fetch_db(host:str) -> Database:
    return MongoClient(host, 9001)['uspto_patent']

def fetch_patent_assignee(db:Database) -> Collection:
    return db['patent_assignee']

def fetch_assignee(db:Database) -> Collection:
    return db['assignee']

def fetch_patent15(db:Database) -> Collection:
    return db['patent_15']

def insert_assignee(start:int) -> None:
    start *= 10000
    db = fetch_db('localhost')
    patent_15 = fetch_patent15(db)
    patent_assignee = fetch_patent_assignee(db)
    assignee = fetch_assignee(db)
    op = []
    for doc in patent_15.find(projection=['number'], no_cursor_timeout=True).skip(start).limit(10000):
        patent_id = doc['number']
        ass = []
        for id_doc in patent_assignee.find({'patent_id': patent_id}, projection=['assignee_id']):
            ass.append(assignee.find_one({'id': id_doc['assignee_id']}))
        op.append(UpdateOne({'number': patent_id}, {'$set': {'assignee': ass}}))
    print(datetime.now(), start)
    patent_15.bulk_write(op, ordered=False)
    print(datetime.now(), start, 'end')


if __name__ == "__main__":
    db = fetch_db('localhost')
    patent_15 = fetch_patent15(db)
    patent_assignee = fetch_patent_assignee(db)
    assignee = fetch_assignee(db)
    patent_15.update_many({'assignee': {'$exists': True}}, {'$unset': {'assignee': ''}})
    print(datetime.now(), 'Clean end.')
    total = patent_15.count()
    print('total', total)
    with Pool(32) as pool:
        pool.map(insert_assignee, range(int(total / 10000)))
