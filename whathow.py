from datetime import datetime
from moviepy.editor import *


def gen_video(image_path):
    resolution = (640, 480)

    # Load sound (should start at 20 seconds)
    snd_clip = AudioFileClip(
        "./res/whathowsound.mp4").subclip(20, 30.15)

    # Generate text --- THIS DOESN'T WORK WITH SOME VERSIONS OF IMAGEMAGICK ---
    what_txt = TextClip(txt="WHAT", font="NimbusSans-Bold", color="white",
        kerning=2, align='north', fontsize=50).set_duration(snd_clip.duration)
    how_txt = TextClip(txt="HOW", font="NimbusSans-Regular", color="white",
        kerning=2, align='north', fontsize=24).set_duration(snd_clip.duration)

    # Load image
    img_clip = ImageClip(image_path).set_pos("center").set_fps(24)

    # Determine how much to scale the image based on the original size
    scale_x = resolution[0] / img_clip.w
    scale_y = resolution[1] / img_clip.h

    scale = scale_x if scale_x < scale_y else scale_y
    print(f"Original res is {img_clip.size}, scaling by {scale}")

    final_scale = 0.5 if scale <= 1.0 else scale - scale.__floor__()

    big_clip = img_clip.resize(scale)
    tmp = big_clip.resize(final_scale)
    small_clip = tmp.set_pos(("center", ((resolution[1] - tmp.h) / 2) - 75))\
        .margin(mar=10).margin(mar=3, color=(255, 255, 255))

    # Composite output video

    target = './tmp'

    file_name = 'what_how_%s.mp4' % datetime.now().microsecond

    output = CompositeVideoClip([big_clip.set_end(1), small_clip.set_start(
        1), what_txt.set_pos(("center", 0.73), relative=True).set_start(1), how_txt.set_pos(("center", 0.85), relative=True).set_start(1)], size=resolution).set_audio(snd_clip).set_duration(snd_clip.duration)
    output.write_videofile(
        f"{target}/{file_name}", audio_bitrate='160k')

    img_clip.close()
    snd_clip.close()
    what_txt.close()
    how_txt.close()
    output.close()

    print(f'Output whathow video at {target}/{file_name}')
    return f'{target}/{file_name}'
