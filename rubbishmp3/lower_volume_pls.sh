#!/bin/bash
for i in `ls Music/*.mp3 | tr " " "\?"`; do
n=`basename "${i}"`
echo $n
b="c/${n}"
i=`tr "\?" " " <<<$i`
b=`tr "\?" " " <<<$b`
echo $i -\> $b
ffmpeg -y -i "$i" -c:v copy -c:a libmp3lame -map_metadata 0 -f mp3 -filter:a "volume=0.075" "$b"
done
