from rec_categorize import Categories,RecordedFile
category = Categories(moemoe_tokyo_years=3,additional_data=["金曜ロードSHOW","ヘボット","孤独のグルメ"])

recs = []

for line in open("testdata.txt"):
    recs.append(RecordedFile(line.rstrip()))
for rec in recs:
    category.select_category(rec)

category.add_category_from_files(recs)

for rec in recs:
    category.select_category(rec)
    assert isinstance(rec,RecordedFile)
    print(rec.category," "*(50-len(str(rec.category))),rec.filename)


