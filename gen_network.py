import re
from multiprocessing import Pool
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from datetime import datetime

def fetch_db(host:str) -> Database:
    return MongoClient(host, 9001)['uspto_patent']

def fetch_patent_all(db:Database) -> Collection:
    return db['patent_all']
    
def batch(args:list) -> (set, set, list):
    now = args[0]
    patents = args[1]
    db = fetch_db('localhost')
    patent_all = fetch_patent_all(db)
    print(datetime.now(), 'Start', now)
    inventor = set()
    assignee = set()
    relation = []
    for number in patents:
        patent = patent_all.find_one({'number': number}, projection=['inventor', 'assignee'])
        for item in patent['inventor']:
            inventor.add(item['id'])
            relation.append(('I', number, item['id']))
        for item in patent['assignee']:
            assignee.add(item['id'])
            relation.append(('A', number, item['id']))
    print(datetime.now(), 'End', now)
    return inventor, assignee, relation

def gen_network(filename:str) -> None:
    with open(filename) as fin:
        corpus = list(eval(fin.read()))
    total = len(corpus)
    print('total:', total)
    patents = []
    inventor = set()
    assignee = set()
    relation = []
    for x in range(int(total / 10000) + 1):
        patents.append((x, corpus[x*10000:(x+1)*10000]))
    with Pool() as p:
        for i, a, r in p.map(batch, patents):
            inventor.update(i)
            assignee.update(a)
            relation.extend(r)
    nxt = 0
    i2id = {}
    for item in inventor:
        nxt += 1
        i2id[item] = nxt
    nxt = 0
    a2id = {}
    for item in assignee:
        nxt += 1
        a2id[item] = nxt
    nxt = 0
    p2id = {}
    for item in corpus:
        nxt += 1
        p2id[item] = nxt
    with open('edges.tsv', 'w', encoding='utf-8') as fout:
        fout.write('#source_node\tsource_class\tdest_node\tdest_class\tedge_class\n')
        for item in relation:
            if item[0] == 'I':
                fout('%d\tP\t%d\tI\tP-I\n' % (p2id[item[1]], i2id[item[2]]))
                fout('%d\tI\t%d\tP\tI-P\n' % (i2id[item[2]], p2id[item[1]]))
            else:
                fout('%d\tP\t%d\tA\tP-A\n' % (p2id[item[1]], a2id[item[2]]))
                fout('%d\tA\t%d\tP\tA-P\n' % (a2id[item[2]], p2id[item[1]]))
    with open('i2id.pyobj', 'w', encoding='utf-8') as fout:
        fout.write(str(i2id))
    with open('a2id.pyobj', 'w', encoding='utf-8') as fout:
        fout.write(str(a2id))
    with open('p2id.pyobj', 'w', encoding='utf-8') as fout:
        fout.write(str(p2id))

if __name__ == "__main__":
    gen_network('remove_corpus.pyobj')
