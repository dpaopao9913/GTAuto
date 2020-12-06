import os
import lxml.html as lh
from lxml import etree
import requests
import sys

# How to use: 
#   ...?text=翻訳したい文字列&source=翻訳前言語&target=翻訳後言語
#   ex) ...?text=こんにちわ&source=ja&target=en
my_google_trans_api = "https://script.google.com/macros/s/AKfycbxqzqhZlbG6Wkko7vs988Kw-7n9mmQZerDjC2tCQ_ATwb2vJAU/exec"


def checkPath():
    print('Hello!')
    print('__name__ is', my_google_trans_api)
    print('getcwd:      ', os.getcwd())
    print('dirname:    ', os.path.dirname(__file__))
    print('outfilename:    ', output_sdlxliff_filename)

## <element attribute="attribute value">contents</element>
def checkXMLElement(et):
    print(et.tag)       ## element name
    print(et.attrib)    ## attribute name


## 機能：原文（source）を渡し、Google翻訳した訳文（target）を返す
## 入力：source（原文）
## 出力：OSと同じエンコードでデコード済みのs_after_rep（原文）r_after_rep（訳文）
def autoGoogleTranslation(source):
    # translation from En to Ja
    trans_url = my_google_trans_api + '?text=' + source + '&source=en&target=ja'
    r = requests.get(trans_url)  # 翻訳文章が返って来る
    #print('translation: ', r.text, '\n')

    # エンコードエラー処理用
    # 参考：https://qiita.com/butada/items/33db39ced989c2ebf644
    b1 = source.encode('gbk', "ignore")
    s_after = b1.decode('gbk')
    b2 = r.text.encode('gbk', "ignore")
    r_after = b2.decode('gbk')

    s_after_rep = s_after.replace('\n', ' ').replace(',', '、')
    r_after_rep = r_after.replace('\n', ' ')

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
        f_out = open(args[2], mode='w')
    except FileNotFoundError as err:
        print("ファイルが存在しないため、読み込めませんでした。")
        exit()
    except Exception as other:
        print("ファイルが読み込めませんでした。")
        exit()

    
    print("Input File: " + args[1])

    f_out.write("***ORIGINAL TEXT***,***TRANSLATION***\n")  # CSVのヘッダー定義
    ss_input = ''.join(f_in.readlines())
    
    tree = lh.fromstring(ss_input)
    list_lang_pair = []  # 翻訳の際に、1回翻訳したソースセグメントは2回目以降翻訳しないようにするための識別用タプル(原文,訳文)のリスト

    count = -1
    for s, t in zip(tree.xpath('//seg-source//mrk'), tree.xpath('//target//mrk')):
 
        count += 1
        #print('count= ' + str(count))
        print('line: ' + str(count) + ', ' + s.text_content() + ", " + t.text_content())

        # 原文があるかどうかチェック（念のため）
        if s.text_content() != '':
            print('原文あり')
        else:
            print('原文なし')

        # 翻訳があるかどうかチェック
        if t.text_content() != '':
            print('訳文あり')
            f_out.write(s.text_content().replace('\n', ' ') + "," + t.text_content().replace('\n', ' ') + "\n")
        else:
            print('訳文なし')

            ##########################################################################################################
            s_after_rep = ''
            r_after_rep = ''

            if len(list_lang_pair) == 0:  # リストに言語ペアがない場合、翻訳して(原文, 翻訳文)のタプルを保持

                print('はじめのリスト追加です。GoogleTranslationAPI が呼ばれました。')

                ############# 自動翻訳 ###########################################
                s_after_rep, r_after_rep = autoGoogleTranslation(s.text_content())
                #################################################################
                
                f_out.write(s_after_rep + "," + r_after_rep + "\n")

                list_lang_pair.append(tuple([s_after_rep, r_after_rep]))  
            else:

                isDuplicated = False  # リストに同じ原文があるかどうかチェック用
                list_index = -1       # リストに同じ原文がある場合のリストのインデックス

                for ii in range(len(list_lang_pair)):
                    isDuplicated = False if list_lang_pair[ii][0] != s.text_content() else True
                    #print(len(list_lang_pair), list_lang_pair[ii][0], isDuplicated)
                    if isDuplicated:
                        list_index = ii
                        break
             
                if isDuplicated:     # リストに対応する言語ペアのタプルがある場合、スキップ
                    print('言語ペアのリストの中に同一の原文を見つけました。翻訳をスキップします。')

                    f_out.write(list_lang_pair[list_index][0] + "," + list_lang_pair[list_index][1] + "\n")
                else:                # リストに対応する言語ペアのタプルがなし場合、翻訳して(原文, 翻訳文)のタプルを保持

                    print('GoogleTranslationAPI が呼ばれました。')

                    ############# 自動翻訳 ###########################################
                    s_after_rep, r_after_rep = autoGoogleTranslation(s.text_content())
                    #################################################################
                
                    f_out.write(s_after_rep + "," + r_after_rep + "\n")

                    list_lang_pair.append(tuple([s_after_rep, r_after_rep])) 
            ##########################################################################################################


        print('\n')


    f_in.close()
    f_out.close()
