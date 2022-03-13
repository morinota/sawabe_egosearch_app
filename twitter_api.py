import requests
import pandas as pd
import re

from datetime import datetime

import emoji
import tweepy
from typing import List 
import os
import datetime

class SawabeTweetScraping:
    '''
    Twitter APIとのやり取りを管理するクラス
    '''
    def __init__(self) -> None:
        # 以下、APIキー
        ## Consumer key
        self.CK = '62NSImwWiQb0RHPjtaKmEjnRm'
        ## Consumer secret
        self.CT = 'l9EwSN4lKziY0sCrQOmeRJyfdnUaKwl1MvfsmHQjRRB66yP8ZP'
        ## Access token
        self.AT = '2485048094-2UGgmNQUKfmWfV4FVN1iiT1NiXonDuoV4iVy61m'
        ## Access token secret
        self.AS = 'gRU3TDbs3ukbdvG3XS7mC3on0zG6M026nqNErgBNQzly4'
        self.bearer_token = 'AAAAAAAAAAAAAAAAAAAAAH9DYAEAAAAApPFRDkkGa9LOyQnVJnQwPMX2y%2FY%3DaDcYTyoPfxwt1k1Yc7gnoYO2kWjBYGRtXoA4adjUHbCanIL9rj'

        # Twitterオブジェクトの生成
        self.auth = tweepy.OAuthHandler(self.CK, self.CT)
        self.auth.set_access_token(key=self.AT, secret=self.AS)
        self.api = tweepy.API(auth=self.auth, wait_on_rate_limit=True)


        # Twitter APIのURL
        self.search_url  = 'https://api.twitter.com/2/tweets/search/recent'

    def get_tweet_data(self)->List[dict]:
        '''
        澤部さんに関するツイートを取得するMethod.
        出力は、各ツイートがJson(Dict型)で格納されたList.
        '''
        # 検索Word
        self.search_words = ['澤部', 'さわべ', 'サワベ']

        # 検索クエリ
        self.queries = []
        for search_word in self.search_words:
            query_params = {'query': f'{search_word} -is:retweet', 'tweet.fields': 'author_id', 'max_results': 100}
            self.queries.append(query_params)

        # ヘッダー生成
        self.headers = {"Authorization": f"Bearer {self.bearer_token}"}
        
        # エンドポイントへの接続(=データのスクレイピング?)
        self.results = []
        for query_params in self.queries:
            has_next = True
            c = 0
            while has_next:
                response = requests.request("GET", self.search_url, headers=self.headers, params=query_params)
                if response.status_code != 200:
                    raise Exception(response.status_code, response.text)

                response_body = response.json()
                self.results += response_body['data']

                rate_limit = response.headers['x-rate-limit-remaining']
                print('Rate limit remaining: ' + rate_limit)

                c = c + 1
                has_next = ('next_token' in response_body['meta'].keys() and c < 300)

                # next_tokenがある場合は検索クエリに追加
                if has_next:
                    query_params['next_token'] = response_body['meta']['next_token']

        return self.results

    
    def create_data_frame(self):
        '''
        収集したツイートデータをpd.DataFrameに加工するmethod.
        '''
        self.df = pd.DataFrame(self.results)

        # ツイート中のURLを削除
        self.df['text'] = self.df['text'].apply(lambda x: re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', x))
        # ツイート中の絵文字を削除
        self.df['text'] = self.df['text'].apply(lambda x: ''.join(c for c in x if c not in emoji.UNICODE_EMOJI))
        return self.df

    
    def write_csv(self, path):
        '''
        収集したツイートデータをcsvファイルとしてはき出すmethod.
        '''
        self.df['text'].to_csv(path, index = False) 


def main():
    # instanceの生成
    twt = SawabeTweetScraping()
    # tweetデータの収集
    twt_data = twt.get_tweet_data() #->dict
    # print(len(twt_data))

    # データフレーム化・余分な文字列を除去
    twt.create_data_frame()
    # csv出力
    today = datetime.datetime.now()
    date = f'{today.year}{today.month}{today.day}'
    INPUT_DIR = r'C:\Users\Masat\デスクトップ_Instead\webアプリ開発\sawabe_egosearch_app'
    twt.write_csv(path=os.path.join(INPUT_DIR, f'sawabe_tweet_{date}.csv'))

# headers = create_headers(bearer_token)
# json_response = connect_to_endpoint(search_url, headers, query_params)

# data_frame = create_data_frame(json_response)
# write_csv(data_frame)

if __name__ == "__main__":
    main()
