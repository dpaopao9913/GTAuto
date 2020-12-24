import os
from lxml import etree
import requests
import sys

# How to use: 
#   ...?text=翻訳したい文字列&source=翻訳前言語&target=翻訳後言語
#   ex) ...?text=こんにちわ&source=ja&target=en
my_google_trans_api = "https://script.google.com/macros/s/AKfycbxqzqhZlbG6Wkko7vs988Kw-7n9mmQZerDjC2tCQ_ATwb2vJAU/exec"


## 機能：原文（source）を渡し、Google翻訳した訳文（target）を返す
## 入力：source（原文）
## 出力：原文と訳文のペア（CSV形式で行ごと出力できるようにフォーマットを整える）
def autoGoogleTranslation(source):
    # translation from En to Ja
    trans_url = my_google_trans_api + '?text=' + source + '&source=en&target=ja'
    r = requests.get(trans_url)  # 翻訳文章が返って来る
    #print('translation: ', r.text, '\n')

    s_after_rep = source.replace('\n', ' ').replace(',', '、')
    r_after_rep = r.text.replace('\n', ' ').replace(',', '、')

    return s_after_rep, r_after_rep


if __name__ == '__main__':

    args = sys.argv
 
    # 引数チェック
    if len(args) != 3:
        print('使い方が間違っています。引数の個数: ' + str(len(args)))
        print('usage: <*.py> <input_filename> <output_filename>')
        print('yours: ')  
        for i in range(len(args)):
            print('args[' + i + ']= ' + str(args[i]))
        exit()

    # 必要なファイルを開く
    try:
        f_in  = open(args[1], encoding='utf-8', mode='r')
        f_out = open(args[2], encoding='utf-8', mode='w')
    except FileNotFoundError as err:
        print("ファイルが存在しないため、読み込めませんでした。")
        exit()
    except Exception as other:
        print("ファイルが読み込めませんでした。")
        exit()

    
    print("Input File: " + args[1])

    ss_input = ''.join(f_in.readlines())   
    tree = etree.fromstring(ss_input)

    # lxml.etreeで名前空間を指定してパースする
    # 参考: トホホな疑問(13) Python、lxml、デフォルト名前空間とXPath（https://jhalfmoon.com/dbc/2019/10/20/%E3%83%88%E3%83%9B%E3%83%9B%E3%81%AA%E7%96%91%E5%95%8F13-python%E3%80%81lxml%E3%80%81%E3%83%87%E3%83%95%E3%82%A9%E3%83%AB%E3%83%88%E5%90%8D%E5%89%8D%E7%A9%BA%E9%96%93%E3%81%A8xpath/） 
    mynsmap = dict()
    mynsmap['x'] = tree.nsmap[None]
    
    #print(mynsmap)
    #print(tree)
    #print(len(tree))

    list_lang_pair = []  # 翻訳の際に、1回翻訳したソースセグメントは2回目以降翻訳しないようにするための識別用タプル(原文,訳文)のリスト

    count = 0
    for s, t in zip(tree.xpath('//x:seg-source//x:mrk', namespaces=mynsmap), tree.xpath('//x:target//x:mrk', namespaces=mynsmap)):
 
        count += 1

        # itertext(self, tag=None, with_tail=True, *tags) を使ってサブツリー内すべてのテキストを抜き出す
        # 参考: https://lxml.de/api/lxml.etree._Element-class.html

        s_temp = []
        t_temp = []
        for ss in s.itertext():
            s_temp.append(ss)
        for tt in t.itertext():
            t_temp.append(tt)
        
        s_all_text = ' '.join(s_temp).replace('&', ' and ')  # convert "&" to "and"
        t_all_text = ' '.join(t_temp)

        print('line: ' + str(count) + ', ' + s_all_text + ", " + t_all_text)

        # 原文があるかどうかチェック（念のため）
        if s_all_text != '':
            print('原文あり')
        else:
            print('原文なし')

        # 翻訳があるかどうかチェック
        if t_all_text != '':
            print('訳文あり')
        else:
            print('訳文なし')

            ##########################################################################################################
            s_after_rep = ''
            r_after_rep = ''

            if len(list_lang_pair) == 0:  # リストに言語ペアがない場合、翻訳して(原文, 翻訳文)のタプルを保持

                print('はじめのリスト追加です。GoogleTranslationAPI が呼ばれました。')

                ############# 自動翻訳 ###########################################
                s_after_rep, r_after_rep = autoGoogleTranslation(s_all_text)
                #################################################################
                
                ############# 出力用ツリーの当該箇所に訳文を挿入 ####################
                t.text = r_after_rep
                list_lang_pair.append(tuple([s_after_rep, r_after_rep])) 
                #################################################################
                 
            else:

                isDuplicated = False  # リストに同じ原文があるかどうかチェック用
                list_index = -1       # リストに同じ原文がある場合のリストのインデックス

                for ii in range(len(list_lang_pair)):
                    isDuplicated = False if list_lang_pair[ii][0] != s_all_text.replace('\n', ' ').replace(',', '、') else True
                    print(len(list_lang_pair), list_lang_pair[ii][0], isDuplicated)
                    if isDuplicated:
                        list_index = ii
                        break
             
                if isDuplicated:     # リストに対応する言語ペアのタプルがある場合、スキップ
                    print('言語ペアのリストの中に同一の原文を見つけました。翻訳をスキップします。')

                    ############# 出力用ツリーの当該箇所に訳文を挿入 ####################
                    t.text = list_lang_pair[list_index][1] 
                    #################################################################

                else:                # リストに対応する言語ペアのタプルがなし場合、翻訳して(原文, 翻訳文)のタプルを保持

                    print('GoogleTranslationAPI が呼ばれました。')

                    ############# 自動翻訳 ###########################################
                    s_after_rep, r_after_rep = autoGoogleTranslation(s_all_text)
                    #################################################################
                
                    ############# 出力用ツリーの当該箇所に訳文を挿入 ####################
                    t.text = r_after_rep
                    list_lang_pair.append(tuple([s_after_rep, r_after_rep]))
                    #################################################################

            ##########################################################################################################


        print('\n')


    ############# 出力用ツリーを出力用sdlxliffファイルへ出力 ############
    f_out.write(etree.tostring(tree, encoding='utf-8', method="xml", xml_declaration=True).decode('utf-8'))
    #################################################################

    f_in.close()
    f_out.close()
