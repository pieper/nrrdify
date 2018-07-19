import os
import subprocess

# to get age ranges:
'''
http://localhost:5984/ch-babies/_design/tags/_view/byTagAndValue?reduce=true&group_level=2&stale=update_after&start_key=[%2200101010%22,%22%22]&end_key=[%2200101010%22,%22Z%22]&_nonce=1509220142419
'''

dwiConvertPath = '/Applications/Slicer-4.6.2.app/Contents/lib/Slicer-4.6/cli-modules/DWIConvert'
sourceDirectory = '/Volumes/encrypted/babybrains/dicom' 
targetDirectory = '/Volumes/encrypted/babybrains/converted'

def convert(subdirectory):
    lsProcess = subprocess.Popen(['ls', os.path.join(subdirectory)], stdout=subprocess.PIPE)
    hasDICOM = False
    for line in lsProcess.stdout.readlines():
      if line.strip().endswith('.dcm'):
        hasDICOM = True
        break
    if hasDICOM:
      patient = subdirectory.split('/')[-3]
      study = subdirectory.split('/')[-2]
      series = subdirectory.split('/')[-1]
      print(patient, study, series)

      outputPath = os.path.join(targetDirectory, patient, study)
      if not os.path.exists(outputPath):
        os.makedirs(outputPath)
      nrrdPath = os.path.join(outputPath, series+".nrrd")
      outFP = open(os.path.join(outputPath, series+".stdout.txt"), 'w')
      errFP = open(os.path.join(outputPath, series+".stderr.txt"), 'w')

      dwiConvertProcess = subprocess.Popen([dwiConvertPath, 
                                            '-i', subdirectory,
                                            '-o', nrrdPath], 
                                            stdout=outFP, stderr=errFP)
      dwiConvertProcess.wait()
      outFP.close()
      errFP.close()
      print('converted to ' + outputPath)

findProcess = subprocess.Popen(['find', sourceDirectory, '-type', 'd'], stdout=subprocess.PIPE)
while True:
  try:
    subdirectory = findProcess.stdout.readline().strip()
    if subdirectory == "":
      break
    print(subdirectory)
    convert(subdirectory)
  except:
      print ('-'*40)
      import traceback
      traceback.print_exc() # XXX But this goes to stderr!
      print ('-'*40)
