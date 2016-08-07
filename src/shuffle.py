# prepare the files required by ProPPR.
# TODO: add edges to node itself
from random import shuffle

if __name__ == '__main__':

    examples = []
    path_all = '../pathway/examples'
    for line in open(path_all, 'r'):
        examples.append(line)
    shuffle(examples)
    cut = int(0.8*len(examples))
    train = examples[1:cut]
    test = examples[cut+1:len(examples)]

    path_train = '../pathway/train.examples'
    path_test = '../pathway/test.examples'
    f = open(path_train,'w')
    for line in train:
        print >> f, '%s'.format(line)
    f.close
    f = open(path_test,'w')
    for line in test:
        print >> f, '%s'.format(line)
    f.close




