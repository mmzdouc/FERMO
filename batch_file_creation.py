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

input_directory = '/home/mitz/aWageningen/MZWUR2/datasets/PLMbyt/input/' #change later to './input' 
output_directory = '.'
output_file = 'mzmine3-batch-file.xml'
MS1_noise_level = 1000.0
MS2_noise_level = 20.0
min_group_size = 8
group_int_threshold = 500.0
min_highest_int = 1000.0
scan_to_scan_accuracy_ppm = 20.0 #ppm
min_peak_height = 1000.0
peak_duration_range_min = 0.2
peak_duration_range_max = 1.0
baseline_level = 250.0




#####INPUT:

#limit command line usage: not too much time since it is going to 
#be a gui tool anyway
#Read into argparse

# ~ parser = argparse.ArgumentParser()
# ~ parser.add_argument("-i", "--input", help="reads input folder",
                    # ~ action=)
# ~ args = parser.parse_args()
# ~ print(args)

#####
#Take care: input() returns string by default


print(
"""
Hi! This script can be used to set up a MzMine3 batch processing file,
which is needed to run MzMine3 in command line/batch mode.
It contains the steps that will be executed, as well as the parameters
that are needed to run the modules. 

For convenience, default parameters have been set.
For each parameter, you will be asked for a new value.
By pressing enter, the default value is kept. 

This script does not check for the right input yet, so please be careful
what you type. Wrong values will prevent MzMine from running.

The default workflow currently consists of:
1) import data
2) mass detection MS1 and MS2
3) chromatogram builder (ADAP)
4) chromatogram deconvolution (baseline resolver)
5) 13C isotope filter
6) chromatogram aligner (join aligner)
7) duplicate peak filter
8) feature list row filter
9) Export

In the future, a more fine-grained selection of the workflow might be 
available.
"""
)





#####OUTPUT:

#checks for presence of file in folder
output_file = overwrite_test(output_file)

#rewrite as with ... as to make writing out safer
file_out = open(output_file, 'w')
print(
'''<?xml version="1.0" encoding="UTF-8"?><batch>
    <batchstep method="io.github.mzmine.modules.io.import_rawdata_all.AllSpectralDataImportModule">
        <parameter name="File names">''', 
file=file_out)

#open file again so that it can be written in append mode
file_out = open(output_file, 'a')
###get file listing
for i in os.listdir(input_directory):
    print(f"            <file>{os.path.join(input_directory, i)}</file>",file=file_out)

