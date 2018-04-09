#!/bin/bash

# commands to train and run Tesseract OCR

convert -density 300 tir_testdata.pdf -depth 8 -background white \
  -flatten +matte tir_testdata-%02d.tiff

# fast int best
for i in {00..18}
do
  tesseract ~/tigrinya_ocr/eval/tir_testdata-$i.tiff ~/tigrinya_ocr/tessdata/best/tir_eval-$i \
  -l tir --oem 1 --tessdata-dir ~/tigrinya_ocr/tessdata/best --psm 3
done

uni2asc < ~/tigrinya_ocr/tessdata/best/tir_eval-00.txt > ~/tigrinya_ocr/eval/tir_testdata_ascii-00.txt
uni2asc < ~/tigrinya_ocr/eval/tir_groundtruth.txt > ~/tigrinya_ocr/eval/tir_groundtruth_ascii.txt
accuracy ~/tigrinya_ocr/eval/tir_groundtruth.txt ~/tigrinya_ocr/tessdata/best/tir_eval-00.txt
accuracy ~/tigrinya_ocr/eval/tir_groundtruth_ascii.txt ~/tigrinya_ocr/eval/tir_testdata_ascii-00.txt

combine_lang_model --input_unicharset ~/tigrinya_ocr/tir/Ethiopic.unicharset \
  --script_dir ~/tigrinya_ocr/tir --output_dir ~/tigrinya_ocr/training --lang tir \
  --words ~/tigrinya_ocr/tir/tir.wordlist --puncs ~/tigrinya_ocr/tir/tir.punc --numbers ~/tigrinya_ocr/tir/tir.numbers \
  --version_str 0.0.1

lstmtraining --model_output ~/tigrinya_ocr/training1 [--max_image_MB 6000] \
  --traineddata ~/tigrinya_ocr/training/tir/tir.traineddata \
  --train_listfile /path/to/list/of/filenames.txt

export TESSDATA_PREFIX=/home/babraham/tigrinya_ocr/training

fc-list | grep tir_fonts

"Ethiopic WashRa SemiBold,Ethiopic Yigezu Bisrat Gothic,Ethiopic Tint,Code2003,Ethiopic Yebse,Ethiopic Zelan,Ethiopic Wookianos,Abyssinica SIL,Abyssinica SIL Zaima,GF Zemen Unicode,Abyssinica SIL Sebatbeit,Ethiopic Fantuwua,Ethiopic Yigezu Bisrat Goffer,Ethiopia Jiret,Ethiopic WashRa Bold,Ethiopic Hiwua,Abyssinica SIL Ximtanga"

tesstrain.sh \
  --fontlist "Ethiopic WashRa SemiBold,Ethiopic Yigezu Bisrat Gothic,Ethiopic Tint,Code2003,Ethiopic Yebse,Ethiopic Zelan,Ethiopic Wookianos,Abyssinica SIL,Abyssinica SIL Zaima,GF Zemen Unicode,Abyssinica SIL Sebatbeit,Ethiopic Fantuwua,Ethiopic Yigezu Bisrat Goffer,Ethiopia Jiret,Ethiopic WashRa Bold,Ethiopic Hiwua,Abyssinica SIL Ximtanga" \
  --fonts_dir /usr/local/share/fonts/tir_fonts \
  --lang tir --langdata_dir ~/tigrinya_ocr \
  --output_dir ~/tigrinya_ocr/training1 \
  --overwrite --linedata_only --exposures 0 \
  --training_text ~/tigrinya_ocr/eval/tir_groundtruth.txt \
  --wordlist ~/tigrinya_ocr/tir/tir.wordlist \
  --tessdata_dir ~/tigrinya_ocr/training

lstmtraining --model_output /path/to/output [--max_image_MB 6000] \
  --continue_from /path/to/existing/model \
  --traineddata /path/to/original/traineddata \
  [--perfect_sample_delay 0] [--debug_interval 0] \
  [--max_iterations 0] [--target_error_rate 0.01] \
  --train_listfile /path/to/list/of/filenames.txt

lstmeval --model ~/training/impact_checkpoint \
  --traineddata ~/tigrinya_ocr/tir/tir_best.traineddata \
  --eval_listfile ~/tesstutorial/engeval/eng.training_files.txt


export TESSDATA_PREFIX=/home/babraham/tigrinya_ocr/training
java -jar VietOCR.jar



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
 
