import logging

import expt
import tensorlog
import learn
import plearn

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info('level is info')
    
    db = tensorlog.parseDBSpec('pathway.cfacts')
    trainData = tensorlog.parseDatasetSpec('train.exam',db)
    testData = tensorlog.parseDatasetSpec('test.exam',db)
    prog = tensorlog.parseProgSpec('pathway.ppr',db,proppr=True)
    prog.setRuleWeights()
    # the parameters for feature?
    prog.db.markAsParam('src',1)
    prog.db.markAsParam('dst',1)
    # the depth of learning?
    prog.maxDepth = 5
    learner = plearn.ParallelFixedRateGDLearner(prog,regularizer=learn.L2Regularizer(),parallel=28,epochs=5)
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
    expt.Expt(params).run()

