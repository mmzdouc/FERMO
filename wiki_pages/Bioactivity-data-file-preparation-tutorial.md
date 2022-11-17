### Overview

Metadata is an essential part of LC-MS/MS data, since it provides (biological) context about the analyzed sample, and helps with data interpretation. FERMO accepts two kinds of metadata: **metadata regarding sample grouping**, which is discussed in a [separate article](https://github.com/mmzdouc/FERMO/wiki/Metadata-file-preparation-tutorial), and **quantitative biological data**. This can be for example data from biological activity testing. Attributing quantitative biological data to samples (and compounds) provides an additional data dimension for prioritization purposes and might have also implications for the commercialization of research.

### Metadata file preparation instructions

FERMO accepts and quantitative biological data (from here: quant_data data for short) in form of a .csv (comma-separated values)-file, which can be prepared using a spreadsheet program (e.g. Microsoft Excel, OpenOffice Calc). It requires the following format :

- A column with the title `sample_name` and the full names of the samples (including their endings)
- A column with the title `quant_data`, containing the measured activity of the sample (in numeric form).


There are many ways to measure quantitative biological data. Often, this is done with biological activity (bioactivity) testing. However, many of them measure either a concentration (e.g. EIC, MIC, IC50), or a percentage of inhibition. Usually, for concentration, a lower value signifies higher activity, while for percentage, a higher value signifies a higher activity. In FERMO, the kind of bioactivity data (concentration or percentage) can be indicated on the processing page. Keep in mind that only samples for which bioactivity was detected should be contained in the bioactivity table. Samples with no (negative) bioactivity must be excluded, since all samples contained in the table will be considered bioactive, even if their value is 0.

During processing, FERMO converts all numeric values to a range between 0.1 and 1 (with 0 reserved for inactive samples), so users are completely free in how to include their bioactivity data. The bioactivity values in the bioactivity table can be set arbitrarily. For example, for bioactivity expressed in percentage inhibition, one sample can have a bioactivity of 90 (percent), a second 40, and a third 8. Bioactivity data without numeric output (e.g. dead/alive, active/inactive) can be expressed in a binary format, such that active or dead is set to 1 (remember to omit inactive samples from the bioactivity data file).
```
sample_name,quant_data
P-sphaerica-107188.mzXML,100
P-sphaerica-135062.mzXML,100
P-sphaerica-91431.mzXML,100
P-sphaerica-91781.mzXML,80
```

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/bioactivity_table.png|alt=bioactivity_table.png]]

Despite the flexible input format, there are still some conditions that must be met:

- There must be only two columns, with the titles `sample_name` and `quant_data`
- Each sample must have a single measurement associated to it (no duplicate entries in column `sample_name`)
- The bioactivity values must be positive numeric values 
- Only bioactive samples must be contained in table. If a sample showed no bioactivity (negative), exclude it from the table. 

Common mistakes during bioactivity file preparation are:

- Instead of a comma `,`, some other delimiter (e.g. `tab`, `;`, `|`) was used in the .csv-file (can be checked by opening the file in a text editor (e.g. Notepad)
