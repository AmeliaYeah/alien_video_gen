#generates a video out of many videos for Crispy Concords
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from faker import Faker
from bing_image_downloader import downloader
from pydub import AudioSegment
from argparse import ArgumentParser
from string import ascii_uppercase, punctuation, digits
import random, os, string, subprocess

#argparse
parser = ArgumentParser(description="random shitpost gen")
parser.add_argument("topic", help="Topic to shitpost about", nargs="+")
args = parser.parse_args()

#setup
charset = ascii_uppercase+punctuation+digits
f = Faker()

#get the number of frames for the video; download all neccessary images
num_frames = random.randint(10,30)
topic = " ".join(args.topic)
if os.path.isdir("./dataset"): os.system("rm -r ./dataset")
download_dir = f"./dataset/{topic}/"
try:
    downloader.download(topic, limit=num_frames)
except Exception as e:
    print(f"Download exception: {e}")
    exit()

#gen images
for i in range(num_frames):
    #setup
    print(f"On frame {i}")
    font_mult = random.randint(1,8)
    font = ImageFont.truetype("./Alien-Regular.ttf", 20*font_mult)

    #create image
    dim = (1920,1080)
    with Image.new("RGBA", dim, "black") as img:
        d = ImageDraw.Draw(img)

        #paste a random image if odds are in our favor
        p = None
        if random.randint(0,100) > 0:#40:
            #open the image
            chosen_path = download_dir+random.choice(os.listdir(download_dir))
            p = Image.open(chosen_path)

            #prep and paste
            try:
                p = p.resize(dim, Image.LANCZOS)
                #try changing Image.LANCZOS to Image.Resampling.LANCZOS if you're having issues with the images not appearing in the videos
                img.paste(p.filter(ImageFilter.FIND_EDGES), (0,0))
            except:
                pass

        #draw text
        random_coord = lambda is_x: random.randint(0, (img.width//(1.2*font_mult) if is_x else img.height))
        random_coords = lambda: (random_coord(True), random_coord(False))
        for num_of_text in range(random.randint(0, 17)):
            text_to_write = "".join(random.choices(charset, k=random.randint(10,50)//font_mult))
            d.text(random_coords(), text_to_write, font=font)

        #save the frame
        img.save(f"frame-{i:03}.png")

        #dispose of the overlay image if used
        if p is not None:
            p.close()
            os.remove(chosen_path)

#create video
os.system(f"ffmpeg -framerate 4 -i 'frame-%03d.png' -r 25 -c:v libx264 -pix_fmt yuv420p finished.mp4")
vid_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries","format=duration", "-of","default=noprint_wrappers=1:nokey=1", "finished.mp4"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout)
print(f"Video is {vid_len} long")

#create sound
with open("to_read.txt", "w") as to_read: to_read.write(f.paragraph())
raw_params = [
    f"sine=f={random.randint(220, 1600)}:b={random.randint(0,4)}:d={vid_len}",
    f"anoisesrc=a={random.randint(0,100)/200}:d={vid_len}",
    "flite=textfile=to_read.txt"
]
def create_sound(param_index):
    param = raw_params[param_index]
    if not os.path.isdir("sounds"): os.mkdir("sounds")
    os.system(f"ffmpeg -f lavfi -i '{param}' sounds/{param_index}.wav")
for raw_param_i in random.sample(range(len(raw_params)), k=random.randint(1,len(raw_params))):
    create_sound(raw_param_i)

#open all sounds
sounds = os.listdir("sounds")
if len(sounds) < 2:
    os.system("mv sounds/* out.wav")
else:
    #convert sounds into audiosegments
    segs = [AudioSegment.from_wav(f"sounds/{sound_f}") for sound_f in sounds]
    master: AudioSegment = segs[0]
    for seg in segs[1:]:
        master = seg.overlay(master, loop=True)

    #save as out.wav
    master.export("out.wav", "wav")

#combine sound with video
os.system(f"ffmpeg -i finished.mp4 -i out.wav -map 0:v:0 -map 1:a:0 -c:a aac final.mp4")

#cleanup
os.remove("out.wav")
os.remove("finished.mp4")
os.remove("to_read.txt")
os.system("rm frame-* && rm -r sounds")
