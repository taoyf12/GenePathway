echo 'CompileAndSet====================================================================='
export PROPPR_JAVA_ARGS=-Xmx140g
proppr compile pathway.ppr
proppr set --programFiles pathway.wam:labels.cfacts:pathway.graph
echo 'Grounding========================================================================='
proppr answer train.examples --apr eps=1e-4 --threads 20 > answer_train.out
proppr answer test.examples --apr eps=1e-4 --threads 20 > answer_test.out
# proppr answer remain.examples --apr eps=1e-4 --threads 20 > answer_remain.out