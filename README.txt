Hello and welcome to MetClass! 

MetClass will take a file of chemical formulas and classify them into the Main Classes and Major Categories
as defined by Lipid MAPS (https://www.lipidmaps.org/data/classification/LM_classification_exp.php)

MetClass is currently distributed under a GNU GPLv3 liscense.

MetClass is currently available for Windows only, but expansion onto Linux and Mac platforms is underway.

To run MetClass, you will need R, Weka, and Python 3.6 or higher. 

The rest of this document outlines guidelines for MetClass usage.

For any questions regarding MetClass usage or errors, contact ehm79@cornell.edu

_________INSTALLING SOFTWARE FOR RUNNING METCLASS ON WINDOWS:_________

To run MetClass, you will first need to have R, Weka, and Python downloaded onto your device.
If you do not have all three softwares, follow the instructions below for installation.

If you already have Python v3 and did not install it through Anaconda, you will need several common Python 
packages: numpy, __future__, re, math, sys, os, and glob.

To download R: 
1) Go here: https://cran.r-project.org/mirrors.html
2) Select the mirror closest to your physical location
3) Select Download R for Windows
4) Click on "install R for the first time"
5) Click "Download R 3.X.X for Windows" in the box on top of the page
6) Follow the instructions on the pop-up boxes.

To download Weka: 
1) Go here: https://www.cs.waikato.ac.nz/ml/weka/
2) Select Download
3) To select the correct version of Weka to download, you must know your current version of java.
To find this out, open the Command Prompt and type "java -version". If your version is 1.8 or higher, you 
do not need to download any version of weka with a java VM, but if your version is lower than 1.8,
you do need to download a version with a java VM. Download the correct Weka 3-9 version for you.
4) Once you click on the right weka 3-9 version, it will launch a new tab, and a pop-up box will appear.
Follow the instructions on the pop-up boxes.

To download Python:
If you do not already have Python installed, the easiest installation process is through Anaconda.
Downloading python through Anaconda will automatically give you all the packages needed for MetClass.

1) Go here: https://www.anaconda.com/distribution/
2) Click on the Download button for "Python 3.X version"
3) This will open a pop-up box. Save the .exe file and follow the instructions on the box.

_________RUNNING METCLASS:_________

Once you have the necessary software installed, you can run MetClass.

MetClass has several required arguments. If you ever want to see what these arguments are, 
open Command Prompt and type:

"python *path_to_MetClass*/MetClassWrapper.py -h"

Where *path_to_MetClass* should be replaced with the path to where you downloaded MetClass. For example, if I
downloaded MetClass in my Documents folder, I would replace *path_to_MetClass* with 
C:/Users/Liz/Documents/MetClass

If you type the above line, you will see: 

        Required Arguments:
        -softdir = Directory containing scripts and required files
        -infile = Input file of formulas -- one formula per line. Files will be
                written to the directory containing this file
        -wekap = Full path to the weka.jar file
        -main_t = Impose a threshold on main category classification? yes OR no
        -sub_t = Impose a threshold on sub-class classification? yes OR no


For each of these arguments, we need the argument itself followed by your input, as per the example below,
for softdir: 

-softdir C:/Users/Liz/Documents/MetClass

A full example looks like this:

python C:/Users/Liz/Documents/MetClass/MetClassWrapper.py -softdir C:/Users/Liz/Documents/MetClass 
-infile C:/Users/Liz/Documents/Formulas/ExampleFormulas.txt -wekap C:/Program Files/Weka-3-9/weka.jar
-main_t no -sub_t no

Again, you should substitute the above paths with the paths to where you downloaded MetClass (for softdir),
the path to your file of input formulas (for infile), and the path to your weka.jar file (for wekap).
In general, THE PATHS (EXCEPTING THAT FOR WEKAP) SHOULD NOT HAVE SPACE CHARACTERS. If your paths do have 
space characters, please see the Notes for Usage section.
***An important note for the wekap argument is found in the Notes for Usage section of this document***

For running MetClass correctly, it is imperative that all files in MetClass are in the same folder. 
Your MetClass folder (-softdir) should contain 6 scripts (scripts 1-5 and MetClassWrapper.py) and 2 folders
(Conf_matrices and Weka_Models). Do not move any of these files/folders out of the MetClass folder.

Additionally, if you have several input files that you want to run MetClass on (the results of several
lipidomics experiments, for example), each file MUST BE IN ITS OWN FOLDER OR HAVE A UNIQUE NAME. If two 
input files are in the same location with the same name, the results for the first file will be lost 
when MetClass is run on the second file.

