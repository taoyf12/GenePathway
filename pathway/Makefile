echo ===Compile & Set=====================================================================
proppr compile pathway.ppr
proppr set --programFiles pathway.wam:labels.cfacts:pathway.graph
echo ===Ground============================================================================
proppr answer train.examples --apr eps=1e-4 --threads 20 > answer.out
