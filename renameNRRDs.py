import json
import os
import shutil
import subprocess

sourceDirectory = '/Volumes/encrypted/babybrains/converted'
targetDirectory = '/Volumes/encrypted/babybrains/converted-renamed'

patientMap = {}
studyMap = {}
seriesMap = {}

def rename(subdirectory):
    lsProcess = subprocess.Popen(['ls', os.path.join(subdirectory)], stdout=subprocess.PIPE)
    nrrds = []
    for line in lsProcess.stdout.readlines():
      if line.strip().endswith('.nrrd'):
        nrrds.append(line.strip())
    for nrrd in nrrds:
      patient = subdirectory.split('/')[-2]
      study = subdirectory.split('/')[-1]

      if not patient in patientMap:
        patientMap[patient] = 'patient-%05d' % len(patientMap.keys())
        studyMap[patient] = {}
      if not study in studyMap[patient]:
        studyMap[patient][study] = 'study-%05d' % len(studyMap[patient].keys())

      outputPath = os.path.join(targetDirectory, patientMap[patient], studyMap[patient][study])
      if not os.path.exists(outputPath):
        os.makedirs(outputPath)
      nrrdPath = os.path.join(outputPath, patientMap[patient] + "_" + studyMap[patient][study] + "_" + "series-" + str(nrrds.index(nrrd)) + ".nrrd")

      print('-- copy --')
      oldPath = os.path.join(subdirectory, nrrd)
      print(oldPath)
      print(nrrdPath)
      shutil.copyfile(oldPath, nrrdPath)


findProcess = subprocess.Popen(['find', sourceDirectory, '-type', 'd'], stdout=subprocess.PIPE)
while True:
  try:
    subdirectory = findProcess.stdout.readline().strip()
    if subdirectory == "":
      break
    print(subdirectory)
    rename(subdirectory)
    #if len(patientMap.keys()) > 20:
      #break
  except:
      print ('-'*40)
      import traceback
      traceback.print_exc() # XXX But this goes to stderr!
      print ('-'*40)

fp = open(os.path.join(sourceDirectory, "patientMap.json"), 'w')
fp.write(json.dumps(patientMap))
fp.close()
fp = open(os.path.join(sourceDirectory, "studyMap.json"), 'w')
fp.write(json.dumps(studyMap))
fp.close()
