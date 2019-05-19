a = set()
b = set()
count = 0
with open('test.tsv') as fin:
    fin.readline()
    for line in fin:
        line = line.split()
        a.add(line[0])
        if len(line[1].split(',')) == 0:
            count += 1
        for item in line[1].split(','):
            b.add(item)
with open('train.tsv') as fin:
    fin.readline()
    for line in fin:
        line = line.split()
        b.add(line[0])
        if len(line[1].split(',')) == 0:
            count += 1
        for item in line[1].split(','):
            b.add(item)

print(count)
print(len(a))
print(len(b))
print(a & b)
'''
0
120518
3604370
set()
'''