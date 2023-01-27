# Alien Video Generator
Random video generator, in python, that generates wacky and goofy ahh alien shitposts. Originally designed for Crispy Concords and his PO box unboxings.

This requires the `ffmpeg` binary to be installed on your system. Pip3 requirements are show in the `pip_requirements.txt` file. Please run `pip3 install -r pip_requirements.txt`.

`gen.py` is the script that generates a single video, `script.sh` is what continuously generates videos and dumps them into a directory (or, in my case, an external device mountpoint). It is strongly recommended to generate a few test videos with `gen.py` first before relying on `script.sh` as there is a non-zero chance of your video output not being what is expected and wasting all the time generating your glorious shitposts.
