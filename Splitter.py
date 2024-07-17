import subprocess
from argparse import ArgumentParser, RawTextHelpFormatter


def get_video_length(video_name):
    output = subprocess.check_output(("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                      "default=noprint_wrappers=1:nokey=1", video_name)).strip()
    video_length = int(output)
    return video_length


def get_video_name(video_path):
    if "\\" in video_path:
        video_name_base = video_path.split("\\")[-1].split(".")[0]
        video_name_extension = video_path.split("\\")[-1].split(".")[1]
    if "/" in video_path:
        video_name_base = video_path.split("/")[-1].split(".")[0]
        video_name_extension = video_path.split("/")[-1].split(".")[1]
    if "\\" not in video_path and "/" not in video_path:
        video_name_base = video_path.split(".")[0]
        video_name_extension = video_path.split(".")[1]

    return video_name_base, video_name_extension


def split_by_duration(video_name, video_extension, video_length, duration):
    if duration and duration <= 0:
        print("The desired duration can't be equal or lower 0")
        raise SystemExit
    if duration >= video_length:
        print("The desired duration can't be equal or higher than the video duration")
        raise SystemExit
    commands = ["ffmpeg", "-i", video_name, "-c", "copy", "-map", "0"
                "-segment_time", "desired_duration", "-f", "segment",
                video_name + "%03d" + video_extension]
    pass


def split_by_parts(video_name, parts):
    pass


def main():
    parser = ArgumentParser(description="Tool to split videos either by duration or by parts",
                            epilog="""Examples for both arguments:
                            python Splitter.py -f videoFile.mp4 -sd 10 m(splits the video in 10m parts)
                            python Splitter.py -f vidoeFile.mp4 -sp 30(splits the video in 30 parts)""", formatter_class=RawTextHelpFormatter)

    parser.add_argument("-f", "--file", dest="video_name",
                        help="Input video name if its not in the same folder copy the full path to the video", type=str, action="store", required=True)
    parser.add_argument("-sd", "--split-duration", dest="duration",
                        help="Input the duration and the time unit(h,m,s)\nExample: -f test -sd 10 m", action="store", nargs=2)
    parser.add_argument("-sp", "--split-parts", dest="parts",
                        help="Input in how many parts the video should be split", type=int, action="store")
    args = parser.parse_args()
    video_name_base, video_extension = get_video_name(args.video_name)
    if args.duration is not None:
        print(args)
        video_length = get_video_length(args.video_name)
        split_by_duration(video_name_base, video_extension, video_length, args.duration)
        pass
    if args.parts is not None:
        pass


if __name__ == '__main__':
    main()