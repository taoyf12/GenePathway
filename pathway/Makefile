compile:
	export PROPPR_JAVA_ARGS=-Xmx450g
	proppr compile pathway_raw.ppr
	proppr set --programFiles pathway_raw.wam:labels.cfacts:pathway.graph
	# proppr ground train.examples --apr eps=1e-4 --threads 20 > ground.out
	# proppr train train.grounded --apr eps=1e-4 --epochs 1 --threads 60 > train.out
	proppr answer test.examples --apr eps=1e-4 --params train.params --threads 20 > answer_test.out
	echo 'calculating roc...'
	python /home/yifengt/GenePathway/src/predict_roc_test_glosa.py --filename 'eps=1e-4wo0epoch'