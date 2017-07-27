#!/bin/bash

DOWNLOAD_LOCATION=/scratch/mjeffers/DMCCPILOT/DOWNLOADS
read -p "ENTER PROJECT; " PROJ;
echo $PROJ
read -p "ENTER SUBJECT: " SUBJ; 
echo $SUBJ
read -p "ENTER SESSION: " SESSION; 
echo $SESSION
read -p "ENTER SCAN NUMBERS: " SCANS;
echo $SCANS

pushd $DOWNLOAD_LOCATION
mkdir -p $SUBJ/unprocessed/3T
pushd $SUBJ/unprocessed/3T


curl -k -n https://intradb.humanconnectome.org/data/projects/${PROJ}/subjects/${SUBJ}/experiments/${SUBJ}_${SESSION}/scans/${SCANS}/resources/NIFTI/files?format=zip>tmp.zip && unzip tmp.zip && rm tmp.zip

popd
popd
