"""
convert from dcm2niix output to BIDS format

intended output:

/scratch/01329/poldrack/GOBS/GOBS_bids/sub-EO2055/anat:
sub-EO2055_acq-TI766_run-1_T1w.json    sub-EO2055_acq-TI794_run-1_T1w.json
sub-EO2055_acq-TI766_run-1_T1w.nii.gz  sub-EO2055_acq-TI794_run-1_T1w.nii.gz
sub-EO2055_acq-TI773_run-1_T1w.json    sub-EO2055_acq-TI801_run-1_T1w.json
sub-EO2055_acq-TI773_run-1_T1w.nii.gz  sub-EO2055_acq-TI801_run-1_T1w.nii.gz
sub-EO2055_acq-TI780_run-1_T1w.json    sub-EO2055_acq-TI808_run-1_T1w.json
sub-EO2055_acq-TI780_run-1_T1w.nii.gz  sub-EO2055_acq-TI808_run-1_T1w.nii.gz
sub-EO2055_acq-TI787_run-1_T1w.json    sub-EO2055_run-1_FLAIR.json
sub-EO2055_acq-TI787_run-1_T1w.nii.gz  sub-EO2055_run-1_FLAIR.nii.gz

/scratch/01329/poldrack/GOBS/GOBS_bids/sub-EO2055/dwi:
sub-EO2055_run-1_dwi.bval  sub-EO2055_run-1_dwi.json
sub-EO2055_run-1_dwi.bvec  sub-EO2055_run-1_dwi.nii.gz

/scratch/01329/poldrack/GOBS/GOBS_bids/sub-EO2055/fmap:
sub-EO2055_magnitude1.json    sub-EO2055_magnitude2.json    sub-EO2055_phasediff.json
sub-EO2055_magnitude1.nii.gz  sub-EO2055_magnitude2.nii.gz  sub-EO2055_phasediff.nii.gz

/scratch/01329/poldrack/GOBS/GOBS_bids/sub-EO2055/func:
sub-EO2055_task-rest_run-1_bold.json    sub-EO2055_task-rest_run-1_events.tsv
sub-EO2055_task-rest_run-1_bold.nii.gz

"""

import sys,os,glob,shutil
import json
import subprocess

def run_shell_cmd(cmd,cwd=[]):
    """ run a command in the shell using Popen
    """
    stdout_holder=[]
    if cwd:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,cwd=cwd)
    else:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
             print(line.strip())
             stdout_holder.append(line.strip())
    process.wait()
    return stdout_holder
basedir='/scratch/01329/poldrack/GOBS/'
niidir=os.path.join(basedir,'GOBS_nii')
bidsdir=os.path.join(basedir,'GOBS_bids')
assert len(sys.argv)>1
subcode=sys.argv[1] #'sub-EO2055'

subdir=os.path.join(niidir,subcode)

if os.path.exists(os.path.join(bidsdir,subcode)):
    print('bids dir already exists! removing')
    shutil.rmtree(os.path.join(bidsdir,subcode))

os.mkdir(os.path.join(bidsdir,subcode))

niifiles=[os.path.basename(i) for i in glob.glob(os.path.join(subdir,'*.nii.gz'))]
assert len(niifiles)>0

filetype_dict={'field_mapping':'fmap',
            'FLAIR':'anat',
            'MPRAGE':'anat',
            'MoCoSeries_ep2d_bold__':'func',
            'high_res_dti_high_res_dti':'dwi'}
filetype={}
files_by_type={}
for v in filetype_dict.values():
    files_by_type[v]=[]
for f in niifiles:
    for ft in filetype_dict:
        if f.find(ft)==0:
            filetype[f]=filetype_dict[ft]
            files_by_type[filetype_dict[ft]].append(f)

cmds=[] # save all commands to a list

# process BOLD

boldfiles=files_by_type['func']
if len(boldfiles)>0:
    os.mkdir(os.path.join(bidsdir,subcode,'func'))
    boldfiles.sort()

    for i,f in enumerate(boldfiles):
        cmd='cp %s/%s %s/%s/func/%s_task-rest_run-%d_bold.nii.gz'%(subdir,
            f,bidsdir,subcode,subcode,i+1)
        cmds.append(cmd)
        metadata=json.loads(open(os.path.join(subdir,f.replace('nii.gz','json'))).read())
        metadata['TaskName']='rest'
        with open('%s/%s/func/%s_task-rest_run-%d_bold.json'%(bidsdir,subcode,subcode,i+1),'w') as outfile:
            json.dump(metadata,outfile, sort_keys=True, indent=4)


