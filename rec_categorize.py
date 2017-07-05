#! /usr/bin python3

import os, os.path
import unicodedata
import shutil
import json
import difflib
import datetime
import collections
import string

import requests


class RecordedFile:
    VIDEO_EXTENSIONS = ["ts", "m2ts", "mp4", "webm", "avi", "m4p", "m4v", "mpeg", "mpeg2"]

    def __init__(self, filename):
        # assert os.path.exists(filename)
        assert filename.split(".")[-1] in self.VIDEO_EXTENSIONS
        self.category = None
        self.filename = filename
        self.filename = os.path.basename(filename)
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
                print(self.filename, move_to)
                return
            if not os.path.exists(move_to):
                os.mkdir(move_to)
            shutil.move(self.filename, move_to)

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
    def __init__(self, targetpath=None, moemoe_tokyo_years=3, additional_data=[]):
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
            if category in recorded_file.search_name:
                recorded_file.category = category
                return
        result = difflib.get_close_matches(recorded_file.search_name, self.data)
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


def main(file_dir, target_dir, execute=False):
    category = Categories(target_dir=target_dir, moemoe_tokyo=3)
    recs = []

    #Recorded files
    for filename in os.listdir(file_dir):
        if filename[0] == ".":
            continue
        recs.append(RecordedFile(filename))

    for rec in recs:
        category.select_category(rec)
    category.add_category_from_files(recs)
    for rec in recs:
        category.select_category(rec)


    if not execute:
        for rec in recs:
            assert isinstance(rec, RecordedFile)
            rec.movefile(target_dir=target_dir, testmode=True)

    if execute or input("EXECUTE? (y,N) :") == "y":
        for rec in recs:
            rec.movefile(target_dir=target_dir, testmode=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print("USAGE  argv 1:file_dir argv2:target_dir")
        exit(-1)
    main(sys.argv[1],sys.argv[2])