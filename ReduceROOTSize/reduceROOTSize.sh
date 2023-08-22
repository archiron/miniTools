#!/bin/sh
# This file is called . reduceROOTSize.sh
# and leads to reduce the size of the ROOT files
# keeping the paths = ['DQMData/Run 1/EgammaV', 'DQMData/Run 1/Info'] paths.

a=()

PATH_INIT=$PWD
localPath='/eos/home-a/archiron/TEST_GITCLONE/quickValidationsNG/DATA/'

cd $localPath # 
# get the releases list
a=`find . -type f | grep root `
for name in ${a[@]}
do
  FILESIZE=$(stat -c%s "$name")
  echo $name $FILESIZE
  if [ $FILESIZE -ge 200000 ]
  then
    python3 $PATH_INIT/reduceSize1File.py $name
  fi
done

cd $PATH_INIT
echo "END"

