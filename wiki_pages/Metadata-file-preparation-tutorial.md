### Overview

Metadata is an essential part of LC-MS/MS data, since it provides (biological) context about the analyzed sample, and helps with data interpretation. FERMO accepts two kinds of metadata: **metadata regarding biological activity** which is discussed in a [separate article](https://github.com/mmzdouc/FERMO/wiki/Bioactivity-data-file-preparation-tutorial), and metadata regarding **sample grouping**. The grouping of samples helps with data organization, result interpretation, and the differentiation of blank-associated signals. FERMO allows arbitrary grouping, with no limitation on how many groups are defined.

### Metadata file preparation instructions

FERMO accepts group metadata (from here: metadata for short) in form of a .csv (comma-separated values) file, which can be prepared using a spreadsheet program (e.g. Microsoft Excel, OpenOffice Calc). It requires the following format :

- A column with the title `sample_name` and the full names of the samples (including their endings)
- A column with the title `attribute`, containing the group lable the sample belongs to

```
sample_name,attribute
sample1.mzXML,BLANK
sample2.mzXML,A2
sample3.mzXML,C
sample4.mzXML,S
sample5.mzXML,A2
sample6.mzXML,S
sample7.mzXML,V2
sample8.mzXML,C
sample9.mzXML,C
sample10.mzXML,S
sample11.mzXML,S
```

[[https://github.com/mmzdouc/FERMO/blob/main/wiki_assets/metadata_table.png|alt=metadata_table.png]]

The group names can be chosen arbitrarily, with two exceptions: first, the label `BLANK` (in capital letters) must only be used to denominate sample/instrument/medium/solvent blanks, since molecular features detected in blanks will be treated differently from other molecular features. Second, the label `GENERAL` (in capital letters) is reserved to group samples without any grouping information, and must not be used by the user. 

Additionally, the following conditions must be met:

- There must be only two columns, with the titles `sample_name` and `attribute`
- Each sample must be associated to a single group

Furthermore, there are some suggestions:

-We advise the following naming convention for group names: single words made up by lowercase letters (a-z) and digits (0-9), without any whitespace, punctuation, or special characters (except for the underscore symbol '_'. Good group names would be for example `group_1`, `group_2`, or `marine`, `terrestrial`, or `treatment`, `control`. Bad group names would be for example `45%-78%`, `+#.-.`, `XxXxxXx`, or `*`.
- Group names are case-sensitive, meaning that `group1`, `Group1` and `GROUP1` would be interpreted as three different groups by the program. 
- While there is no limit on the number of different groups used, it is suggested to keep this number low, to make it easier to detect differences between groups. 
- The nesting of groups is not supported. 

Common mistakes during metadata file preparation are:

- The metadata file format was mistaken with the one used in GNPS molecular networking
- Instead of a comma `,`, some other delimiter (e.g. `tab`, `;`, `|`) was used in the .csv-file (can be checked by opening the file in a text editor (e.g. Notepad)
