echo ==Copying==========================================================================
rm examples_train
cp ../pathway_patient/{proppr.settings,pathway.graph,pathway.wam,test.examples} ./
echo ==Grounding========================================================================
proppr ground train.examples --apr eps=5e-5 --threads 20 > ground.out
echo ==Training=========================================================================
proppr train train.grounded --apr eps=5e-5 --epochs 1 --threads 30 > train.out
proppr answer train.examples --apr eps=5e-5 --params train.params --threads 20 > answer.out
proppr eval train.examples train.solutions.txt --metric p1 --echo --details > eval.out
proppr answer test.examples --apr eps=5e-5 --params train.params --threads 20 > answer_test.out
proppr eval test.examples test.solutions.txt --metric p1 --echo --details > eval_test.out