________INPUT FILE FORMAT:__________ 
Please have your input file be either .txt, .tab, or .csv
If your file is in .xlxs format, save it as one of the above formats within excel.

The input file should have one formula per line. Formulas should not contain any spaces or special characters.
Formulas lacking any C/H/O/N/P/S will be removed. Please do not have any headers at the top of the file or 
empty lines at the bottom.

Example formulas: 

C38H68O5
C22H46NO6P
C22H46NO6P
C59H96O6
C21H24O8
C79H140N4O36
C67H108O6

_________METCLASS FUNCTIONALITY:_________

MetClass uses pre-trained Weka machine learning models to classify users' lipidomics data. Given an input file 
of lipid molecular formulas, the software will extract features (using script 1), make a Weka Attribute Relation
File (with script 2), classify lipids into lipid Main Class using these features and pre-trained models, then 
repeat this process to classify lipids into Major Categories (which we refer to as Subclasses).

An example Main class is Glycerophospholipid. This is a broad lipid category. Example Major Categories of 
Glycerophospholipids include phosphatidyl inositols, glycerophosphoethanolamines, etc. These categories of 
lipids are more specific.

Script 1 removes formulas that do not have any C/H/O/N/P or S, and removes any elements either than 
C/H/O/N/P/S from all formulas. It also assigns a unique numerical ID to each formula. For example, formula "4" 
is the 4th formula on your input file.

Two of the required arguments for MetClass are main_t and sub_t. The options for both of these arguments are
"yes" and "no" (without the quotation marks). Choosing "yes" will impose a 90% confidence threshold on final
predictions for Main Class prediction (through main_t) and Major Category prediction (sub_t). 
For details on the thresholding procedure, please see MetClass' publication in the Journal of Cheminformatics.

_________OUTPUT FILES:_________

MetClass creates several output files and one folder of output files per input file/thresholds combination.
These files are for your reference.
The major, final output file has FinalMetClassOutput in the title, along with your input file's name, and 
threshold choices.

Within this final output file:
Each row corresponds to one lipid.
The output file will include the main class prediction, subclass prediction, main class precision, and subclass
precision for each lipid. Also included is the probabilities for prediction Weka outputs for each lipid,
corresponding to the % of trees in the Random Forest machine learning model that voted for a particular class. 

The precision for each lipid is calculated as follows:

1) Determine the prediction for that lipid,
2) Find the total number of lipids that were predicted as being that class in our machine learning
training process,
3) Determine the actual classes of lipids.

For example, if your Subclass_Precision cell reads: 
X2.Fatty_esters:21.31%, X12.Fatty_Acids_and_Conjugates:74.63%

This means that:
1) This lipid was classified as a "Fatty_Acids_and_Conjugates"
2) Of all the lipids classified as "Fatty_Acids_and_Conjugates" in our machine learning training process,
74.63% of these lipids were actually "Fatty_Acids_and_Conjugates", and 21.31% of these lipids were 
"Fatty_esters". 

The precision can give something of a confidence score for each lipid's classification. 

The thresholding process is based on each lipid's precision. Applying the main class precision threshold
will remove lipids falling into classes with lower than 90% precision.

_________NOTES FOR USAGE:_________

***Important note for the -wekap argument AND FOR PATHS WITH SPACES***

MetClass assumes that Weka downloaded in your C:/Program Files directory.

More specifically, it assumes that there is a space character in the path to your weka.jar file. If this 
IS NOT the case, open the MetClassWrapper.py file (if you do not have a Python IDE, you can open the file
with Notepad), and replace line 23 with:

wekap = os.path.abspath(argv_l[i + 1])

AND replace line 24 with: 

#wekap = os.path.abspath(wekap)

(In other words, put a # in front of line 24).

MAKE SURE THAT BOTH LINES ARE INDENTED WITH ONE TAB.

IF YOU HAVE A SPACE CHARACTER IN THE PATH FOR -softdir OR -infile:

For -softdir

Replace line 19 with:

softdir = ' '.join([argv_l[i + 1], argv_l[i + 2]])
softdir = os.path.abspath(softdir)

For -infile

Replace line 21 with: 

infil = ' '.join([argv_l[i + 1], argv_l[i + 2]])
infil = os.path.abspath(infil)

MAKE SURE THAT BOTH LINES ARE INDENTED WITH ONE TAB.