###creates batch-file for MzMine3

#creates "standard workflow"
#gets list of files for processing (folder with  .mzXML files)
#gets parameters from user 
#gets location of mzmine from user -> not in this script; later

#create symbolic link to MzMine binary ?

#declare all the variables that have to be filled beforehand
#check if gotten from command line or if it needs to be requested 
#from user

#standard workflow
#1) import data
#2) mass detection MS1 and MS2
#3) chromatogram builder (ADAP)
#4) chromatogram deconvolution (baseline resolver)
#5) 13C isotope filter
#6) chromatogram aligner (join aligner)
#7) duplicate peak filter
#8) feature list row filter
#9) Export

#structure
#argparser
#command line input request user
#writing out batch.xml file



import argparse
import sys
import os

from batch_file.overwrite_test import overwrite_test



#####VARIABLES:

#set any defaults? Probably best

input_directory = ''
file_type = '' #mzML or mzXML or mzData etc?
output_directory = ''
output_file = 'mzmine3-batch-file.xml'
MS1_noise_level = ''
MS2_noise_level = ''
min_group_size = ''
group_int_threshold = ''
min_highest_int = ''
scan_to_scan_accuracy = ''
min_peak_height = ''
peak_duration_range = ''
baseline_level = ''




#####INPUT:

#Read into argparse

# ~ parser = argparse.ArgumentParser()
# ~ parser.add_argument("-i", "--input", help="reads input folder",
                    # ~ action=)
# ~ args = parser.parse_args()
# ~ print(args)

#####





#####OUTPUT:

#opens filehandle and checks for presence of file in folder
file_out = overwrite_test(output_file)

#writes output file.
print(
'''
<?xml version="1.0" encoding="UTF-8"?><batch>
    <batchstep method="io.github.mzmine.modules.io.import_rawdata_all.AllSpectralDataImportModule">
        <parameter name="File names">
''',
file=file_out)

#add files from input folder -> absolute paths










#split print into multiple statements to expand dict with filenames with for loop
#find way to append to file when writing to output




#'''The directory is {dir}  '''.format(dir = input_dir)
# ~ >>> d = { 'vars': "variables", 'example': "example" }
# ~ >>> s = "This is an {example} with {vars}"
# ~ >>> s.format(**d)

#print(''' ''', ''' ''') #possible

