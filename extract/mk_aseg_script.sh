ls /scratch/01329/poldrack/GOBS/GOBS_bids/derivatives/fmriprep/|grep "sub" | grep -v "html">subcodes
cat subcodes | sed 's/^/python extract_aseg_timeseries.py /' > run_aseg_extract.sh
