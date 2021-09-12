import argparse
import shutil
import time
from pathlib import Path
import ffmpeg
import numpy as np
from extract_features import run
from resnet_50 import i3_res50


def generate(datasetpath, outputpath, pretrainedpath, frequency, batch_size, sample_mode):
    Path(outputpath).mkdir(parents=True, exist_ok=True)
    temppath = outputpath + "/temp/"
    rootdir = Path(datasetpath)
    videos = [str(f) for f in rootdir.glob('**/*.mp4')]
    # setup the model，一个预训练模型
    i3d = i3_res50(400, pretrainedpath)
    # i3d.cuda()
    i3d.train(False)  # Set model to evaluate mode

    for video in videos:
        videoname = video.split("/")[-1].split(".")[0]
        startime = time.time()  # 这个时间其实与视频时间无关
        print("Generating for {0}".format(video))
        Path(temppath).mkdir(parents=True, exist_ok=True)
        # 先把video转成图片
        # 大致按照1s三十帧
        # ffmpeg.input(video).output('{}%d.jpg'.format(temppath), start_number=0).global_args('-loglevel', 'quiet').run()
        print("Preprocessing done..")
        features = run(i3d, frequency, temppath, batch_size, sample_mode)

        # 保存特征
        np.save(outputpath + "/" + videoname, features)
        print("Obtained features of size: ", features.shape)
        shutil.rmtree(temppath)
        print("done in {0}.".format(time.time() - startime))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--datasetpath', type=str, default="samplevideos/")
    parser.add_argument('--outputpath', type=str, default="output")
    parser.add_argument('--pretrainedpath', type=str, default="pretrained/i3d_r50_kinetics.pth")
    parser.add_argument('--frequency', type=int, default=16)
    parser.add_argument('--batch_size', type=int, default=20)
    parser.add_argument('--sample_mode', type=str, default="oversample")
    args = parser.parse_args()
    generate(args.datasetpath, str(args.outputpath), args.pretrainedpath, args.frequency, args.batch_size,
             args.sample_mode)
