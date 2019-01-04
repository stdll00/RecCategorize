#!/usr/bin/env python3
"""
https://github.com/stdll00/RecCategorize.git


--setup--
pip3 install requests
chomod +x rec_categorize.py
"""

import os, os.path
import unicodedata
import shutil
import json
import difflib
import datetime
import collections
import string
import time
import requests


class RecordedFile:
    VIDEO_EXTENSIONS = ["ts", "m2ts", "mp4", "webm", "avi", "m4p", "m4v", "mpeg", "mpeg2", "testdir"]

    def __init__(self, filepath):
        # assert os.path.exists(filename)
        assert filepath.split(".")[-1] in self.VIDEO_EXTENSIONS
        self.category = None
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.search_name = self.processing_searchname(
            unicodedata.normalize(
                "NFKC",
                self.filename.split("]")[-1].split(".")[0]
            )
        )
        assert isinstance(self.search_name, str)

    def movefile(self, target_dir, testmode=False):
        if self.category:
            move_to = os.path.join(target_dir, self.category)
            if testmode:
                print(self.filename, ">>", move_to)
                return
            if not os.path.exists(move_to):
                os.mkdir(move_to)
            if os.path.exists(os.path.join(move_to, self.filename)):
                print("same file Already Exists... ", self.filename)
                # TODO move to trash?
                return
            shutil.move(self.filepath, move_to)
        else:
            print("IGNORED : ", self.filename)

    def symlink(self, target_dir, testmode=False):
        if self.category:
            move_to = os.path.join(target_dir, self.category)
            if testmode:
                print(self.filename, ">>", move_to)
                return
            if not os.path.exists(move_to):
                os.mkdir(move_to)
            if os.path.exists(os.path.join(move_to, self.filename)):
                print("same file Already Exists... ", self.filename)
                return
            os.symlink(self.filepath, os.path.join(move_to, self.filename))

    @staticmethod
    def escape_filename(filename):
        filename = filename.replace("?", "？")
        filename = filename.replace("/", "／")

        filename = filename.replace(":", "")
        filename = filename.replace("|", "")

        filename = filename.replace("*", "＊")
        filename = filename.replace(".", "")
        filename = filename.replace(",", "")
        filename = filename.replace(";", "")
        return filename

    @staticmethod
    def processing_searchname(searchname):
        for i, s in enumerate(searchname):
            if i == 0:
                if s in "「『":
                    return RecordedFile.processing_searchname(searchname[1:])
                continue

            if s in " 「『【(」』":
                if i != len(searchname) - 1 and \
                                searchname[i - 1] in string.ascii_letters and \
                                searchname[i + 1] in string.ascii_letters:
                    continue
                else:
                    return searchname[:i]
            if s in "123456789" and i >= 2:
                return searchname[:i]
        return RecordedFile.escape_filename(searchname)

    def __repr__(self):
        if not self.category:
            return self.search_name + ":" + self.filename
        return "!" + self.category + ":" + self.filename


class Categories:
    def __init__(self, targetpath=None, moemoe_tokyo_years=0, additional_data=[]):
        self.data = [] + list(additional_data)
        if targetpath:
            self.data.extend(file for file in os.listdir(targetpath) if file[0] != ".")

        if moemoe_tokyo_years:
            print("fetch data")
            for i in range(moemoe_tokyo_years):
                for title in self.get_moemoe_tokyo(datetime.datetime.today().year - i):
                    self.data.append(
                        RecordedFile.processing_searchname(title
                                                           ))

        self.reduce_category()

    @staticmethod
    def get_moemoe_tokyo(year):
        url = "http://api.moemoe.tokyo/anime/v1/master/{}".format(year)
        r = requests.get(url)
        for anime in json.loads(r.text):
            yield unicodedata.normalize("NFKC", anime["title"]).split("(")[0]

    def select_category(self, recorded_file):
        assert isinstance(recorded_file, RecordedFile)
        for category in self.data:
            if category in recorded_file.search_name:  # TODO 先頭一致に変えるべき?
                recorded_file.category = category
                return
        result = difflib.get_close_matches(recorded_file.search_name, self.data, cutoff=0.8)
        if not result:
            return
        recorded_file.category = result[0]

    @staticmethod
    def create_category_from_filename_(iter_of_rec, border_count=3):
        counter = collections.Counter(rec.search_name for rec in iter_of_rec)
        return [key for key, count in counter.items() if count >= border_count]

    def add_category_from_files(self, recs, border_count=3, not_categorized_only=True):
        self.data.extend(self.create_category_from_filename_(
            [rec for rec in recs if not not_categorized_only or not rec.category]
            , border_count))
        self.reduce_category()

    def reduce_category(self):
        for category in self.data:
            if len(category) <= 1:
                self.data.remove(category)
        # TODO 部分文字列になっているときに削除
        remove_indexs = []
        for category1 in self.data:
            for i, category2 in enumerate(self.data):
                if len(category1) < len(category2):
                    if category1 == category2[:len(category1)]:
                        remove_indexs.append(i)
        for i in sorted(remove_indexs, reverse=True):
            self.data.pop(i)


def main(file_dir, target_dir, execute=False, link=False):
    category = Categories(targetpath=target_dir, moemoe_tokyo_years=3)
    recs = []

    # Recorded files
    for filename in os.listdir(file_dir):
        if filename[0] == ".":
            continue
        filepath = os.path.join(file_dir, filename)
        if os.path.isfile(filepath):
            recs.append(RecordedFile(filepath))

    for rec in recs:
        category.select_category(rec)
    category.add_category_from_files(recs)
    for rec in recs:
        category.select_category(rec)

    if not execute:
        for rec in recs:
            assert isinstance(rec, RecordedFile)
            rec.movefile(target_dir=target_dir, testmode=True)

    _time = time.time()
    if execute or input("EXECUTE? (y,N) :") == "y":
        for i, rec in enumerate(recs):
            assert isinstance(rec, RecordedFile)
            print("\r{}/{}    {} left. ".format(i, len(recs), int(time.time() - _time), ), end="")
            if link:
                rec.symlink(target_dir=target_dir, testmode=False)
            if not link:
                rec.movefile(target_dir=target_dir, testmode=False)

    print("END")


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs=2, help="file source  and directory that files move to ")
    parser.add_argument("-y", "--execute", help="execute without confirm",
                        action="store_true")
    parser.add_argument("-d", "--dupedelete", help="dupedelte",
                        action="store_false")

    parser.add_argument("-l", "--link", help="symlink",
                        action="store_false")

    args = parser.parse_args()

    main(args.dir[0], args.dir[1], execute=args.execute, link=args.link)
