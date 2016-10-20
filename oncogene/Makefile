compile:
	export PROPPR_JAVA_ARGS=-Xmx140g
	proppr compile oncogene.ppr
	proppr set --programFiles oncogene.wam:isSGA.cfacts:isDEG.cfacts:sgaInPatient.cfacts:degInPatient.cfacts:gotCancer.cfacts:sga2deg.graph
	proppr answer test.examples --apr eps=1e-7 --threads 20 > answer_test.out