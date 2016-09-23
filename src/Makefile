compile:
	#source /usr1/public/yifeng/GenePathway/ProPPR/init.sh
	#export PROPPR=`/usr1/public/yifeng/GenePathway/ProPPR`
	#export PATH=$PATH:$PROPPR/scripts
	export PROPPR_JAVA_ARGS=-Xmx140g
	proppr compile pathway.ppr
	proppr set --programFiles pathway.wam:labels.cfacts:pathway.graph
	# proppr answer train.examples --apr eps=1e-4 --threads 20 > answer_train.out
	proppr answer test.examples --apr eps=1e-4 --threads 20 > answer_test.out
	#proppr ground train.examples --apr eps=1e-4 --threads 20 > ground_train.out
	#proppr train train.grounded --apr eps=1e-4 --epochs 10 --threads 30 > train.out