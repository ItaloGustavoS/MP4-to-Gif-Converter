import imageio
import os, sys

class TargetFormat(object):
    GIF = ".gif"
    MP4 = ".mp4"
    AVI = ".avi"

def convertFile(inputpath, targetFormat):
    outputpath = os.path.splitext(inputpath)[0] + targetFormat
    print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(inputpath, outputpath))

    reader = imageio.get_reader(inputpath)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outputpath, fps=fps)
    for i,im in enumerate(reader):
        sys.stdout.write("\r Frame {0}".format(i))
        sys.stdout.flush()
        writer.append_data(im)
    print("\r\nFinalizando...")
    writer.close()
    print("Concluido!")

convertFile('C:\\Users\\Italo\\Desktop\\GifConverter\\Ed.mp4', TargetFormat.GIF)
