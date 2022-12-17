### Overview

Metadata is an essential part of LC-MS/MS data. It provides (biological) context about the analyzed sample, and helps with data interpretation. This article discusses metadata regarding **quantitative biological data**. For metadata regarding sample grouping, see [this article](https://github.com/mmzdouc/FERMO/wiki/Metadata-file-preparation-tutorial).


### Metadata file preparation instructions

FERMO accepts and quantitative biological data (from here: quant_data for short) in form of a .csv (comma-separated values)-file, which can be prepared using a spreadsheet program (e.g. Microsoft Excel, OpenOffice Calc). It requires the following format :

- A column with the title `sample_name` and the full names of the samples (including their endings).
- A column with the title `quant_data`, containing the measured activity of the sample (in numeric form).

There are many ways to measure quantitative biological data. Often, this is done with biological activity (bioactivity) testing. However, many of the measure either a concentration (e.g. minimal inhibitory concentration), or a percentage of inhibition. Usually, for concentration, a lower value signifies higher activity, while for percentage, a higher value signifies a higher activity. In FERMO, the kind of quantitative biological data (concentration-like or percentage-like) can be indicated on the **processing page**.

Example table: 
```
sample_name,quant_data
sample1.mzXML,100
sample2,100
sample3,100
sample4,80
```

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/bioactivity_table.png|alt=bioactivity_table.png]]

Further, some conditions must be met:

- There must be only two columns, with the titles `sample_name` and `quant_data`.
- Each sample must have a single measurement associated to it (no duplicate entries in column `sample_name`).
- The bioactivity values must be positive numeric values. Rows with a quant_data value of 0 are ignored.

Common mistakes during bioactivity file preparation are:

- Instead of a comma `,`, some other delimiter (e.g. `tab`, `;`, `|`) was used in the .csv-file (can be checked by opening the file in a text editor (e.g. Notepad).
