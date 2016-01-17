import unittest
import random
from ani_sub import *
from pathlib import Path, PurePath

class FakeFile:
    def __init__(self, name):
        self.name = name


def extract_case(input):
    video_list = []
    subtitle_list = []
    match_list = []
    subtitle_video_map = {}
    current_mode = None
    with input.open(mode="r", encoding="utf-8") as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = line.strip()
            if len(line) == 0:
                continue

            if line.startswith("#"):
                line.split(":")
                current_mode = line
                continue

            if current_mode == "#video":
                video_list.append(line)
            elif current_mode == "#subtitle":
                subtitle_list.append(line)
            elif current_mode == "#match":
                match_list.append(line)

    assert(len(subtitle_list) == len(match_list))
    for (x,y) in zip(subtitle_list, match_list):
        subtitle_video_map[x] = y
        assert(y in video_list)

    random.shuffle(video_list)
    random.shuffle(subtitle_list)
    video_list = list(map(lambda x: VItem(FakeFile(x)), video_list))
    subtitle_list = list(map(lambda x: VItem(FakeFile(x)), subtitle_list))

    return video_list, subtitle_list, subtitle_video_map


class Test(unittest.TestCase):
    def test(self):
        test_dir = Path("test")
        for case in test_dir.iterdir():
            if not case.is_file():
                continue
            (video, sub, match) = extract_case(case)
            video = process_file_list(video)
            sub = process_file_list(sub)
            self.assertEqual(len(video), len(sub), "Numbers of extracted files are different")

            for (v,s) in zip(video, sub):
                self.assertEqual(v.name, match[s.name], "Matched video is incorrect")

if __name__ == '__main__':
    unittest.main()
