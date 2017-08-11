#!/bin/bash

DOWNLOAD_LOCATION=/scratch/${USERNAME}/DMCCPILOT/DOWNLOADS
HOST='intradb.humanconnectome.org'
read -p "ENTER PROJECT (DMCC_Phase2 or DMCC_Phase3): " PROJ;
read -p "ENTER SUBJECT: " SUBJ;
read -p "ENTER SESSION: " session;
pushd $DOWNLOAD_LOCATION
mkdir -p $SUBJ/unprocessed/3T/${SUBJ}_${session}
pushd $SUBJ/unprocessed/3T

for RESOURCE in $(IFS=% && curl -s -k -n https://intradb.humanconnectome.org/data/projects/${PROJ}/subjects/${SUBJ}/experiments/${SUBJ}_${session}/scans?format=csv | grep -F -e'mrScanData' | grep -F -e 'tfMRI' -e 'T1w' -e 'T2w' -e 'SpinEchoFieldMap' -e 'rfMRI'| cut -d, -f2,4,7; unset IFS); do
echo -e "RESOURCE=${RESOURCE}"
scan_num="$(echo ${RESOURCE} | cut -d, -f1)"
scan_qa="$(echo ${RESOURCE} | cut -d, -f2)"
scan_name="$(echo ${RESOURCE} | cut -d, -f3)"
#scan_note="$(echo ${RESOURCE} | cut -d, -f3)"
echo -e "\nDownloading scan ${scan_num}\tQUALITY ASSESSMENT:'${scan_qa}'\t${scan_name}'"
printf "%-5s  %-35s  %-20s\n" "${scan_num}" "${scan_name}" "${scan_qa}"

## TODO:
##  echo "curl -s -k -n https://$HOST/data/projects/$PROJ/subjects/${SUBJ}/experiments/${SUBJ}_3T/resources/$RESOURCE/files?format=zip"
	curl -k -n https://${HOST}/data/projects/${PROJ}/subjects/${SUBJ}/experiments/${SUBJ}_${session}/scans/${scan_num}/resources/NIFTI/files?format=zip > ${SUBJ}_${session}/tmp.zip && unzip ${SUBJ}_${session}/tmp.zip && rm ${SUBJ}_${session}/tmp.zip
## TODO: if scan_qa=unusable, break
## TODO: instead of ‘for x in $(curl ..)’, create a textfile and ‘while read < file’
done
popd
popd

