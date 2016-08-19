echo ==Copying==========================================================================
rm examples
cp ../pathway/{proppr.settings,pathway.graph,pathway.wam} ./
echo ==Grounding========================================================================
proppr ground train.examples --apr eps=1e-5 --threads 20 > ground.out
echo ==Training=========================================================================
proppr train train.grounded --apr eps=1e-5 --epochs 1 --threads 30 > train.out
#proppr answer train.examples --apr eps=1e-4 --params train.params > answer.out
#proppr eval train.examples train.solutions.txt --metric p1 > eval.out

