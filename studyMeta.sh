#!/bin/bash

cd /Volumes/encrypted/babybrains/dicom/MGH

studies=`ls -d */*`

for study in $studies; do echo $study ; done

firstSeries=$(for study in $studies; do echo ${study}/`ls ${study} | head -1` ; done)

for series in $firstSeries; do echo $series ; done

firstDCMs=$(for study in $studies; do find ${study} -name \*.dcm | head -1  ;  done)


for dcm in $firstDCMs; do echo $dcm ; done

for dcm in $firstDCMs; do dcmdump $dcm | grep -E 'PatientID|PatientAge|StudyDate' ; done | grep -v IssuerOfPatientID > studyMeta.dump


python << EOF | grep -v "missing" > studyMeta.txt

import json

fp = open('../../converted/studyMap.json')
studyMap = json.load(fp)

fp = open('../../converted/patientMap.json')
patientMap = json.load(fp)

studyMeta = {}

currentID = ''
fp = open('studyMeta.dump')

while True:
  try:
    studyDateLine = fp.readline()
    patientIDLine = fp.readline()
    patientAgeLine = fp.readline()

    studyDate = studyDateLine.split()[2].strip('[]')
    patientID = patientIDLine.split()[2].strip('[]')
    patientAge = patientAgeLine.split()[2].strip('[]')

    mappedID = patientMap[patientID]

    print(mappedID, patientAge, studyDate)
  except KeyError:
    print('missing %s' % patientID)
    continue
  except IndexError:
    print(studyDateLine)
    print(patientIDLine)
    print(patientAgeLine)
    break

  except:
    print ('-'*40)
    import traceback
    traceback.print_exc() # XXX But this goes to stderr!
    print ('-'*40)

EOF


