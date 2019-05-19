import datetime

split_date = datetime.datetime(2018, 1, 1)

with open('patent_target.pyobj', 'r', encoding='utf-8') as fin:
    patent_target = eval(fin.read())

with open('corpus.pyobj', 'r', encoding='utf-8') as fin:
    corpus = eval(fin.read())

train = {}
test = {}
count = 0
remove_list = set()
test_list = set()
for number in patent_target:
    if patent_target[number]['date'] >= split_date:
        test_list.add(number)
print(test_list)

for number in patent_target:
    count += 1
    if count % 10000 == 0:
        print(count)
    citation = patent_target[number]['citation']
    tmp = []
    for item in citation:
        if item not in test_list:
            tmp.append(item)
    if len(tmp) > 0:
        if patent_target[number]['date'] >= split_date:
            test[number] = tmp
        else:
            train[number] = tmp
    else:
        remove_list.add(number)

with open('train.tsv', 'w', encoding='utf-8') as fout:
    fout.write('number\tcitation\n')
    for number in train:
        fout.write('%s\t%s\n' % (number, ','.join(train[number])))

with open('test.tsv', 'w', encoding='utf-8') as fout:
    fout.write('number\tcitation\n')
    for number in test:
        fout.write('%s\t%s\n' % (number, ','.join(test[number])))

print('patent_target:', len(patent_target))
print('corpus:', len(corpus))

for item in remove_list:
    del patent_target[item]

for item in remove_list:
    corpus.remove(item)

with open('remove_patent_target.pyobj', 'w', encoding='utf-8') as fout:
    fout.write(str(patent_target))

with open('remove_corpus.pyobj', 'w', encoding='utf-8') as fout:
    fout.write(str(corpus))

print('patent_target:', len(patent_target))
print('corpus:', len(corpus))
print('train:', len(train))
print('test:', len(test))

'''
patent_target: 1158994
corpus: 3881549
patent_target: 985560
corpus: 3708115
train: 865042
test: 120518
'''