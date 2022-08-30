#!/bin/sh
# This file is called ./miniExtractHisto.sh histoName

aa=$PWD
echo "actual path : $aa"

STR=$aa
Choice='Local'
for SUB in 'llr' 'pbs' 'cern'
do
  if [[ "$STR" == *"$SUB"* ]]; then
    echo "It's $SUB there.";
    Choice=${SUB^^};
  fi
done

echo "Choice is : $Choice"

if [[ "$Choice" == "LLR" ]] 
  then
    echo "LLR"
elif [[ "$Choice" == "PBS" ]] 
  then
    echo "PBS"
    module load Programming_Languages/python/3.9.1
    module load Compilers/gcc/9.3.1
    module load DataManagement/xrootd/4.8.1
    module load Analysis/root/6.24.06
elif [[ "$Choice" == "CERN" ]] 
  then
    echo "PBS"

fi

python miniExtractHisto.py $1

echo 'END'
