<!-- screenshots -->
<img src="https://d-paopao.com/wp-content/uploads/2020/12/GTAuto_output00.jpg" alt="自動翻訳の出力ファイル" />

<img src="https://d-paopao.com/wp-content/uploads/2020/12/20201215_google_translate_api-result.png" alt="auto_google_translation_from_trados_sdlxliff" />


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#googletranslationauto">GoogleTranslationAuto</a>
    </li>
    <li>
      <a href="#package">Package</a>
    </li>
    <li>
      <a href="#prerequisite">Prerequisite</a>
    </li>
    <li>
      <a href="#setup">Setup</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#further-options">Further options</a></li>
      </ul>
    </li>
    <li>
      <a href="#license">License</a>
    </li>
    <li>
      <a href="#contributor">Contributor</a>
    </li>
    <li>
      <a href="#reference">Reference</a>
    </li>
  </ol>
</details>


# GoogleTranslationAuto

Automated machine translation using Google translation API from .sdlxliff file and output the translation as .csv/.sdlxliff file.
翻訳支援ソフトTrados専用形式の.sdlxliffファイルから、原文を自動抽出して、Google自動翻訳した後、訳文をcsvファイルまたはsdlxliffファイルとして出力するプログラム。


# Package

- sdlxliff_sample/Harassment_NA_Managers_S01_Introduction SM.xlf.sdlxliff <br>
  .sdlxliff sample file
  
- AllSdlxliffFilename.csv <br>
  sdlxliff file name list for input
  
- GTAuto_ToCSV.py <br>
  Program (input: sdlxliff, output: <b>csv</b>) <br>
  Automated machine translation using Google translation API from .sdlxliff file and output the translation as <b>.csv</b> file.
  
- GTAuto_ToSdlxliff.py <br>
  Program (input: sdlxliff, output: <b>sdlxliff</b>) <br>
  Automated machine translation using Google translation API from .sdlxliff file and output the translation as <b>.sdlxliff</b> file.
  
- pyBatchTest01.bat <br>
  Batch file for "GTAuto_ToCSV.py"
  
- pyBatchTest02.bat <br>
  Batch file for "GTAuto_ToSdlxliff.py"
  

# Prerequisite

- Windows 10 x64

- Anaconda 5.2.0 (conda 4.9.2)

- Python 3.8.5

- SDL Trados Studio 2019 (optional)


# Setup

requests/lxml packages can be installed by (if necessary): 

```sh
$ conda install requests
```

```sh
$ conda install lxml
```


# Usage

Run `pyBatchTest01.bat` or `pyBatchTest02.bat` after updating input file names in `AllSdlxliffFilename.csv`.


## Further options

- How to change translation language pair ? <br>
  Default language pair is "English -> Japanse". If you have to change the language pair, you can change the following line in `pyBatchTest01.bat` and `pyBatchTest02.bat`: 
  
  ```python
  trans_url = my_google_trans_api + '?text=' + source + '&source=en&target=ja'
  ```
    
  If you want to use "Japanse -> English" pair, you can change as below:
  
  ```python
  trans_url = my_google_trans_api + '?text=' + source + '&source=ja&target=en'
  ```
  
  If you want to use "Chinese -> Japanese" pair, you can change as below:
  
  ```python
  trans_url = my_google_trans_api + '?text=' + source + '&source=zh-CN&target=ja'
  ```
  
  *Note: you can change any source and target langage code as you like.


# License

This software is released under the MIT License, see LICENSE.


# Contributor

[d_paopao9913](https://twitter.com/d_paopao9913)


# Reference

- https://d-paopao.com/trados_auto_translation/
