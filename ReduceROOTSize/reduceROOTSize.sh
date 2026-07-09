#!/bin/sh
# This file is called . reduceROOTSize.sh
# and leads to reduce the size of the ROOT files
# keeping the paths = ['DQMData/Run 1/EgammaV', 'DQMData/Run 1/Info'] paths.

#Black        0;30     Dark Gray     1;30
#Red          0;31     Light Red     1;31
#Green        0;32     Light Green   1;32
#Brown/Orange 0;33     Yellow        1;33
#Blue         0;34     Light Blue    1;34
#Purple       0;35     Light Purple  1;35
#Cyan         0;36     Light Cyan    1;36
#Light Gray   0;37     White         1;37
B_BLUE="\\e[1;34m"
B_GREEN="\033[1;32m"
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'

NC='\033[0m' # No Color

a=()

PATH_INIT=$PWD
#localPath='/sps/cms/chiron/REGENERATION/ZpToEE'
#localPath='/eos/home-a/archiron/HGCal_Shares'
localPath='/eos/home-a/archiron/TEST_GITCLONE/quickValidationsNG/DATA'
#localPath='/afs/cern.ch/work/a/archiron/private/TEST_GITCLONE/quickValidationsNG/DATA/'
#localPath='/home/arnaud/cernbox/TEST_GITCLONE/quickValidationsNG/DATA'
#localPath='/eos/home-a/archiron/OLD_THINGS/AllSteps/Stockage'
#localPath='/eos/home-a/archiron/TEST_GITCLONE/quickValidationsNG/Tests'
echo "working on $localPath"

sName='DQM_V' # degin of the name
#sName='step'
#sName='DQMIO'

extension='root'

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
a=`find . -type f | grep $extension `
for name in ${a[@]}
do
  if [[ "$name" == *"$sName"* ]]; then # test with the begin of the name
    FILESIZE=$(stat -c%s "$name")
    echo -e "${B_GREEN}$name${NC} $FILESIZE"
    if [ $FILESIZE -ge 2500000 ] # test with file size
    then
      python3 $PATH_INIT/reduceSize1File.py $name
    else
      echo -e "${B_BLUE}size too small${NC}"
    fi
  fi
done

cd $PATH_INIT
echo "END"

