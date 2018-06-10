ls /scratch/01329/poldrack/GOBS/GOBS_bids/derivatives/fmriprep/|grep "sub" | grep -v "html">subcodes
cat subcodes | sed 's/^/python mk_scrubbing_masks.py /' > mk_scrubbing_masks.sh
