# -*- coding: utf-8 -*-
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import requests
import MeCab as mc
from os import path


def get_analysis_mecab_words(text):
    st_text = text.encode('utf-8')
    tagger = mc.Tagger('-Ochasen')
    words = tagger.parse(st_text)

    outputs = []
    for w in words.split('\n'):
        word = w.split('\t')
        if word[0] == 'EOS':
            break

        word_type = word[3].split('-')[0]
        if word_type in ['形容詞', '動詞', '名詞', '副詞']:
            outputs.append(word[0])

    return outputs


def get_keywords(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    text = soup.body.section.get_text().replace('\n', '').replace('\t', '')
    outputs = get_analysis_mecab_words(text)
    return ' '.join(outputs).decode('utf-8')


def view_image(word_cloud):
    word_cloud.to_file(path.join(path.dirname(__file__), 'sample.png'))
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.figure(figsize=(15, 12))
    plt.show()


if __name__ == '__main__':
    url = 'https://qiita.com/kobaboy/items/46ff9f19b9ea5638fa8e'
    keywords = get_keywords(url)

    stop_words = [u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して', \
                  u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した', u'思う', \
                  u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て', u'に', u'を', u'は', u'の', u'が', u'と', u'た', u'し', u'で', \
                  u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'']

    word_cloud = WordCloud(
        font_path='/System/Library/Fonts/ヒラギノ明朝 ProN.ttc',
        background_color="white",
        width=900,
        height=500,
        stopwords=set(stop_words)).generate(keywords)

    view_image(word_cloud)
