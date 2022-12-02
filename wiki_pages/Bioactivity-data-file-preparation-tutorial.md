### Overview

Metadata is an essential part of LC-MS/MS data, since it provides (biological) context about the analyzed sample, and helps with data interpretation. FERMO accepts two kinds of metadata: **metadata regarding sample grouping**, which is discussed in a [separate article](https://github.com/mmzdouc/FERMO/wiki/Metadata-file-preparation-tutorial), and **quantitative biological data**. Often, this is data from testing for biological activity, but is not limited to it. Attributing quantitative biological data to samples (and compounds) provides an additional data dimension for prioritization purposes and might have also implications for the commercialization of research.

### Metadata file preparation instructions

FERMO accepts and quantitative biological data (from here: quant_data data for short) in form of a .csv (comma-separated values)-file, which can be prepared using a spreadsheet program (e.g. Microsoft Excel, OpenOffice Calc). It requires the following format :

- A column with the title `sample_name` and the full names of the samples (including their endings)
- A column with the title `quant_data`, containing the measured activity of the sample (in numeric form).


There are many ways to measure quantitative biological data. Often, this is done with biological activity (bioactivity) testing. However, many of the measure either a concentration (e.g. EIC, MIC, IC50), or a percentage of inhibition. Usually, for concentration, a lower value signifies higher activity, while for percentage, a higher value signifies a higher activity. In FERMO, the kind of quantitative biological data (concentration-like or percentage-like) can be indicated on the processing page.

During processing, molecular features are examined if they may be associated to the quantitative biological data. If molecular features are only associated to "active" or "inactive" samples, they are or are not considered to be associated to the variable, respectively. Feature found in both "active" and "inactive" samples are treated separately. Assuming that the measured quantitative biological variable is concentration-dependent, the lowest intensity across "active" samples is compared to the highest intensity across "inactive" samples. If the fold-difference is above a user-specified QuantData factor, the feature is further considered to be putatively associated to bioactivity.

There are several limitations to consider: for one, it is based on the assumptions that the quantitative biological value is concentration-dependent, and that all samples were analyzed in an identical way (identical injection volumes of identical dilutions of samples). Next, the approach relies on a comparison between active and inactive samples. If no inactive samples were provided, no molecular feature could be excluded from consideration. If the samples are chemically very different from each other (i.e. little overlap between features), only a low number of molecular features could be excluded from consideration. These limitations should be taken into account before experimental design.

During processing, FERMO converts all numeric values greater than 0 to a range between 0.1 and 1. Samples with 0 as value are considered inactive. Therefore, the values can be set arbitrarily by the user, and do not have to be converted from another format. For example, for bioactivity expressed in percentage inhibition, one sample can have a bioactivity of 90 (percent), a second 40, and a third 8. Binary data (e.g. dead/alive, active/inactive) can be expressed as 1 (active) and 0 (inactive).

Example table: 
```
sample_name,quant_data
sample1.mzXML,100
sample2,100
sample3,100
sample4,80
```

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/bioactivity_table.png|alt=bioactivity_table.png]]

Despite the flexible input format, there are still some conditions that must be met:

- There must be only two columns, with the titles `sample_name` and `quant_data`
- Each sample must have a single measurement associated to it (no duplicate entries in column `sample_name`)
- The bioactivity values must be positive numeric values 

Common mistakes during bioactivity file preparation are:

- Instead of a comma `,`, some other delimiter (e.g. `tab`, `;`, `|`) was used in the .csv-file (can be checked by opening the file in a text editor (e.g. Notepad)
