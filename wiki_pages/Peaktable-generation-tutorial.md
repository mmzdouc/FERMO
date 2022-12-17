### Overview

For data processing, FERMO needs pre-processed LC-MS/MS data in form of a peak table. Below, you can find instructions on how to generate the peak table using MZmine3. Minimal instructions addressing experienced users are given in the paragraph **MZmine3 peak table export overview**. A thorough guide can be found in the section **MZmine3 step-by-step guide**.

### MZmine3 peak table export

Prepare the peak table by processing the LC-MS/MS data with MZmine3. Export the peak table via **'Feature list methods'** → **'Export feature list'** → **'GNPS - feature based molecular networking'**. Settings can be left default except for: **'Filter rows: ALL'**, **'Feature intensity: Peak height'**, **'CSV export: ALL'**. Save the files to a folder of your choice and run FERMO as indicated in the **Installation instructions** of the README.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/peaktable_export.png|alt=peaktable_export.png]]

If you do not know how to process your data with MZmine3, see below.

### MZmine3 step-by-step guide

**Disclaimer: the described workflow is an suggested example workflow for inexperienced users. The modules were chosen due to their simplicity and low number of user-defined parameters. More experienced users are welcome to change the modules as needed.**

1. **Download** and install the newest version of [MZmine3](http://mzmine.github.io/). 

2. (Optional) **convert** LC-MS/MS data into a format compatible with MZmine3, such as .mzXML or .mzML. An excellent tutorial on LC-MS/MS data conversion can be found in the [GNPS documentation](https://ccms-ucsd.github.io/GNPSDocumentation/fileconversion/). Data conversion can be done in different ways:
    - Use the **msConvert** program of the [**ProteoWizard* suite](https://proteowizard.sourceforge.io/). 
    - Use the [online conversion tool](https://gnps-quickstart.ucsd.edu/conversion) on the GNPS website. 

3. **Import** LC-MS/MS data into MZmine3 by going to **'Raw data methods'** → **'Raw data import'** and clicking on the import button respective to the data format at hand (e.g. **.mzML**).

4. **Detect** the MS1 signals contained in the data using the following step: **'Raw data methods'** → **'Mass detection'** → **'Mass detection'**, with default settings except: **'Raw data files: All raw data files'**, **'Scans: MS level 1'**; **'Mass detector: Centroid'**; **'Noise Level: see below'**. The noise level is data-specific and the easiest way to set this parameter sensibly is to check the data in the live preview and set the value so that the instrument noise is cut off (also called "cutting the grass"). 

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/mzmine3_ms1_detection.png|alt=mzmine3_ms1_detection.png]]

5. **Detect** the MS2 signals: **'Raw data methods'** → **'Mass detection'** → **'Mass detection'**, with default settings except for: **'Raw data files: All raw data files'**, **'Scans: MS level 2'**; **'Mass detector: Centroid'**; **'Noise Level: see below'**. Again, the noise level is best determined by looking at the raw data and 'cutting the grass'.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/mzmine3_ms2_detection.png|alt=mzmine3_ms2_detection.png]]

6. **Create** time/signal intensity curves (so-called extracted ion chromatograms): **'Feature detection'** → **'LC-MS'** → **'ADAP chromatogram builder'**, with default settings except **'Raw data files: All raw data files'**; **'Scans: MS level 1'**; **'Min group size in # of scans: see below'**; **'Group intensity threshold: see below'**; **'Min highest intensity : see below'**; **'Scan to scan accuracy: see below'**. The user-dependent parameters are intended to reduce the probability to pick up noise signals. For the parameter **'Min group size in # of scans'**, give the minimum number of consecutive scans a mass must appear in to be considered a trace, and should be reasonably high (e.g. 8). The parameter **'Group intensity threshold'** sets the minimum intensity of a signal to be considered member of a group. This parameter needs to be set by looking at any known compound in the chromatogram, and determining the minimum intensity at which the first scan related to this compound rises from the 'grass' (i.e. the noise). The parameter **'Min highest intensity'** sets the minimum intensity a mass needs to reach so that a new chromatogram is started. To determine this parameter, check which maximum intensity the instrument noise reaches, and set a value below that, taking into account a safety margin (e.g. if the instrument noise is around 1E1, you can set the parameter to 3E1). The parameter **'Scan to scan accuracy'** indicates the mass deviation that can be expected between scans. The mass deviation can be estimated by looking at consecutive scans of a known compound, and calculating the average mass deviation. 

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/mzmine3_chrom_building.png|alt=mzmine3_chrom_building.png]]

