# SessionBuilder
Assist in Building Sessions for Pipelines Running DMCC

These programs are to be used together

Inorder to use these programs you should set up your .bashrc to export your cluster user name as USERNAME. to accomplish this add the following lines to your .bashrc:

export USERNAME=CLUSTERUSERNAMEHERE

after doing that disconnect and reconnect to the cluster to load changes.

You should also add a 
.netrc file to your home directory


What are the Programs:

IntraDBDownloader.sh:
will download all the nifti files from a session of a subject intraDB to the directory:
/scratch/USERNAME/DMCCPILOT/DOWNLOADS

IntraDBSelector.sh:
will download selected NIFTIs from a session of a subject to the directory:
/scratch/USERNAME/DMCCPILOT/DOWNLOADS
input desired scans comma separated when prompted, like the Following
SCANS:12,13,14,15

SessionBuilder.py:
will build the sessions from the resulting file structure of intraDBDownloader or IntraDBSelector
If duplicatly named scans are downloaded the second set of scans will be placed into Duplicate_Files in the directory.
It is suggested to use non-normalized images.
This program will also remove any Strooptest Files along with the scans directory once it has finished
This program can handle sessions with multiple spinechos pairs


