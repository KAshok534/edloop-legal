"""Make the web copies of the "study together" film for the home page (assets/video/).

    python tools/encode_film.py <landscape.mp4> <vertical.mp4>

The masters are HyperFrames renders in the private IIT-APP repository
(marketing/videos/edloop-together/renders and marketing/videos/edloop-together-reels/renders, 4K 60 fps, about 41 MB
each). They never go into this public repository, only these encodes:

    assets/video/edloop-together-1080.mp4          1920x1080, 60 fps, H.264 CRF 27, AAC 96k   (about 3.6 MB, desktop)
    assets/video/edloop-together-vertical-720.mp4  720x1280, 30 fps, H.264 CRF 27, AAC 96k    (about 2.0 MB, phones)
    assets/video/poster-wide.jpg, poster-tall.jpg  frame at 6.2 s ("Race your friends. Live.")

Needs ffmpeg on PATH. premium.js picks the file by screen width; Data Saver and reduced motion get the poster only.
The film shows features that ship with app 0.9.10 (friends, challenges, this week): publish it with that release.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "video"


def run(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], check=True)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    wide, tall = sys.argv[1], sys.argv[2]
    OUT.mkdir(parents=True, exist_ok=True)
    codec = ["-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p", "-profile:v", "high",
             "-movflags", "+faststart", "-c:a", "aac", "-b:a", "96k"]
    run("-i", wide, "-vf", "scale=1920:1080:flags=lanczos", *codec, OUT / "edloop-together-1080.mp4")
    run("-i", tall, "-vf", "scale=720:1280:flags=lanczos,fps=30", *codec, OUT / "edloop-together-vertical-720.mp4")
    run("-ss", "6.2", "-i", wide, "-frames:v", "1", "-vf", "scale=1920:1080", "-q:v", "4", OUT / "poster-wide.jpg")
    run("-ss", "6.2", "-i", tall, "-frames:v", "1", "-vf", "scale=720:1280", "-q:v", "4", OUT / "poster-tall.jpg")
    for f in sorted(OUT.iterdir()):
        print(f"{f.name}: {f.stat().st_size / 1e6:.1f} MB")


main()
