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

def gen_text(patent:dict) -> list:
    text = []
    if 'brf_sum_text' in patent:
        text.append(patent['brf_sum_text'])
    if 'title' in patent:
        text.append(patent['title'])
    if 'abstract' in patent:
        text.append(patent['abstract'])
    if 'claim' in patent:
        text.append(patent['claim'])
    text = ' '.join(text).lower()
    text = re.split(r'[.\\!?,\'/()]', text)
    return ' '.join(text).split()

def batch(args) -> dict:
    now = args[0]
    patents = args[1]
    db = fetch_db('localhost')
    patent_all = fetch_patent_all(db)
    print(datetime.now(), 'Start', now)
    result = {}
    for item in patents:
        patent = patent_all.find_one({'number': item}, projection=['brf_sum_text', 'title', 'abstract', 'claim', 'ipcr'])
        text = gen_text(patent)
        result[item] = '%s\t%s\n' % (' '.join(text[:500]), '   '.join(['__label__' + x for x in patent['ipcr']]))
    print(datetime.now(), 'End', now)
    return result

def make_cls_corpus(filename:str, test:str) -> None:
    with open(filename) as fin:
        corpus = list(eval(fin.read()))
    patent_text = {}
    total = len(corpus)
    print('total:', total)
    patents = []
    for x in range(int(total / 10000) + 1):
        patents.append((x, corpus[x*10000:(x+1)*10000]))
    with Pool() as p:
        for item in p.map(batch, patents):
            patent_text.update(item)
    test_list = set()
    with open(test) as fin:
        fin.readline()
        for line in fin:
            line = line.split()[0]
            test_list.add(line)
    with open('train_cls_id.txt', 'w', encoding='utf-8') as train_id:
        with open('train_cls.txt', 'w', encoding='utf-8') as train:
            with open('test_cls.txt', 'w', encoding='utf-8') as test:
                with open('test_cls_id.txt', 'w', encoding='utf-8') as test_id:
                    for item in patent_text:
                        if item in test_list:
                            test.write(patent_text[item])
                            test_id.write(item)
                            test_id.write('\n')
                        else:
                            train.write(patent_text[item])
                            train_id.write(item)
                            train_id.write('\n')

if __name__ == "__main__":
    make_cls_corpus('remove_corpus.pyobj', 'test.tsv')
