#!/bin/bash

# commands to train and run Tesseract OCR

training/boxtrain.sh \
  --fonts_dir  /mnt/c/Windows/Fonts \
  --training_text ../langdata/eng/nyd.training_text \
  --langdata_dir ../langdata \
  --tessdata_dir ./tessdata \
  --lang eng  \
  --exposures "-2 -1 0" \
  --fontlist "Century Schoolbook" "Dejavu Serif" "Garamond" "Liberation Serif" "Times New Roman," "FreeSerif" "Georgia" \
  --output_dir ~/tesstutorial/nydlegacy

training/boxtrain.sh \
  --fonts_dir  /mnt/c/Windows/Fonts \
  --training_text ../langdata/eng/nyd.training_text \
  --langdata_dir ../langdata \
  --tessdata_dir ./tessdata \
  --lang eng \
  --linedata_only \
  --noextract_font_properties \
  --exposures "-2 -1" \
  --fontlist "Bookman Old Style Semi-Light"  \
  --output_dir ~/tesstutorial/nyd
  
combine_tessdata -e ../tessdata/eng.traineddata \
   ~/tesstutorial/eng_from_nyd/eng.lstm

lstmtraining  \
   -U ~/tesstutorial/nyd/eng.unicharset \
  --train_listfile ~/tesstutorial/nyd/eng.training_files.txt \
  --script_dir ../langdata   \
  --append_index 5 --net_spec '[Lfx256 O1c105]' \
  --continue_from ~/tesstutorial/eng_from_nyd/eng.lstm \
  --model_output ~/tesstutorial/eng_from_nyd/nyd \
  --debug_interval -1 \
  --target_error_rate 0.01
   
lstmtraining \
  --continue_from ~/tesstutorial/eng_from_nyd/nyd_checkpoint \
  --model_output ~/tesstutorial/eng_from_nyd/nyd.lstm \
  --stop_training

cp ../tessdata/eng.traineddata ~/tesstutorial/eng_from_nyd/nyd.traineddata
   
combine_tessdata -o ~/tesstutorial/eng_from_nyd/nyd.traineddata \
  ~/tesstutorial/eng_from_nyd/nyd.lstm \
  ~/tesstutorial/nyd/eng.lstm-number-dawg \
  ~/tesstutorial/nyd/eng.lstm-punc-dawg \
  ~/tesstutorial/nyd/eng.lstm-word-dawg 
 
