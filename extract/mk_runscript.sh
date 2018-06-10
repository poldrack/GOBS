ls /scratch/01329/poldrack/GOBS/GOBS_bids/derivatives/fmriprep/|grep "sub" | grep -v "html">subcodes
cat subcodes | sed 's/^/python extract_mmp1.py /' > run_extract.sh
