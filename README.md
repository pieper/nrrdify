
Warning: these scripts have not been widely tested and should only be used in research.

These scripts convert directories of DICOM data into nrrd files using [3D Slicer](http://slicer.org)'s
[DWIConvert](https://www.slicer.org/wiki/Documentation/Nightly/Modules/DWIConverter) utility.

* `convertall.py` - runs DWIConvert on all series folders in the hard coded directory structure
  * input is dicom directory (currently hard coded)
  * output is directory named "converted" with the same patient/study naming convention but with each study directory containing a series file as a .nrrd along with the output stdout and stderr of the converter command for diagnostic purposes.
  * a convert.log.txt at the top level of the converted directory is kept for overall diagnostics
  * *NOTE* outuput of this is still PHI

* `renameNRRDs.py` - removes patient ID
  * input is a directory output from `convertall.py`
  * output is a directory of the form: `converted-rename/patient-#####/patient-#####-study-#####/patient-#####-study-#####-series-##.nrrd (No identifiers, just images)
  * creates a patientMap.json that maps MRN to patient-#####  (contains PHI)
  * creates a studyMap.json that maps MRN and original study subdirectory name to study-#####  (contains PHI)

* `studyMeta.sh` creates tables of patient ID information
  * in the source data directory (hardcoded) creates the following:
    * `studyMeta.dump` with a line for StudyData,PatientID,PatientAge for each study (contains PHI)
    * `studyMeta.txt` with same data on one line (contains PHI)

Background: These scripts were developed to process dicom directories in the format exported from the [Partners mi2b2](https://www.nmr.mgh.harvard.edu/lab/mi2b2) system and would need to be customized for any other use.

Usage: These have been used on a mac, but probably also work unchanged on linux, but not on windows unless using a linux compatibility layer.

TODO: These script could be useful for other purposes and should be generalized at some point to handle different directory layouts and command line options.

Sponsored by: MI2B2 ENABLED PEDIATRIC RADIOLOGICAL DECISION SUPPORT, NIH grant R01EB014947
