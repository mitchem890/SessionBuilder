import os
import shutil

#####################################################################################################
# USEAGE: To assist in building sessions for the DMCC HCP pipelines using Files Dowloaded from intraDB
# CREATED BY: Mitchell Jeffers
# DATE CREATED: 7/15/17
# LAST UPDATED: 7/25/17
#####################################################################################################
print "Warning, before using this program ensure that your scans do not contain more than one set of Structural Images \n The suggested Structual Images are non-Normalized"

USR = raw_input("Enter Cluster Username: ")
SUBJ = raw_input("Enter Subject: ")
SESS = raw_input("Enter Session: ")

ABV = SESS[:3].capitalize()

#WorkDir = '/home/mitchell/Desktop/practice/'+SUBJ+'/unprocessed/3T/'+SUBJ+'_'+SESS
WorkDir = '/scratch/' + USR + '/DMCCPILOT/DOWNLOADS/' + SUBJ + '/unprocessed/3T/' + SUBJ + '_' + SESS
Scans = WorkDir + '/scans'
structuralNames = ['T1w', 'T2w']
foundStructuralImages = []
expectedTrialFolders = ["rfMRI_Rest", "tfMRI_Axcpt", "tfMRI_Cuedts", "tfMRI_Stern", "tfMRI_Stroop"]


# finds the position of the nth needle in haystack 0 indexed
def findnth(haystack, needle, n):
    parts = haystack.split(needle, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(haystack) - len(parts[-1]) - len(needle)

# moves the files along with the current spin echos to their correct file
def movefile(root, name, SpinEchoAP, SpinEchoPA):
    newName = renameFile(name)
    folder = findFolder(newName)
    print "Moving From: " + os.path.join(root, name)
    print "To: " + os.path.join(WorkDir, findFolder(newName), newName)

    os.rename(os.path.join(root, name), os.path.join(WorkDir, findFolder(newName), newName))
    shutil.copy(SpinEchoAP, os.path.join(WorkDir, folder, renameFile(os.path.basename(SpinEchoAP))))
    shutil.copy(SpinEchoPA, os.path.join(WorkDir, folder, renameFile(os.path.basename(SpinEchoPA))))


# Setup Structural image folder and handle special Structural image naming scheme aswell as Check for duplicate Structural images
###TODO###Structural Images still overwriting eachother
def StructuralSetup(root, StructuralImage, SpinEchoAP, SpinEchoPA):
    if not os.path.isdir(os.path.join(WorkDir, "T1w_MPR1")):
        os.mkdir(os.path.join(WorkDir, "T1w_MPR1"))
    if not os.path.isdir(os.path.join(WorkDir, "T2w_SPC1")):
        os.mkdir(os.path.join(WorkDir, "T2w_SPC1"))
    if not os.path.isdir(os.path.join(WorkDir, "T1w")):
        os.mkdir(os.path.join(WorkDir, "T1w"))
    if not os.path.isdir(os.path.join(WorkDir, "T2w")):
        os.mkdir(os.path.join(WorkDir, "T2w"))
    newName = StructuralImage.replace(SUBJ + '_' + SESS + '_', '')
    newName = newName.replace('_MPR', '')
    newName = newName.replace('_SPC', '')
    folderName = newName.replace('.nii.gz', '')
    if any(x in folderName for x in foundStructuralImages):
        if not os.path.isdir(os.path.join(WorkDir, 'DuplicateFiles')):
            os.mkdir(os.path.join(WorkDir, 'DuplicateFiles'))
        print "FOUND DUPLICATE STRUCTURAL IMAGE: " + os.path.join(root, StructuralImage) + "\nImage will be placed in: " + os.path.join(WorkDir, 'Duplicate')
        os.rename(os.path.join(root, StructuralImage), os.path.join(WorkDir, 'DuplicateFiles', StructuralImage))
    else:
        foundStructuralImages.append(folderName)
        shutil.copy(os.path.join(root, StructuralImage), os.path.join(WorkDir, folderName, newName))
        movefile(root, StructuralImage, SpinEchoAP, SpinEchoPA)


# pads files names with zeros if need to maintain order
def StandardizeFileName(oldFileName):
    num, file = oldFileName.split('-')
    num = num.rjust(2, '0')
    newFileName = num + "-" + file
    return newFileName


# renames files based on Pipeline required Structure
#replace the session name with 3T
#replace Structural appendices
#add the session abbreviation to the Rest tag
#replace Rest numbers with 1 or 2 deending on original scan numbers
def renameFile(oldFilename):
    newFilename = oldFilename

    if '_' + SESS + '_' in oldFilename:
        newFilename = oldFilename.replace('_' + SESS + '_', '_3T_')
    if any(x in name for x in structuralNames):
        newFilename = newFilename.replace("MPR", "MPR1")
        newFilename = newFilename.replace("SPC", "SPC1")
    elif "_Rest" in newFilename:
        a = newFilename.index("Rest")
        newFilename = newFilename.replace("Rest", "Rest" + ABV)
        if (int(newFilename[a+7])%2 is 0):
            newFilename = newFilename[:a + 7] + '2' + newFilename[a + 8:]
        else:
            newFilename = newFilename[:a + 7] + '1' + newFilename[a + 8:]

    return newFilename


# finds the folders to place the file based on DMCC standard name scheme
def findFolder(filename):
    a = findnth(filename, '_', 1)
    folderName = filename[a + 1:]
    if "SBRef" in filename:
        folderName = folderName.replace("_SBRef", '')
    folderName = folderName.replace(".nii.gz", '')
    return folderName

#rename the directories with padded zeros to allow sorting
for directory in sorted(os.listdir(Scans)):
    os.rename(os.path.join(Scans, directory), os.path.join(Scans, StandardizeFileName(directory)))

for directory in sorted(os.listdir(Scans)):
    for root, dirs, files in os.walk(os.path.join(Scans, directory)):
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
            elif any(x in name for x in structuralNames):
                StructuralSetup(root, name, pathCurSpinEchoAP, pathCurSpinEchoPA)
            else:
                newName = renameFile(name)
                curFolder = findFolder(newName)
                print "Moving From: " + os.path.join(root, name)
                print "To: " + os.path.join(WorkDir, curFolder, newName)
                if not os.path.isdir(os.path.join(WorkDir, curFolder)):
                    os.mkdir(os.path.join(WorkDir, curFolder))
                os.rename(os.path.join(root, name), os.path.join(WorkDir, curFolder, newName))
                shutil.copy(pathCurSpinEchoAP, os.path.join(WorkDir, curFolder, renameFile(nameCurSpinEchoAP)))
                shutil.copy(pathCurSpinEchoPA, os.path.join(WorkDir, curFolder, renameFile(nameCurSpinEchoPA)))

shutil.rmtree(Scans)
