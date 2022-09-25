import sys
from mutagen.mp4 import MP4, MP4Cover
from mutagen import MutagenError


def embed(pic_data, mp4_name):
    try:
        mp4 = MP4(mp4_name)
        mp4.tags["covr"] = [MP4Cover(data=pic_data, imageformat=MP4Cover.FORMAT_JPEG)]
        mp4.save()
    except MutagenError as err:
        print("嵌入縮圖時出錯，詳情：")
        print(err)
        sys.exit(1)


# example:

# pic_name = "BG123.jpg"
# mp4_name = "任性 High-Spec [1].mp4"
# mp4 = MP4(mp4_name)

# with open(pic_name, 'rb') as pic:
#     pic_data = pic.read()
# mp4.tags["covr"] = [MP4Cover(data=pic_data, imageformat=MP4Cover.FORMAT_JPEG)]
# mp4.save()
