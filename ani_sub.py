import re
from pathlib import Path
import collections

re_index = re.compile("\d+")

class VItem:
    def __init__(self, file):
        self.file = file
        self.search_pos = 0
        self.found_pos = None
        self.found_num = None

def process_video(root_dir, suffix):
    video_list = []
    for file in root_dir.iterdir():
        if not file.is_file():
            continue
        if file.suffix != suffix:
            continue
        video_item = VItem(file = file)
        video_list.append(video_item)

    while len(video_list) > 0:
        found_pos = []
        remove_list = []
        for vitem in video_list:
            ret = re_index.search(vitem.file.name, vitem.search_pos)
            if ret is None:
                remove_list.append(vitem)
                continue
            (found, next_find) = ret.span()
            vitem.search_pos = next_find
            vitem.found_pos = found
            vitem.found_num = int(ret.group())
            found_pos.append(found)
        counter = collections.Counter(found_pos)
        for x in remove_list:
            video_list.remove(x)

        if len(counter) == 0:
            return None
        (best, count) = counter.most_common()[0]
        dist_index = set()
        remove_list = []
        for vitem in video_list:
            if vitem.found_pos != best:
                remove_list.append(vitem)
                continue
            dist_index.add(vitem.found_num)
        for x in remove_list:
            video_list.remove(x)
        if len(dist_index) == len(video_list):
            ret_list = list(map(lambda x: x.file, video_list))
            ret_list.sort()
            return ret_list
    return None


import sys, getopt

def main(name, argv):
    video_suffix = None
    sub_suffix = None
    try:
        opts, args = getopt.getopt(argv,"hv:s:",["video_suffix=","sub_suffix="])
    except getopt.GetoptError:
        print(name + " -v <video_suffix> -s <sub_suffix>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(name + " -v <video_suffix> -s <sub_suffix>")
            sys.exit()
        elif opt in ["-v", "--video_suffix"]:
            video_suffix = arg
        elif opt in ["-s", "--sub_suffix"]:
            sub_suffix = arg
    if video_suffix is None or sub_suffix is None:
        print(name + " -v <video_suffix> -s <sub_suffix>")
        sys.exit(2)
    video_list = process_video(Path("."), "." + video_suffix)
    sub_list = process_video(Path("."), "." + sub_suffix)
    if len(video_list) != len(sub_list):
        print("number of sub and video are not equal")

    for (video, sub) in zip(video_list, sub_list):
        sub.rename(video.stem + sub.suffix)
    print("%d files renamed" % len(sub_list))
    pass

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
