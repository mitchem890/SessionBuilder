import os
import shutil
import glob
#####################################################################################################
#USEAGE: To assist in building sessions for the DMCC HCP pipelines using Files Dowloaded from intraDB
#CREATED BY: Mitchell Jeffers
#DATE CREATED: 7/15/17
#LAST UPDATED: 7/21/17
#####################################################################################################
print "Warning, before using this program ensure that your scans do not contain more than one set of Structural Images \n The suggested Structual Images are non-Normalized"

SUBJ = str(input("Enter Subject: "))
SESS = raw_input("Enter Session: ")
ABV=SESS[:3].capitalize()

#WorkDir = '/home/mitchell/Desktop/practice/'+SUBJ+'/unprocessed/3T/'+SUBJ+'_'+SESS
WorkDir = '/scratch/mjeffers/DMCCPILOT/test_session_download/DOWNLOADS/'+ SUBJ +'/unprocessed/3T/'+SUBJ+'_'+ SESS
Scans =  WorkDir +'/scans'

trialFolders = ["rfMRI_Rest",  "tfMRI_Axcpt",  "tfMRI_Cuedts", "tfMRI_Stern", "tfMRI_Stroop"]

#finds the position of the nth needle in haystack 0 indexed
def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)


#Setup Structural image folder and handle special Structural image naming scheme
def StructuralSetup(StructuralImage):
    if not os.path.isdir(os.path.join(WorkDir,"T1w_MPR1")):
        os.mkdir(os.path.join(WorkDir,"T1w_MPR1"))
    if not os.path.isdir(os.path.join(WorkDir,"T2w_SPC1")):
        os.mkdir(os.path.join(WorkDir,"T2w_SPC1"))
    if not os.path.isdir(os.path.join(WorkDir,"T1w")):
        os.mkdir(os.path.join(WorkDir, "T1w"))
    if not os.path.isdir(os.path.join(WorkDir,"T2w")):
        os.mkdir(os.path.join(WorkDir,"T2w"))



#pads files names with zeros if need to maintain order
def StandardizeFileName(oldFileName):
    num, file = oldFileName.split('-')
    num = num.rjust(2, '0')
    newFileName = num+"-"+file
    return newFileName


#renames files based on Pipeline required Structure
def renameFile(oldFilename):
    newFilename = oldFilename

    if '_'+SESS+'_' in oldFilename:
        newFilename = oldFilename.replace('_'+SESS+'_', '_3T_')

    if "_Rest" in newFilename:
        a = newFilename.index("Rest")
        newFilename = newFilename.replace("Rest", "Rest"+ABV)

        if "_AP" in newFilename:
            newFilename = newFilename[:a+7] + '1' + newFilename[a+8:]
        else:
            newFilename = newFilename[:a + 7] + '2' + newFilename[a + 8:]

    return newFilename


#finds the folders to place the file based on DMCC standard name scheme
def findFolder(filename):
    a = findnth(filename, '_', 1)
    folderName = filename[a+1:]
    if "SBRef" in filename:
        folderName = folderName.replace("_SBRef",'')
    folderName = folderName.replace(".nii.gz", '')
    return folderName


#Build Folders for that session based on DMCC standard naming scheme
for folder in trialFolders:
    if not os.path.isdir(os.path.join(WorkDir, folder+ABV+"1_AP")):
        os.mkdir(os.path.join(WorkDir,folder+ABV+"1_AP"))
    if not os.path.isdir(os.path.join(WorkDir, folder + ABV + "2_PA")):
        os.mkdir(os.path.join(WorkDir,folder+ABV+"2_PA"))


for directory in sorted(os.listdir(Scans)):
    os.rename(os.path.join(Scans, directory), os.path.join(Scans, StandardizeFileName(directory)))

for directory in sorted(os.listdir(Scans)):
    for root, dirs, files in os.walk(os.path.join(Scans,directory)):
        for name in files:
            if "SpinEchoFieldMap_AP" in name:
                pathCurSpinEchoAP = os.path.join(root, name)
                nameCurSpinEchoAP = name
                print "Found NEW SpinEchoAP: " + pathCurSpinEchoAP
            elif "SpinEchoFieldMap_PA" in name:
                pathCurSpinEchoPA = os.path.join(root, name)
                nameCurSpinEchoPA = name
                print "Found NEW SpinEchoPA: " + pathCurSpinEchoPA
            elif "StroopTest" in name:
                shutil.rmtree(os.path.join(root))
            else:
                ###TODO###ADD T1w and T2w exceptions
                if ('T1w','T2w') in name:
                    StructuralSetup(name)
                newName = renameFile(name)
                folder = findFolder(newName)
                print "Moving From: " + os.path.join(root, name)
                print "To: " + os.path.join(WorkDir, findFolder(newName), newName)
                os.rename(os.path.join(root, name), os.path.join(WorkDir, findFolder(newName), newName))
                shutil.copy(pathCurSpinEchoAP, os.path.join(WorkDir, folder, renameFile(nameCurSpinEchoAP)))
                shutil.copy(pathCurSpinEchoPA, os.path.join(WorkDir, folder, renameFile(nameCurSpinEchoPA)))

shutil.rmtree(Scans)
