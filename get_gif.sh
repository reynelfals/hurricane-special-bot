#!/bin/bash
curl $1 >./data/$2_temp.gif
if [ -f $2.gif ]
then
  DIFF=$(diff ./data/$2.gif ./data/$2_temp.gif)
else
  DIFF="something"
fi

if [ "$DIFF" != "" ]
then
    mv ./data/$2.gif ./data/$2_old.gif
    mv ./data/$2_temp.gif ./data/$2.gif
    gifsicle --colors 256 ./data/$2.gif --resize 500x500 > ./data/$2_resized500_500.gif
    gifsicle --use-colormap gray --colors 16 ./data/$2.gif --resize 500x500 > ./data/$2_resized500_500_gray.gif

    date  >> ./data/history.log
    md5sum ./data/$2.gif >> ./data/history.log
    md5sum ./data/$2_resized500_500.gif >> ./data/history.log
    echo "---------------------------------------------------------------------------" >> ./data/history.log
fi
rm ./data/$2_temp.gif

