### Overview

- "FERMO takes very long to process my files. Did it crash?"

For large peak tables, FERMO can calculate a long time, since all calculations are performed on the local computer. One way of checking if FERMO has crashed is to check the command line window that is opened when FERMO is started. The log messages can give an idea of which step is currently calculated. Depending on the calculation performance of the computer used, the size of the input data (number of molecular features in the peak table) and if molecular feature annotation is performed, the calculation can take some time. For a molecular feature table of 2000 molecular features, FERMO needs about 5 minutes to calculate the spectral similarity network, and another 120 minutes (4 second per molecular feature) for the annotation. This can be sped up by using a computer with higher performance, or by filtering out low-intensity molecular features using the **'Relative intensity filter'** on the [Processing page](https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page). If FERMO crashed unexpectedly, please feel free to open an issue on our Github page. 

- "I would like to have a certain functionality which is missing in FERMO. What should I do?"

FERMO is still under active development. If you are missing a particular functionality, please feel free to open an issue, make a pull request, or contact the authors. We are happy to receive feedback.

- "In the dashboard view, the spectral similarity/molecular network is not shown when I click on a molecular feature. Why?"

There are two reasons why a click on a molecular feature does not trigger the spectral similarity network. A short warning message is displayed, informing about the reasons, which are explained in more detail below.

First, the molecular feature might not have any associated MS² spectrum, either because there was none attributed during pre-processing, or because the MS² spectrum was filtered due to poor quality. By default, a MS² spectrum must have a minimum of 8 fragments to be considered appropriate. If you want to keep low-quality MS² spectra, set the **'Minimal required number of fragments per MS² spectrum'** filter on the [Processing page](https://github.com/mmzdouc/FERMO/wiki/Pages-Processing-page) to a lower value (e.g. 0).

Second, the molecular feature might be part of a very large spectral similarity/molecular network (>250 nodes). Due to performance limitations of the cytoscape.js plugin, rendering of such large networks is disabled. In any way, such networks are not very informative and can be better perceived by looking at the chromatogram view, which is always enabled.

