#mris_convert --annot <annot> $FREESURFER_SUBJECTS/fsaverage/lh.white lh.<annot>.fsaverage
mris_convert --annot lh.HCP-MMP1.annot /Applications/freesurfer/subjects/fsaverage/surf/lh.white lh.HCP-MM1.fsaverage.annot
mris_convert --annot rh.HCP-MMP1.annot /Applications/freesurfer/subjects/fsaverage/surf/rh.white rh.HCP-MM1.fsaverage.annot
#mri_surf2surf --mapmethod nnf --srcsubject fsaverage --sval lh.<annot>.fsaverage --trgsubject fsaverage5 --tval lh.<annot>.fsaverage5
mri_surf2surf --mapmethod nnf --hemi lh --srcsubject fsaverage --sval-annot /Applications/freesurfer/subjects/fsaverage/label/lh.HCP-MM1.fsaverage.annot --trgsubject fsaverage5 --tval lh.HCP-MM1.annot
mris_convert --annot /Applications/freesurfer/subjects/fsaverage5/label/lh.HCP-MM1.annot /Applications/freesurfer/subjects/fsaverage5/surf/lh.white lh.HCP-MMP1.fsaverage5.gii