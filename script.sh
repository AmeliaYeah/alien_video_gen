#!/bin/sh
for i in `seq 300`
do
    python3 gen.py $(faker word | tr -d '\n') $(faker word | tr -d '\n')
    rand=$(head -c 5 /dev/urandom | xxd -u -ps)
    mv final.mp4 "/tmp/tmp.iwG5YW2VYA/${rand}${i}.mp4"
done
