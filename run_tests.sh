#!/bin/sh

golden=$1
mutations=$2
vectors=$3
outdir=$4

echo "Golden"
./golden.py $golden $vectors $outdir/golden

src=`basename $golden`

for f in $mutations/v*
do
  v=`basename $f`
  mutated=$f/$src
  echo $v
  ./mutated.py $golden $mutated $vectors $outdir/golden $outdir/$v
done
