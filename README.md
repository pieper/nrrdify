
These scripts convert directories of DICOM data into nrrd files using 3D Slicer's
DWIConvert utility.

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
