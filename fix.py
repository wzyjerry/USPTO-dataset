test_list = set()
with open('test.tsv') as fin:
    fin.readline()
    for line in fin:
        line = line.split()[0]
        test_list.add(line)
count = 0
with open('cls.txt') as clsin:
    with open('cls_id.txt') as clsid:
        with open('train_cls_id.txt', 'w', encoding='utf-8') as train_id:
            with open('train_cls.txt', 'w', encoding='utf-8') as train:
                with open('test_cls.txt', 'w', encoding='utf-8') as test:
                    with open('test_cls_id.txt', 'w', encoding='utf-8') as test_id:
                        for line in clsid:
                            line = line.strip()
                            txt = clsin.readline()
                            if line in test_list:
                                test.write(txt)
                                test_id.write(line)
                                test_id.write('\n')
                            else:
                                train.write(txt)
                                train_id.write(line)
                                train_id.write('\n')
