echo ===CompileAndSet=====================================================================
export PROPPR_JAVA_ARGS=-Xmx140g
proppr compile pathway.ppr
proppr set --programFiles pathway.wam:labels.cfacts:pathway.graph
echo ===Ground============================================================================
proppr answer train.examples --apr eps=1e-5 --threads 20 > answer.out
