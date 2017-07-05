from rec_categorize import Categories,RecordedFile
category = Categories(moemoe_tokyo_years=3,additional_data=["金曜ロードSHOW","ヘボット","孤独のグルメ"])

recs = []

for line in open("testdata.txt"):
    recs.append(RecordedFile(line))
for rec in recs:
    category.select_category(rec)

category.add_category_from_files(recs)
print(list(sorted(category.data)))

for rec in recs:
    category.select_category(rec)
    assert isinstance(rec,RecordedFile)
    if 0 or not rec.category:
        print(rec) #IGNORED Files

print(list(sorted(list(set(rec.category for rec in recs if rec.category)))))
