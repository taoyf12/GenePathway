newdir='trial003'
mkdir tmpdir
rm -r tmp-cache
mkdir tmp-cache
export PYTHONPATH=$PYTHONPATH:/usr1/public/yifeng/GenePathway/TensorLog-dev/src
python gene-expt.py > out.txt 2> log.txt
cp * tmpdir
cp -r tmp-cache tmpdir
mv tmpdir $newdir