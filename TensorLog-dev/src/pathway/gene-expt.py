import logging

import expt
import tensorlog
import learn
import plearn

import time


def ruleWeights(prog):
    db = prog.db
    ruleWeights = db.matEncoding[('weighted',1)]
    return db.rowAsSymbolDict(ruleWeights)

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info('level is info')
    
    db = tensorlog.parseDBSpec('pathway.db|pathway.cfacts')
    trainData = tensorlog.parseDatasetSpec('train.dset|train.exam',db)
    testData = tensorlog.parseDatasetSpec('test.dset|test.exam',db)
    prog = tensorlog.parseProgSpec('pathway.ppr',db,proppr=True)
    prog.setRuleWeights()

    print 'init ruleWeights',ruleWeights(prog)

    # the parameters for feature
    prog.db.markAsParam('src',1)
    prog.db.markAsParam('dst',1)

    # the depth of learning
    prog.maxDepth = 15

    def myTracer(learner,ctr,**kw):
        print 'rule weights',ruleWeights(learner.prog)
        learn.EpochTracer.default(learner,ctr,**kw)

    learner = plearn.ParallelFixedRateGDLearner(
      prog,
      regularizer=learn.L2Regularizer(),
      parallel=48,
      epochs=10,
      miniBatchSize=100,
      epochTracer=myTracer,
      rate=0.0001)
    params = {'prog':prog,
              'trainData':trainData, 'testData':testData,
              'targetMode':'pathTo/io',
              'savedModel':'tmp-cache/gene-trained.db',
              'savedTestPredictions':'tmp-cache/gene-test.solutions.txt',
              'savedTrainExamples':'tmp-cache/gene-train.examples',
              'savedTestExamples':'tmp-cache/gene-test.examples',
              'learner':learner
    }
    print 'maxdepth', prog.maxDepth

    start_time = time.time()
    expt.Expt(params).run()
    elapsed_time = time.time() - start_time
    print elapsed_time