# process field_mapping
fmapfiles=files_by_type['fmap']
if len(fmapfiles)>0:
    os.mkdir(os.path.join(bidsdir,subcode,'fmap'))
    fmapfiles.sort()
    echoTime={}
    filetype={}

    # first load json files to get metadata to distinguish files and get echo times
    for f in fmapfiles:
        metadata=json.loads(open(os.path.join(subdir,f.replace('nii.gz','json'))).read())
        print(echoTime)
        if metadata['ImageType'][2]=='M':
            filetype[f]='magnitude'
            echoTime[f]=metadata['EchoTime']
        elif metadata['ImageType'][2]=='P':
            filetype[f]='phasediff'
        else:
            print('skipping!')
            print(metadata['ImageType'])


    # now load data and copy files
    magctr=1
    echotimes=list(echoTime.values())
    assert len(echotimes)==2
    echotimes.sort()
    for f in fmapfiles:
        if filetype[f]=='magnitude':
            cmd='cp %s/%s %s/%s/fmap/%s_magnitude%d.nii.gz'%(subdir,
                f,bidsdir,subcode,subcode,magctr)
            cmds.append(cmd)
            cmd='cp %s/%s %s/%s/fmap/%s_magnitude%d.json'%(subdir,
                f.replace('nii.gz','json'),bidsdir,subcode,subcode,magctr)
            cmds.append(cmd)
            magctr+=1
        elif filetype[f]=='phasediff':
            cmd='cp %s/%s %s/%s/fmap/%s_phasediff.nii.gz'%(subdir,
                f,bidsdir,subcode,subcode)
            cmds.append(cmd)
            metadata=json.loads(open(os.path.join(subdir,f.replace('nii.gz','json'))).read())
            metadata['EchoTime1']=echotimes[0]
            metadata['EchoTime2']=echotimes[1]
            del metadata['EchoTime']
            with open('%s/%s/fmap/%s_phasediff.json'%(bidsdir,subcode,subcode),'w') as outfile:
                json.dump(metadata,outfile, sort_keys=True, indent=4)

# process anatomical
anatfiles=files_by_type['anat']
if len(anatfiles)>0:
    os.mkdir(os.path.join(bidsdir,subcode,'anat'))
    anatfiles.sort()

    for f in anatfiles:
        if f.find('MPRAGE')==0:
            TIflag=f.split('_')[5].replace('-','')
            cmd='cp %s/%s %s/%s/anat/%s_acq-%s_run-1_T1w.nii.gz'%(subdir,
                f,bidsdir,subcode,subcode,TIflag)
            cmds.append(cmd)
            cmd='cp %s/%s %s/%s/anat/%s_acq-%s_run-1_T1w.json'%(subdir,
                f.replace('nii.gz','json'),bidsdir,subcode,subcode,TIflag)
            cmds.append(cmd)
        # sub-EO2055_acq-TI794_run-1_T1w.nii.gz
        elif f.find('FLAIR')==0:
            cmd='cp %s/%s %s/%s/anat/%s_run-1_FLAIR.nii.gz'%(subdir,
                f,bidsdir,subcode,subcode)
            cmds.append(cmd)
            cmd='cp %s/%s %s/%s/anat/%s_run-1_FLAIR.json'%(subdir,
                f.replace('nii.gz','json'),bidsdir,subcode,subcode)
            cmds.append(cmd)

# process DWI

dwifiles=files_by_type['dwi']
if len(dwifiles)>0:
    os.mkdir(os.path.join(bidsdir,subcode,'dwi'))
    dwifiles.sort()

    for f in dwifiles:
        f=f.replace('#','\#')
        cmd='cp %s/%s %s/%s/dwi/%s_dwi.nii.gz'%(subdir,
            f,bidsdir,subcode,subcode)
        cmds.append(cmd)
        for extension in ['bval','bvec']:
            cmd='cp %s/%s %s/%s/dwi/%s_dwi.%s'%(subdir,
                f.replace("nii.gz",extension),bidsdir,subcode,subcode,extension)
            cmds.append(cmd)
        cmd='cp %s/%s %s/%s/dwi/%s_dwi.json'%(subdir,
            f.replace('nii.gz','json'),bidsdir,subcode,subcode)
        cmds.append(cmd)

output=[]
for cmd in cmds:
    output.append(run_shell_cmd(cmd))
