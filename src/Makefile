compile:
	export PROPPR_JAVA_ARGS=-Xmx140g
	proppr compile pathway.ppr
	proppr set --programFiles pathway.wam:labels.cfacts:pathway.graph
	proppr answer test.examples --apr eps=1e-7 --threads 20 > answer_test.out
	