#attention: f-fstrings
print(
f'''        </parameter>
        <parameter name="Advanced import" selected="true">
            <parameter name="MS1 detector (Advanced)" selected="false" selected_item="Centroid">
                <module name="Centroid">
                    <parameter name="Noise level">100.0</parameter>
                    <parameter name="Detect isotope signals below noise level" selected="false">
                        <parameter name="Chemical elements">H,C,N,O,S</parameter>
                        <parameter name="m/z tolerance">
                            <absolutetolerance>5.0E-4</absolutetolerance>
                            <ppmtolerance>10.0</ppmtolerance>
                        </parameter>
                        <parameter name="Maximum charge of isotope m/z">1</parameter>
                    </parameter>
                </module>
                <module name="Exact mass">
                    <parameter name="Noise level"/>
                    <parameter name="Detect isotope signals below noise level" selected="false">
                        <parameter name="Chemical elements">H,C,N,O,S</parameter>
                        <parameter name="m/z tolerance">
                            <absolutetolerance>5.0E-4</absolutetolerance>
                            <ppmtolerance>10.0</ppmtolerance>
                        </parameter>
                        <parameter name="Maximum charge of isotope m/z">1</parameter>
                    </parameter>
                </module>
                <module name="Local maxima">
                    <parameter name="Noise level"/>
                </module>
                <module name="Recursive threshold">
                    <parameter name="Noise level"/>
                    <parameter name="Min m/z peak width"/>
                    <parameter name="Max m/z peak width"/>
                </module>
                <module name="Wavelet transform">
                    <parameter name="Noise level"/>
                    <parameter name="Scale level"/>
                    <parameter name="Wavelet window size (%)"/>
                </module>
                <module name="Auto">
                    <parameter name="Noise level">1000.0</parameter>
                    <parameter name="Detect isotope signals below noise level" selected="false">
                        <parameter name="Chemical elements">H,C,N,O,S</parameter>
                        <parameter name="m/z tolerance">
                            <absolutetolerance>5.0E-4</absolutetolerance>
                            <ppmtolerance>10.0</ppmtolerance>
                        </parameter>
                        <parameter name="Maximum charge of isotope m/z">1</parameter>
                    </parameter>
                </module>
            </parameter>
            <parameter name="MS2 detector (Advanced)" selected="false" selected_item="Centroid">
                <module name="Centroid">
                    <parameter name="Noise level">100.0</parameter>
                    <parameter name="Detect isotope signals below noise level" selected="false">
                        <parameter name="Chemical elements">H,C,N,O,S</parameter>
                        <parameter name="m/z tolerance">
                            <absolutetolerance>5.0E-4</absolutetolerance>
                            <ppmtolerance>10.0</ppmtolerance>
                        </parameter>
                        <parameter name="Maximum charge of isotope m/z">1</parameter>
                    </parameter>
                </module>
                <module name="Exact mass">
                    <parameter name="Noise level"/>
                    <parameter name="Detect isotope signals below noise level" selected="false">
                        <parameter name="Chemical elements">H,C,N,O,S</parameter>
                        <parameter name="m/z tolerance">
                            <absolutetolerance>5.0E-4</absolutetolerance>
                            <ppmtolerance>10.0</ppmtolerance>
                        </parameter>
                        <parameter name="Maximum charge of isotope m/z">1</parameter>
                    </parameter>
                </module>
                <module name="Local maxima">
                    <parameter name="Noise level"/>
                </module>
                <module name="Recursive threshold">
                    <parameter name="Noise level"/>
                    <parameter name="Min m/z peak width"/>
                    <parameter name="Max m/z peak width"/>
                </module>
                <module name="Wavelet transform">
                    <parameter name="Noise level"/>
                    <parameter name="Scale level"/>
                    <parameter name="Wavelet window size (%)"/>
                </module>
                <module name="Auto">
                    <parameter name="Noise level">1000.0</parameter>
                    <parameter name="Detect isotope signals below noise level" selected="false">
                        <parameter name="Chemical elements">H,C,N,O,S</parameter>
                        <parameter name="m/z tolerance">
                            <absolutetolerance>5.0E-4</absolutetolerance>
                            <ppmtolerance>10.0</ppmtolerance>
                        </parameter>
                        <parameter name="Maximum charge of isotope m/z">1</parameter>
                    </parameter>
                </module>
            </parameter>
        </parameter>
        <parameter name="Spectral library files"/>
    </batchstep>
    <batchstep method="io.github.mzmine.modules.dataprocessing.featdet_massdetection.MassDetectionModule">
        <parameter name="Raw data files" type="BATCH_LAST_FILES"/>
        <parameter name="Scans">
            <ms_level>1</ms_level>
            <scan_definition/>
        </parameter>
        <parameter name="Scan types (IMS)">All scan types</parameter>
        <parameter name="Mass detector" selected_item="Centroid">
            <module name="Centroid">
                <parameter name="Noise level">{MS1_noise_level}</parameter>
                <parameter name="Detect isotope signals below noise level" selected="false">
                    <parameter name="Chemical elements">H,C,N,O,S</parameter>
                    <parameter name="m/z tolerance">
                        <absolutetolerance>5.0E-4</absolutetolerance>
                        <ppmtolerance>10.0</ppmtolerance>
                    </parameter>
                    <parameter name="Maximum charge of isotope m/z">1</parameter>
                </parameter>
            </module>
            <module name="Exact mass">
                <parameter name="Noise level"/>
                <parameter name="Detect isotope signals below noise level" selected="false">
                    <parameter name="Chemical elements">H,C,N,O,S</parameter>
                    <parameter name="m/z tolerance">
                        <absolutetolerance>5.0E-4</absolutetolerance>
                        <ppmtolerance>10.0</ppmtolerance>
                    </parameter>
                    <parameter name="Maximum charge of isotope m/z">1</parameter>
                </parameter>
            </module>
            <module name="Local maxima">
                <parameter name="Noise level"/>
            </module>
            <module name="Recursive threshold">
                <parameter name="Noise level"/>
                <parameter name="Min m/z peak width"/>
                <parameter name="Max m/z peak width"/>
            </module>
            <module name="Wavelet transform">
                <parameter name="Noise level"/>
                <parameter name="Scale level"/>
                <parameter name="Wavelet window size (%)"/>
            </module>
            <module name="Auto">
                <parameter name="Noise level">1000.0</parameter>
                <parameter name="Detect isotope signals below noise level" selected="false">
                    <parameter name="Chemical elements">H,C,N,O,S</parameter>
                    <parameter name="m/z tolerance">
                        <absolutetolerance>5.0E-4</absolutetolerance>
                        <ppmtolerance>10.0</ppmtolerance>
                    </parameter>
                    <parameter name="Maximum charge of isotope m/z">1</parameter>
                </parameter>
            </module>
        </parameter>
        <parameter name="Output netCDF filename (optional)" selected="false"/>
    </batchstep>
    <batchstep method="io.github.mzmine.modules.dataprocessing.featdet_massdetection.MassDetectionModule">
        <parameter name="Raw data files" type="BATCH_LAST_FILES"/>
        <parameter name="Scans">
            <ms_level>2</ms_level>
            <scan_definition/>
        </parameter>
        <parameter name="Scan types (IMS)">All scan types</parameter>
        <parameter name="Mass detector" selected_item="Centroid">
            <module name="Centroid">
                <parameter name="Noise level">{MS2_noise_level}</parameter>
                <parameter name="Detect isotope signals below noise level" selected="false">
                    <parameter name="Chemical elements">H,C,N,O,S</parameter>
                    <parameter name="m/z tolerance">
                        <absolutetolerance>5.0E-4</absolutetolerance>
                        <ppmtolerance>10.0</ppmtolerance>
                    </parameter>
                    <parameter name="Maximum charge of isotope m/z">1</parameter>
                </parameter>
            </module>
            <module name="Exact mass">
                <parameter name="Noise level"/>
                <parameter name="Detect isotope signals below noise level" selected="false">
                    <parameter name="Chemical elements">H,C,N,O,S</parameter>
                    <parameter name="m/z tolerance">
                        <absolutetolerance>5.0E-4</absolutetolerance>
                        <ppmtolerance>10.0</ppmtolerance>
                    </parameter>
                    <parameter name="Maximum charge of isotope m/z">1</parameter>
                </parameter>
            </module>
            <module name="Local maxima">
                <parameter name="Noise level"/>
            </module>
            <module name="Recursive threshold">
                <parameter name="Noise level"/>
                <parameter name="Min m/z peak width"/>
                <parameter name="Max m/z peak width"/>
            </module>
            <module name="Wavelet transform">
                <parameter name="Noise level"/>
                <parameter name="Scale level"/>
                <parameter name="Wavelet window size (%)"/>
            </module>
            <module name="Auto">
                <parameter name="Noise level">1000.0</parameter>
                <parameter name="Detect isotope signals below noise level" selected="false">
                    <parameter name="Chemical elements">H,C,N,O,S</parameter>
                    <parameter name="m/z tolerance">
                        <absolutetolerance>5.0E-4</absolutetolerance>
                        <ppmtolerance>10.0</ppmtolerance>
                    </parameter>
                    <parameter name="Maximum charge of isotope m/z">1</parameter>
                </parameter>
            </module>
        </parameter>
        <parameter name="Output netCDF filename (optional)" selected="false"/>
    </batchstep>
    <batchstep method="io.github.mzmine.modules.dataprocessing.featdet_adapchromatogrambuilder.ModularADAPChromatogramBuilderModule">
        <parameter name="Raw data files" type="BATCH_LAST_FILES"/>
        <parameter name="Scans">
            <ms_level>1</ms_level>
        </parameter>
        <parameter name="Min group size in # of scans">{min_group_size}</parameter>
        <parameter name="Group intensity threshold">{group_int_threshold}</parameter>
        <parameter name="Min highest intensity">{min_highest_int}</parameter>
        <parameter name="Scan to scan accuracy (m/z)">
            <absolutetolerance>0.0</absolutetolerance>
            <ppmtolerance>{scan_to_scan_accuracy_ppm}</ppmtolerance>
        </parameter>
        <parameter name="Suffix">chromatograms</parameter>
        <parameter name="Allow single scan chromatograms"/>
    </batchstep>
    <batchstep method="io.github.mzmine.modules.dataprocessing.featdet_chromatogramdeconvolution.baseline.BaselineFeatureResolverModule">
        <parameter name="Feature lists" type="BATCH_LAST_FEATURELISTS"/>
        <parameter name="Suffix">resolved</parameter>
        <parameter name="Original feature list">KEEP</parameter>
        <parameter name="MS/MS scan pairing" selected="false">
            <parameter name="Retention time tolerance" unit="MINUTES">0.2</parameter>
            <parameter name="MS1 to MS2 precursor tolerance (m/z)">
                <absolutetolerance>0.01</absolutetolerance>
                <ppmtolerance>10.0</ppmtolerance>
            </parameter>
            <parameter name="Limit by RT edges">false</parameter>
            <parameter name="Combine MS/MS spectra (TIMS)">false</parameter>
            <parameter name="Lock to feature mobility range">false</parameter>
            <parameter name="Minimum merged intensity (IMS)" selected="false">250.0</parameter>
        </parameter>
        <parameter name="Min peak height">{min_peak_height}</parameter>
        <parameter name="Peak duration range (min)">
            <min>{peak_duration_range_min}</min>
            <max>{peak_duration_range_max}</max>
        </parameter>
        <parameter name="Baseline level">{baseline_level}</parameter>
    </batchstep>
    <batchstep method="io.github.mzmine.modules.dataprocessing.filter_isotopegrouper.IsotopeGrouperModule">
        <parameter name="Feature lists" type="BATCH_LAST_FEATURELISTS"/>
        <parameter name="Name suffix">deisotoped</parameter>
        <parameter name="m/z tolerance">
            <absolutetolerance>0.0</absolutetolerance>
            <ppmtolerance>{scan_to_scan_accuracy_ppm}</ppmtolerance>
        </parameter>
        <parameter name="Retention time tolerance" unit="MINUTES">0.2</parameter>
        <parameter name="Mobility tolerance" selected="false"/>
        <parameter name="Monotonic shape">false</parameter>
        <parameter name="Maximum charge">2</parameter>
        <parameter name="Representative isotope">Most intense</parameter>
        <parameter name="Never remove feature with MS2">true</parameter>
        <parameter name="Original feature list">KEEP</parameter>
    </batchstep>
    <batchstep method="io.github.mzmine.modules.dataprocessing.align_join.JoinAlignerModule">
        <parameter name="Feature lists" type="BATCH_LAST_FEATURELISTS"/>
        <parameter name="Feature list name">Aligned feature list</parameter>
        <parameter name="m/z tolerance">
            <absolutetolerance>0.0</absolutetolerance>
            <ppmtolerance>20.0</ppmtolerance>
        </parameter>
        <parameter name="Weight for m/z">60.0</parameter>
        <parameter name="Retention time tolerance" unit="MINUTES">0.7</parameter>
        <parameter name="Weight for RT">40.0</parameter>
        <parameter name="Mobility tolerance" selected="false"/>
        <parameter name="Mobility weight">1.0</parameter>
        <parameter name="Require same charge state">false</parameter>
        <parameter name="Require same ID">false</parameter>
        <parameter name="Compare isotope pattern" selected="false">
            <parameter name="Isotope m/z tolerance">
                <absolutetolerance>0.001</absolutetolerance>
                <ppmtolerance>5.0</ppmtolerance>
            </parameter>
            <parameter name="Minimum absolute intensity"/>
            <parameter name="Minimum score"/>
        </parameter>
        <parameter name="Compare spectra similarity" selected="false">
            <parameter name="Spectral m/z tolerance">
                <absolutetolerance>0.001</absolutetolerance>
                <ppmtolerance>10.0</ppmtolerance>
            </parameter>
            <parameter name="MS level">2</parameter>
            <parameter name="Compare spectra similarity" selected_item="Weighted dot-product cosine">
                <module name="Weighted dot-product cosine">
                    <parameter name="Weights">MassBank (mz^2 * I^0.5)</parameter>
                    <parameter name="Minimum  cos similarity">0.7</parameter>
                    <parameter name="Handle unmatched signals">KEEP ALL AND MATCH TO ZERO</parameter>
                </module>
                <module name="Composite dot -product identity (similar to NIST search)">
                    <parameter name="Weights">MassBank (mz^2 * I^0.5)</parameter>
                    <parameter name="Minimum  cos similarity">0.7</parameter>
                    <parameter name="Handle unmatched signals">KEEP ALL AND MATCH TO ZERO</parameter>
                </module>
            </parameter>
        </parameter>
        <parameter name="Original feature list">KEEP</parameter>
    </batchstep>
    <batchstep method="io.github.mzmine.modules.dataprocessing.filter_duplicatefilter.DuplicateFilterModule">
        <parameter name="Feature lists" type="BATCH_LAST_FEATURELISTS"/>
        <parameter name="Name suffix">filtered</parameter>
        <parameter name="Filter mode">NEW AVERAGE</parameter>
        <parameter name="m/z tolerance">
            <absolutetolerance>0.02</absolutetolerance>
            <ppmtolerance>0.0</ppmtolerance>
        </parameter>
        <parameter name="RT tolerance" unit="MINUTES">0.4</parameter>
        <parameter name="Require same identification">false</parameter>
        <parameter name="Original feature list">KEEP</parameter>
    </batchstep>
    <batchstep method="io.github.mzmine.modules.dataprocessing.filter_rowsfilter.RowsFilterModule">
        <parameter name="Feature lists" type="BATCH_LAST_FEATURELISTS"/>
        <parameter name="Name suffix">filteredrtmz</parameter>
        <parameter name="Minimum features in a row (abs or %)" selected="false">0.1</parameter>
        <parameter name="Minimum features in an isotope pattern" selected="false">2</parameter>
        <parameter name="Validate 13C isotope pattern" selected="false">
            <parameter name="m/z tolerance">
                <absolutetolerance>5.0E-4</absolutetolerance>
                <ppmtolerance>10.0</ppmtolerance>
            </parameter>
            <parameter name="Max charge">1</parameter>
            <parameter name="Estimate minimum carbon">true</parameter>
            <parameter name="Remove if 13C">true</parameter>
            <parameter name="Exclude isotopes">H,C,N,O,S</parameter>
        </parameter>
        <parameter name="m/z" selected="true">
            <min>300.0</min>
            <max>3000.0</max>
        </parameter>
        <parameter name="Retention time" selected="true">
            <min>2.0</min>
            <max>20.0</max>
        </parameter>
        <parameter name="features duration range" selected="false">
            <min>0.0</min>
            <max>10.0</max>
        </parameter>
        <parameter name="Chromatographic FWHM" selected="false">
            <min>0.0</min>
            <max>1.0</max>
        </parameter>
        <parameter name="Charge" selected="false">
            <min>1</min>
            <max>2</max>
        </parameter>
        <parameter name="Kendrick mass defect" selected="false">
            <parameter name="Kendrick mass defect">
                <min>0.0</min>
                <max>1.0</max>
            </parameter>
            <parameter name="Kendrick mass base"/>
            <parameter name="Shift">0.0</parameter>
            <parameter name="Charge">1</parameter>
            <parameter name="Divisor">1</parameter>
            <parameter name="Use Remainder of Kendrick mass">false</parameter>
        </parameter>
        <parameter name="Parameter">No parameters defined</parameter>
        <parameter name="Only identified?">false</parameter>
        <parameter name="Text in identity" selected="false"/>
        <parameter name="Text in comment" selected="false"/>
        <parameter name="Keep or remove rows">Keep rows that match all criteria</parameter>
        <parameter name="Feature with MS2 scan">true</parameter>
        <parameter name="Never remove feature with MS2">false</parameter>
        <parameter name="Reset the feature number ID">false</parameter>
        <parameter name="Mass defect" selected="false"/>
        <parameter name="Original feature list">KEEP</parameter>
    </batchstep>
    <batchstep method="io.github.mzmine.modules.io.export_features_gnps.fbmn.GnpsFbmnExportAndSubmitModule">
        <parameter name="Feature lists" type="BATCH_LAST_FEATURELISTS"/>
        <parameter name="Filename">
            <current_file>/home/mitz/Desktop/BytAll-csv_expgnpsall.csv</current_file>
            <last_file>/home/mitz/Desktop/BytAll-csv_expgnpsall.csv</last_file>
        </parameter>
        <parameter name="Merge MS/MS (experimental)" selected="false">
            <parameter name="Select spectra to merge">across samples</parameter>
            <parameter name="m/z merge mode">weighted average (remove outliers)</parameter>
            <parameter name="intensity merge mode">sum intensities</parameter>
            <parameter name="Expected mass deviation"/>
            <parameter name="Cosine threshold (%)">0.7</parameter>
            <parameter name="Signal count threshold (%)">0.2</parameter>
            <parameter name="Isolation window offset (m/z)">0.0</parameter>
            <parameter name="Isolation window width (m/z)">3.0</parameter>
        </parameter>
        <parameter name="Filter rows">ONLY WITH MS2</parameter>
        <parameter name="Feature intensity">Peak height</parameter>
        <parameter name="CSV export">ALL</parameter>
        <parameter name="Submit to GNPS" selected="false">
            <parameter name="Meta data file" selected="false"/>
            <parameter name="Export ion identity networks">true</parameter>
            <parameter name="Presets">HIGHRES</parameter>
            <parameter name="Job title"/>
            <parameter name="Email"/>
            <parameter name="Username"/>
            <parameter name="Password"/>
            <parameter name="Open website">true</parameter>
        </parameter>
        <parameter name="Open folder">false</parameter>
    </batchstep>
</batch>''', 
file=file_out)




file_out.close()


#split print into multiple statements to expand dict with filenames with for loop
#find way to append to file when writing to output


#chosen format: f-strings


#works
#'''The directory is {keyword}  '''.format(keyword=value)




#'''The directory is {dir}  '''.format(dir = input_dir)
# ~ >>> d = { 'vars': "variables", 'example': "example" }
# ~ >>> s = "This is an {example} with {vars}"
# ~ >>> s.format(**d)

#print(''' ''', ''' ''') #possible

