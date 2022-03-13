import imp
from janome.tokenizer import Tokenizer 
from wordcloud import WordCloud
import pandas as pd
import os
import matplotlib.pyplot as plt
from typing import List
from tqdm import tqdm

INPUT_DIR = r'C:\Users\Masat\デスクトップ_Instead\webアプリ開発\twitter_API_sawabe'

def get_nouns(sentence:str, noun_list:List)->List:
    t = Tokenizer()
    for token in t.tokenize(sentence):
        split_token = token.part_of_speech.split(',')
        ## 名詞を抽出
        if split_token[0] == '名詞' or split_token[0] == '形容詞':
            # surface属性が表層形
            # noun_list.append(token.surface)
            noun_list.append(token.base_form)

    return noun_list

def remove_sawabe_haraichi(noun_list:List)->List:
    # 「サワベ」や「ハライチ」を単語リストから取り除く.
    remove_target = ['澤', '部', 'さわべ', 'サワベ', 'ハライチ', 'はらいち', 'ハラ', 'イチ', 'さん', 'くん', 'ちゃん']
    noun_list = [element for element in noun_list if element not in remove_target]
    # 一文字の単語を取り除く
    noun_list = [element for element in noun_list if len(element)>1]
    return noun_list

def create_word_cloud(noun_list):
    ## 名詞リストの要素を空白区切りにする(word_cloudの仕様)
    noun_space = ' '.join(map(str, noun_list))
    ## word cloudの設定(フォントの設定)
    wc = WordCloud(background_color="white", font_path=r"C:/WINDOWS/Fonts/msgothic.ttc", width=300,height=300)
    wc.generate(noun_space)
    ## 出力画像の大きさの指定
    plt.figure(figsize=(5,5))
    ## 目盛りの削除
    plt.tick_params(labelbottom=False,
                    labelleft=False,
                    labelright=False,
                    labeltop=False,
                   length=0)
    ## word cloudの表示
    plt.imshow(wc)
    plt.show()
    plt.savefig(os.path.join(INPUT_DIR, 'wordcrowd_sawabe.png'), dpi=300)

def all_process_get_wordCrowd():
    # データimport
    df = pd.read_csv(os.path.join(INPUT_DIR, 'sawabe_tweet_2022226.csv'), header=0)
    noun_list_in_tweet = []
    # 各Tweetを繰り返し処理で形態素解析していく.
    for sentence in tqdm(list(df['text'])):
        noun_list_in_tweet = get_nouns(sentence=sentence, noun_list=noun_list_in_tweet)
    # ノイズや見出し語の処理
    noun_list_in_tweet = remove_sawabe_haraichi(noun_list_in_tweet)
    # ワードクラウドの作成
    create_word_cloud(noun_list_in_tweet)

if __name__ == "__main__":
    all_process_get_wordCrowd()