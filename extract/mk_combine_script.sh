ls /scratch/01329/poldrack/GOBS/GOBS_bids/derivatives/fmriprep/|grep "sub" | grep -v "html">subcodes
cat subcodes | sed 's/^/python combine_data.py /' > run_combine.sh
