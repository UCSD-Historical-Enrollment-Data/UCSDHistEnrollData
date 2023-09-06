#!/bin/bash

TERM="2023Fall"

# check if the term folder exists
# If it does, pull from repo for latest updates.
# Otherwise, clone
if [[ -d $TERM ]]; then
    cd $TERM
    git pull
    
else
    echo "cloning..."
    git clone https://github.com/ewang2002/UCSDHistEnrollData/$TERM
    cd $TERM
fi

START_PLOT=`date +%s` # start timer 

echo "================== Processing $TERM. =================="
echo "Cleaning raw CSVs."
# do we need python3? 
python clean_raw_csvs.py

echo "Categorizing enroll data."
python enroll_data_cleaner.py $term

echo "Plotting overall data."
python plot.py o
echo "Plotting section data."
python plot.py s

python list_files.py
python generate_toc.py

END_PLOT=$(date +%s)

PLOT_TIME=$((END_PLOT-START_PLOT))

# =============================================================== #
#                           GIT                                   # 
# =============================================================== #
START_GIT=$(date +%s)

BASE_MSG="$(date +%m-%d-%Y) - updated (plot, automated)"
DUR_MSG="Took: $(printf "%.2f\n" $((10**2 * PLOT_TIME/60))e-2) minutes to plot."

# commit
echo "Committing changes."
git add .
git commit -m $BASE_MSG -m $DUR_MSG
git push

END_GIT=$(date +%s)

GIT_TIME=$((END_GIT-START_GIT))

# =============================================================== #
#                         DONE                                    # 
# =============================================================== #

echo "[plot] Took $(printf "%.2f\n" $((10**2 * PLOT_TIME/60))e-2) minutes to complete!"
echo "[git ] Took $(printf "%.2f\n" $((10**2 * GIT_TIME/60))e-2) minutes to complete!"