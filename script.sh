#!/bin/sh
dest_f_dir="PUT THE DIRECTORY WHERE YOU WANT YOUR VIDEOS TO GO"

for i in `seq 300`
do
    python3 gen.py $(faker word | tr -d '\n') $(faker word | tr -d '\n')
    rand=$(head -c 5 /dev/urandom | xxd -u -ps)
    mv final.mp4 "${dest_f_dir}/${rand}${i}.mp4"
done
