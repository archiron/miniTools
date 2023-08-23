#!/bin/sh
# This file is called . reduceROOTSize.sh
# and leads to reduce the size of the ROOT files
# keeping the paths = ['DQMData/Run 1/EgammaV', 'DQMData/Run 1/Info'] paths.

a=()

PATH_INIT=$PWD
localPath='/sps/cms/chiron/REGENERATION/ZpToEE'
sName='DQM_V' # degin of the name

for SUB in 'llr' 'pbs'
do
  if [[ "$PATH_INIT" == *"$SUB"* ]]; then
    echo "It's $SUB there.";
    Choice=${SUB^^};
  fi
done

if [[ "$Choice" == "LLR" ]] 
  then
    echo "LLR"
    source /opt/exp_soft/llr/root/v6.24.04-el7-gcc9xx-py370/etc/init.sh
elif [[ "$Choice" == "PBS" ]] 
  then
    echo "PBS"
    module purge
    module load Programming_Languages/python/3.9.1
    module load Compilers/gcc/9.3.1
    module load DataManagement/xrootd/4.8.1
    module load Analysis/root/6.24.06
fi

cd $localPath # 
# get the releases list
a=`find . -type f | grep root `
for name in ${a[@]}
do
  if [[ "$name" == *"$sName"* ]]; then # test with the begin of the name
    FILESIZE=$(stat -c%s "$name")
    echo $name $FILESIZE
    if [ $FILESIZE -ge 2500000 ] # test with file size
    then
      python3 $PATH_INIT/reduceSize1File.py $name
    else
      echo "size too small"
    fi
  fi
done

cd $PATH_INIT
echo "END"

