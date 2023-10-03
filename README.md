# miniTools
only to generate one histo  from one ROOT file or one comparison between 2 histos from 2 ROOT files.

sources.py<br>
++++<br>
input_rel_file : ROOT file name, used to generate one histo from one ROOT file.
input_ref_file : ROOT file name, used for the comparison with the input_rel_file ROOT file.

histoName : name of the histo to be generated<br>
++++<br>
dataPath : path to be used where the previous ROOT file are located. A DATA folder is given to set locally those ROOT files.
The data
The path MUST be with full path (not with ../).

miniExtractHisto.py<br>
++++<br>
python script used for the generation. It use the HistosConfigFiles folder for the parameters of each histogram.
It also create a local folder to put the pictures in with the histo name as a folder name.
By default, all cases of RECO, Fake, Pt1000 and miniAOD are made (tp, th).

miniExtractHisto.sh<br>
++++<br>
sh script used to launch the computation. 
With it the histogram can be generated onto lxplus, cca or LLR workers.

One can use the ReduceRootSize folder by modifiyng the localPath variable and launch : . reduceRootSize.sh

++++<br>
cloning from git :
git clone https://github.com/archiron/miniTools/ miniTools
