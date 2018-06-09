# convert MMP1 atlas from fsaverage to fsaverage5 space
export SUBJECTS_DIR=$WORK/subjects

#mris_convert --annot <annot> $FREESURFER_SUBJECTS/fsaverage/lh.white lh.<annot>.fsaverage
mris_convert --annot HCP-MMP1/lh.HCP-MMP1.annot ${SUBJECTS_DIR}/fsaverage/surf/lh.white lh.HCP-MMP1.fsaverage.annot
mris_convert --annot HCP-MMP1/rh.HCP-MMP1.annot ${SUBJECTS_DIR}/fsaverage/surf/rh.white rh.HCP-MMP1.fsaverage.annot
#mri_surf2surf --mapmethod nnf --srcsubject fsaverage --sval lh.<annot>.fsaverage --trgsubject fsaverage5 --tval lh.<annot>.fsaverage5
mri_surf2surf --mapmethod nnf --hemi lh --srcsubject fsaverage --sval-annot ${SUBJECTS_DIR}/fsaverage/label/lh.HCP-MMP1.fsaverage.annot --trgsubject fsaverage5 --tval lh.HCP-MMP1.annot
mris_convert --annot ${SUBJECTS_DIR}/fsaverage5/label/lh.HCP-MMP1.annot ${SUBJECTS_DIR}/fsaverage5/surf/lh.white HCP-MMP1/lh.HCP-MMP1.fsaverage5.gii
mri_surf2surf --mapmethod nnf --hemi rh --srcsubject fsaverage --sval-annot ${SUBJECTS_DIR}/fsaverage/label/rh.HCP-MMP1.fsaverage.annot --trgsubject fsaverage5 --tval rh.HCP-MMP1.annot
mris_convert --annot ${SUBJECTS_DIR}/fsaverage5/label/rh.HCP-MMP1.annot ${SUBJECTS_DIR}/fsaverage5/surf/rh.white HCP-MMP1/rh.HCP-MMP1.fsaverage5.gii
