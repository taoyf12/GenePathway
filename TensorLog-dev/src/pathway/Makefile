# directory to contain files
newdir='trial015'

# train
export PYTHONPATH=$PYTHONPATH:/usr1/public/yifeng/GenePathway/TensorLog-dev/src

rm -r $newdir
mkdir $newdir
rm -r tmp-cache
mkdir tmp-cache
echo 'training...'
python gene-expt.py > out.txt 2> log.txt

# save trained params
echo 'saving params...'
echo 'params_0_rule' > params.out
python -m list --db tmp-cache/gene-trained.db --mode rule/1 | sort -gr -k3 >> params.out
echo 'params_1_src' >> params.out
python -m list --db tmp-cache/gene-trained.db --mode src/1 | sort -gr -k3 >> params.out
echo 'params_2_dst' >> params.out
python -m list --db tmp-cache/gene-trained.db --mode dst/1 | sort -gr -k3 >> params.out
echo 'params_3_weighted' >> params.out
python -m list --db tmp-cache/gene-trained.db --mode weighted/1 | sort -gr -k3 >> params.out
echo 'params_4_isDEG' >> params.out
python -m list --db tmp-cache/gene-trained.db --mode isDEG/1 | sort -gr -k3 >> params.out
echo 'params_5_leadTo' >> params.out
python -m list --db tmp-cache/gene-trained.db --mode leadTo/2 | sort -gr -k4 >> params.out
echo 'params_6_train' >> params.out
python -m list --db tmp-cache/gene-trained.db --mode train/2 | sort -gr -k4 >> params.out
echo 'params_7_test' >> params.out
python -m list --db tmp-cache/gene-trained.db --mode test/2 | sort -gr -k4 >> params.out

# move generated files
cp * $newdir
cp -r tmp-cache $newdir

# get roc
echo 'calculating roc...'
python /usr1/public/yifeng/GenePathway/src/predict_roc_test_ts.py --filename $newdir