7. **Resolve** extracted ion chromatograms into individual peaks (split up): **'Feature detection'** → **'chromatogram resolving'** → **'Baseline resolver'**, with default settings except **'Feature lists: all feature lists'**, **'MS/MS scan pairing: ticked'**, **'Min peak height: see below'**; **'Peak duration range: see below'**; **'Baseline level: see below'**; **'Min # of data points: see below'**. The parameter **'Min peak height'** sets the minimal height/intensity a peak must reach to be considered signal and not noise, and has to be determined by looking at the data. A pragmatic way to do this is to take the average height of a number of low-intensity peaks with nice (gaussian) peak shapes. The parameter **'Peak duration range'** depends on the LC method and the column used, and can be estimated by looking at a peak corresponding to a known compound. The parameter **'Baseline level'** is the absolute cutoff below which all data points are deleted and on which a 'new' x-axis is drawn. The **'Min # of data points'** sets the minimum number of consecutive mass signals a peak is allowed to have. This needs to be a minimum of 3 (start, maximum, stop), but should ideally be higher, and needs to be assessed by looking at the number of scans in the peak of a known compound.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/mzmine3_baseline_cutoff.png|alt=mzmine3_baseline_cutoff.png]]

8. **Collapse** isotopic peaks resulting from the same molecule: **'Feature list methods'** → **'Isotopes'** → **'13C isotope filter'**, with default parameter settings except **'Feature lists: all feature lists'**, **'m/z tolerance: see below'**, **'Retention time tolerance:  see below'**. The **m/z tolerance** and the **retention time tolerance** can be set relatively strictly, since the values are coming from a single LC-MS/MS run and should be fairly uniform.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/mzmine3_13Cdeiso.png|alt=mzmine3_13Cdeiso.png]]

9. **Aligne** peaks across samples: **'Feature list methods'** → **'Alignment'** → **'Join aligner'**, with default parameter settings except **'m/z tolerance: see below'**; **'Weight for m/z: see below'**; **'Retention time tolerance: see below'**; **'Weight for RT: see below'**. For the parameters **'m/z tolerance'** and **'Retention time tolerance'**, the settings are dependent on how different the mass precision and the retention time variation of the individual samples are from each other. If they have been analyzed as part of the same batch, retention time drift and mass drift should be relatively similar. If samples were part of different batches, retention time drift and mass drift can lead to bigger differences, and therefore require larger tolerances. Similarly, for **'Weight for m/z'** and **'Weight for RT'** values should be adjusted dependent on aforementioned sample similarity. If no weight preference should be given, both values can be set to 50. 

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/mzmine3_join_aligner.png|alt=mzmine3_join_aligner.png]]

10. **Filter** the peak list: **'Feature list methods'** → **'Feature list filtering'**. The filters can be applied upon individual preferences, but we suggest to use **'Feature List Row Filter'** and set a filter on the retention time window, so that the solvent peak at the beginning of the instrument run is filtered out. Also, we suggest to remove the wash step at the end of the LC gradient. In this case, the field **'Never remove feature with MS2 scan'** must not be ticked.

11. **Export** the peak table for analysis with FERMO:  **'Feature list methods'** → **'Export feature list'** → **'GNPS - feature based molecular networking'** and default settings except for **'Filter rows: ALL'**, **'Feature intensity: Peak height'**, **'CSV export: ALL'**. Save the files to a folder of your choice.

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/peaktable_export.png|alt=peaktable_export.png]]

12. The peak table export leads to three files. Only two of them are used for the further analysis: the peak table, which is a file ending with **'_quant_full.csv'**, and the file containing the MS/MS data, ending with **'.mgf'**. The third file, which ends in '_quant.csv', only contains limited information and is not used further. If the file ending in **'_quant_full.csv'** is missing, verify if the file export in MZmine3 was performed with the setting **'CSV export: ALL'**.
