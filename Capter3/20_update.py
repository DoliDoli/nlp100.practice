import json

uk = open("jawiki_uk.txt","w")

#Wikipedia記事のJSONファイルを読み込み，イギリスに関する記事本文を表示
#文字化け防止のためencode文を作成した
f = open("jawiki-country.json")
for line in f.readlines():
    jawiki_data = json.loads(line)
    if jawiki_data["title"] == u"イギリス":
        jawiki_uk_disguise =  jawiki_data["text"]
        uk.write(jawiki_uk_disguise.encode("utf-8"))

f.close()
uk.close()