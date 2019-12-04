#!/usr/bin/env python3

import os, sys, glob

def print_help():
	print('''
	Required Arguments:
	-softdir = Directory containing scripts and required files
	-infile = Input file of formulas -- one formula per line. Files will be
		written to the directory containing this file
	-wekap = Full path to the weka.jar file
	-main_t = Impose a threshold on main category classification? yes OR no
	-sub_t = Impose a threshold on sub-class classification? yes OR no
	''')
	
def parse_args(argv_l):
	for i in range(0, len(argv_l)):
		if argv_l[i] == '-softdir':
			sdir = os.path.abspath(argv_l[i + 1])
		elif argv_l[i] == '-infile':
			infil = os.path.abspath(argv_l[i + 1])
		elif argv_l[i] == '-wekap':
			wekap = ' '.join([argv_l[i + 1], argv_l[i + 2]])
			wekap = os.path.abspath(wekap)
		elif argv_l[i] == '-main_t':
			mt = argv_l[i + 1]
		elif argv_l[i] == '-sub_t':
			st = argv_l[i + 1]
	return sdir, infil, wekap, mt, st
	
	
def main():
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		sdir, infil, wekap, mt, st = parse_args(sys.argv)
	except:
		print_help()
		print("Error reading arguments, quitting!")
		sys.exit()
		
	indir = '/'.join(infil.split('\\')[:-1])
	innam = infil.split('\\')[-1][:-4]
	
	##launching first script. Taking input formula and making _augmented2.tab
	os.system(f'python {sdir}/1_FormulaProcessing.py {infil}')	
	print('Done with first script')
	
	##launching second script. Makes weka .arff file from the _augmented2.tab
	os.system(f'python {sdir}/2_MakeArff.py {infil}_augmented2.tab '\
			  'Fatty_Acyls,Glycerophospholipids,Sphingolipids,Polyketides,'\
			  'Saccharolipids,Glycerolipids,Sterol_Lipids,Prenol_Lipids')
	print('Done with second script')
	
	##launching weka, running main category model on new arff
	os.system(f'java -classpath \"{wekap}\" weka.classifiers.meta.FilteredClassifier'\
			  f' -T {infil}_augmented2.tab.challenge.multi.arff '\
			  f'-l {sdir}/Weka_models/main_classes_training.model -c last '\
			  f'-p 1 -distribution > {indir}/multiclass_output.pred')
	print('Done with weka main class')
	
	##making output directory first
	dir_par = indir + '/' + f'{innam}_parsed_MAIN_outputs_thresh{mt.upper()}_SUBthresh_{st.upper()}/'
	os.mkdir(f'{dir_par}/')
	
	##launching third script to parse weka's output
	os.system(f'Rscript {sdir}/3_ParseMainOut.R {indir}/multiclass_output.pred '\
			  f'{sdir}/Conf_matrices/Thresh{mt.upper()}/main.tab '\
			  f'{dir_par} {mt}')
	
	##now beginning subclass analysis
	
	##final output file
	#finalout = open(f'{indir}/FinalClassificationOutputMainThresh{mt.upper()}'\
	#				f'SubThresh{st.upper()}.tab','w')
	
	##dict of subclasses per class
	clsdict = {'1.Fatty_Acyls': 'Hydrocarbons,Fatty_esters,Oxygenated_hydrocarbons,'\
			'Fatty_acyl_glycosides,Other,Fatty_amides,Fatty_alcohols,Octadecanoids,'\
			'Fatty_aldehydes,Docosanoids,Eicosanoids,Fatty_Acids_and_Conjugates',
			'6.Glycerolipids': 'Triradylglycerols,Monoradylglycerols,Diradylglycerols,'\
			'Glycosyldiradylglycerols', '2.Glycerophospholipids': 'Glycerophosphates,'\
			'Glycerophosphoinositolglycans,Glycerophosphoethanolamines,'\
			'Glycerophosphoglycerophosphoglycerols,Glycerophosphoglycerols,'\
			'CDP-Glycerols,Other,Glycerophosphoinositols,Oxidized_glycerophospholipids,'\
			'Glycerophosphoserines,Glycerophosphocholines', '4.Polyketides':
			'Flavonoids,Other,Aromatic_polyketides,Macrolides_and_lactone_polyketides,'\
			'Polyether_antibiotics_', '8.Prenol_Lipids': 'Isoprenoids,Polyprenols,'\
			'Quinones_and_hydroquinones,Hopanoids', '5.Saccharolipids':
			'Other,Acyltrehaloses', '3.Sphingolipids': 'Acidic_glycosphingolipids,'\
			'Neutral_glycosphingolipids,Other,Ceramides,Phosphosphingolipids,'\
			'Sphingoid_bases', '7.Sterol_Lipids': 'Steroid_conjugates,Sterols,'\
			'Secosteroids,Bile_acids_and_derivatives,Steroids'}

	
	dir_pars = dir_par + '*'
	fils = glob.glob(dir_pars)
	for i in fils:
		name = '.'.join([i.split('.')[0][-1],i.split('.')[1]])
		print('Classifying subclasses for ' + name)
		fulli = os.path.abspath(i)
		
		##launching fourth script to make _augmented2.tab files from the outputs
		os.system(f'python {sdir}/4_MakeAugmentedSubclassFiles.py '\
				  f'{fulli} {infil}_augmented2.tab')
		
		##launching second script again to make new .arff files
		os.system(f'python {sdir}/2_MakeArff.py {fulli}_augmented2.tab '\
				  f'{clsdict[name]}')
		
		##launching weka
		os.system(f'java -classpath \"{wekap}\" weka.classifiers.meta.FilteredClassifier'\
				  f' -T {fulli}_augmented2.tab.challenge.multi.arff '\
				  f'-l {sdir}/Weka_models/{name}_training.model -c last '\
				  f'-p 1 -distribution > {dir_par}/{name}_output.pred')
		
	##Parsing final output files
	os.system(f'Rscript {sdir}/5_MakingFInalOutput.R {dir_par} '\
			  f'{sdir}/Conf_matrices/Thresh{st.upper()}/ '\
			  f'{indir} {mt} {st} {innam}')
		
	print('MetClass has completed!')	
	
if __name__ == "__main__":
	main()