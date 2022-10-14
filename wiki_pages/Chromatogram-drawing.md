### Overview

This Wiki page describes the ratio behind the (pseudo)chromatogram drawing in FERMO.

### Chromatogram drawing

In mass spectrometry, a *m/z* chromatogram peak represents a specific *m/z* that has been detected across a number of consecutive scans. Therefore, it is an continuous trace, with each data point having a specific retention time and intensity. Peak picking algorithms transform these continuous traces into discrete parameters such as retention time at the start/stop of the peak, feature width at half maximum intensity, or retention time at maximum intensity. This form of representation is more memory-efficient then the continuous one and generally justifies the loss in information about the original chromatogram trace. 

In FERMO, the chromatograms peaks are drawn only from the discrete parameters mentioned above, since the peaktable used as input does not contain continuous chromatogram traces. Therefore, FERMO actually draws pseudo-chromatograms. Manual inspection showed that pseudo-chromatograms are good representations of the original chromatograms. Still, they remain abstractions of the original data, and users are advised to inspect the original chromatograms before important decision-making (e.g. before prioritization). 

Pseudo-chromatograms are drawn using following data points (x/y, where x is the retention time (rt), and y is the relative intensity (int):
- `rt at start of peak/0*int`
- `rt at start of feature width at half maximum/0.5*int`
- `rt at maximum int/int`
- `rt at stop of feature width at half maximum/0.5*int`
- `rt at stop of peak/0*int`
    
This form of representation comes with certain limitations: 

- Shoulder peaks arising from co-eluting isomers are not considered due to the lack of information about them 
- Asymmetry and tailing factors are not utilized since they are not present for all peaks in the MZmine3 peaktable.

Despite these limitations, we consider the use of pseudo-chromatograms a computationally efficient way of peak representation, with sufficient accuracy. 
