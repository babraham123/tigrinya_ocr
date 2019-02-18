#!/bin/bash
# commands to train and run Tesseract OCR

dpkg --listfiles tesseract-ocr-eng

tesseract --print-parameters >> tessconfigs.log

# convert a pdf into tiff files, one per page
convert -density 300 tir_testdata.pdf -depth 8 -background white \
  -flatten +matte tir_testdata-%02d.tiff

# try tesseract for the generated tiff files
# repeat for fast, int, best
for i in {00..18}
do
  tesseract ~/tigrinya_ocr/eval/tir_testdata-$i.tiff ~/tigrinya_ocr/tessdata/best/tir_eval-$i \
  -l tir --oem 1 --tessdata-dir ~/tigrinya_ocr/tessdata/best --psm 3
done

# evaluate, need to format ground truth txt files
uni2asc < ~/tigrinya_ocr/tessdata/best/tir_eval-00.txt > ~/tigrinya_ocr/eval/tir_testdata_ascii-00.txt
uni2asc < ~/tigrinya_ocr/eval/tir_groundtruth.txt > ~/tigrinya_ocr/eval/tir_groundtruth_ascii.txt
accuracy ~/tigrinya_ocr/eval/tir_groundtruth.txt ~/tigrinya_ocr/tessdata/best/tir_eval-00.txt
accuracy ~/tigrinya_ocr/eval/tir_groundtruth_ascii.txt ~/tigrinya_ocr/eval/tir_testdata_ascii-00.txt

# create a new tir.traineddata
combine_lang_model --input_unicharset ~/tigrinya_ocr/langdata/Ethiopic.unicharset \
  --script_dir ~/tigrinya_ocr/langdata --output_dir ~/tigrinya_ocr/training \
  --words ~/tigrinya_ocr/langdata/tir/tir.wordlist \
  --puncs ~/tigrinya_ocr/langdata/tir/tir.punc \
  --numbers ~/tigrinya_ocr/langdata/tir/tir.numbers \
  --lang tir --version_str 0.0.1

# list fonts
fc-list | grep tir_fonts
text2image --list_available_fonts --fonts_dir /usr/local/share/fonts/tir_fonts

# update language specific fonts under AMHARIC_FONTS
sudo vi /usr/share/tesseract-ocr/language-specific.sh

sudo mv /usr/share/tesseract-ocr/4.00/tessdata/tir.traineddata ~/tigrinya_ocr/original
sudo cp ~/tigrinya_ocr/training/tir/tir.traineddata /usr/share/tesseract-ocr/4.00/tessdata/tir.traineddata

# generate test data
/usr/share/tesseract-ocr/tesstrain.sh \
  --fontlist "Abyssinica SIL" "Abyssinica SIL Sebatbeit" "Abyssinica SIL Ximtanga" "Code2003 Medium" "Droid Sans Ethiopic" "Droid Sans Ethiopic Bold" "Ethiopia Jiret" "Ethiopic Fantuwua" "Ethiopic Hiwua" "Ethiopic Tint" "Ethiopic WashRa Bold, Bold" "Ethiopic WashRa SemiBold, Bold" "Ethiopic Wookianos" "Ethiopic Yebse" "Ethiopic Zelan" "GF Zemen Unicode" "Noto Sans Ethiopic" "Noto Sans Ethiopic Bold" "Ethiopic Yigezu Bisrat Goffer" "Ethiopic Yigezu Bisrat Gothic" \
  --fonts_dir /usr/local/share/fonts/tir_fonts \
  --lang tir --langdata_dir ~/tigrinya_ocr \
  --output_dir ~/tigrinya_ocr/generated \
  --overwrite --linedata_only --exposures 0 --noextract_font_properties \
  --training_text ~/tigrinya_ocr/eval/tir_groundtruth.txt \
  --wordlist ~/tigrinya_ocr/tir/tir.wordlist \
#  --tessdata_dir ~/tigrinya_ocr/training 

for font in "Abyssinica SIL" "Abyssinica SIL Sebatbeit" "Abyssinica SIL Ximtanga" "Code2003 Medium" "Droid Sans Ethiopic" "Ethiopia Jiret" "Ethiopic Fantuwua" "Ethiopic Hiwua" "Ethiopic Tint" "Ethiopic WashRa Bold, Bold" "Ethiopic WashRa SemiBold, Bold" "Ethiopic Wookianos" "Ethiopic Yebse" "Ethiopic Zelan" "GF Zemen Unicode" "Noto Sans Ethiopic" "Ethiopic Yigezu Bisrat Goffer" "Ethiopic Yigezu Bisrat Gothic"
do
  /usr/share/tesseract-ocr/tesstrain.sh \
    --fontlist "$font" \
    --fonts_dir /usr/local/share/fonts/tir_fonts \
    --lang tir --langdata_dir ~/tigrinya_ocr/langdata \
    --output_dir ~/tigrinya_ocr/generated \
    --overwrite --linedata_only --exposures 0 --noextract_font_properties \
    --training_text ~/tigrinya_ocr/eval/tir_groundtruth.txt \
    --wordlist ~/tigrinya_ocr/langdata/tir/tir.wordlist \
  #  --tessdata_dir ~/tigrinya_ocr/training
done

# view generated images
gksudo nautilus --browser /tmp/tmp.wpk6QANxS5/tir
xdg-open /tmp/tmp.wpk6QANxS5/tir/tir.Abyssinica_SIL.exp0.tif

# create filnames file
ls -d ~/tigrinya_ocr/generated/*.lstmf > ~/tigrinya_ocr/generated/tir.training_files.txt

# evaluate model
lstmeval --model ~/tigrinya_ocr/langdata/tir/tir_best.traineddata \
  --eval_listfile ~/tigrinya_ocr/generated/tir.training_files.txt
# At iteration 0, stage 0, Eval Char error rate=38.163577, Word error rate=37.982017

lstmtraining --model_output ~/tigrinya_ocr/tuning \
  --continue_from ~/tigrinya_ocr/langdata/tir/tir_best.traineddata \
  --traineddata ~/tigrinya_ocr/langdata/tir/tir.traineddata \
  --train_listfile ~/tigrinya_ocr/generated/tir.training_files.txt \
  --max_image_MB 3000 &> ~/tigrinya_ocr/logs/try1.log
#  [--perfect_sample_delay 0] [--debug_interval 0] \
#  [--max_iterations 0] [--target_error_rate 0.01] \

lstmeval --model ~/tigrinya_ocr/training/checkpoint \
  --traineddata ~/tigrinya_ocr/langdata/tir/tir.traineddata \
  --eval_listfile ~/tigrinya_ocr/generated/tir.training_files.txt


export TESSDATA_PREFIX=/home/babraham/tigrinya_ocr/training
java -jar VietOCR.jar

# segmentation
convert -density 300 TIGRINA_SUN_9_APR_2017.pdf -depth 8 -background white -flatten +matte TIGRINA_SUN_9_APR_2017-%02d.tiff
# convert TIGRINA_SUN_9_APR_2017-00.tiff -bordercolor White -border 10x10 427-1b.jpg
ls /usr/share/tesseract-ocr/4.00/tessdata/configs/
vi tessconfig
```
debug_file tesseract.log
tessedit_write_images 1
tessedit_create_hocr 1
segment_nonalphabetic_script 1
tessedit_dump_pageseg_images 1
```
tesseract TIGRINA_SUN_9_APR_2017-00.tiff tir_eval-00 -l tir --psm 2 tessconfig
tesseract TIGRINA_SUN_9_APR_2017-00.tiff tir_eval-01 -l tir --psm 1 hocr
