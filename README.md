# dlSubscanStakingRewardsHistory
PySimpleGUIとSubscanAPIを使用してReward&amp;Slashのデータをcsvファイルで保存するGUIアプリ

[![](https://img.shields.io/badge/poetry-1.4.1-blue)](https://pypi.org/project/poetry/1.4.1/) [![](https://img.shields.io/badge/license-MIT-blue)](https://github.com/opensource-jp/licenses/blob/main/MIT/MIT.md) 

## 目次
- [概要](#概要)
- [取得対象のTokenとSubscanAPI情報](#取得対象のTokenとSubscanAPI情報)
  - [注意事項1](#注意事項1)
- [サンプル](#サンプル)
  - [注意事項2](#注意事項2)
  - [起動画面](#起動画面)
  - [履歴タイプ：Reward&Slash](#履歴タイプ：Reward&Slash)
  - [履歴タイプ：CryptactCustom](#履歴タイプ：CryptactCustom)
- [使い方](#使い方)
  - [パッケージインストール](#パッケージインストール)
    - [開発用環境の構築](#開発用環境の構築)
  - [SubscanAPIの設定](#SubscanAPIの設定)
  - [main画面操作実行](#main画面操作実行)
    - [画面の名称と詳細](#画面の名称と詳細)
  - [コマンド実行](#コマンド実行)
- [その他](#その他)
  - [Cryptactカスタムファイル(ステーキング報酬)について](#Cryptactカスタムファイル(ステーキング報酬)について)
  - [構造](#構造)
    - [パッケージ図](#パッケージ図)
    - [クラス図](#クラス図)

## 概要
PySimpleGUIとSubscanAPIを使用して下記形式のデータをcsvファイルで保存します。
* Reward&Slashの取引履歴(Download all data)  
* Cryptactカスタムファイル(ステーキング報酬)  

### 取得対象のTokenとSubscanAPI情報
StakingRewardsは[API Endpoint](https://support.subscan.io/#api-endpoints)の仕様に合わせてトークン毎に下記`Request URL`を指定して取得します。
| Token | API         | Request URL     | module_id    | event_id | 
| ----- | ----------- | --------------- | ------------ | -------- | 
| DOT   | V2 API      | reward-slash-v2 | Staking      | Reward   | 
| KSM   | V2 API      | reward-slash-v2 | Staking      | Reward   | 
| ASTR  | Staking API | reward-slash    | dappsstaking | Reward   | 

### 注意事項1
* 特定のアカウントで受信データの確認をできることは確認していますが、必ずしも期待されたデータを取得することは保証しません。
* 本コードを実行したこと、参考にしたことによって被るあらゆる損害について責任を負いかねますのでご注意ください。
* Subscanの仕様やクリプタクトのデータフォーマットは変わることがありますので、最新の情報を確認してください。
* アプリを使用する際は後述する設定画面よりSubscanAPI情報を設定してください。
* 取引履歴は取引状況に依存します。取得したデータは目的のデータを取得できていること、トランザクションデータを参照して誤りがないことを必ず確認してください。
* サポートするNetworkはPolkadot,Kusama,Astarのみです。  
  他のNetworkを指定した場合正しく取得できずにエラーになります。  
  (参考:[API Endpoints](https://support.subscan.io/#api-endpoints))  

## サンプル
Docs記載の[アドレス](https://polkadot.subscan.io/reward?address=1REAJ1k691g5Eqqg9gL7vvZCBG7FCCZ8zgQkZWd4va5ESih&role=account)で取得したReward&Slashを例に示します。(2022/06/05時点) 
### 注意事項2
* 前提として、アプリ上で表示されるデータはSubscan Expoloerで表示されるStakingReward(Value)とは異なります。
* 全てのアカウントに当てはまる訳ではありませんが、Valueは桁数調整されて表示されています。
* 本コードではReward&Slashの取引履歴(Download all data)に合わせていますので、確認する際はそちらと比較してください。

### 起動画面
![image1](./png/dlSubscanStakingRewardsHistory_startup.png)  

### 履歴タイプ：Reward&Slash
![image1](./png/dlSubscanStakingRewardsHistory_Reward&Slash.png)
[DLしたcsvファイル例](./csv_sample/1REAJ1k691g5Eqqg9gL7vvZCBG7FCCZ8zgQkZWd4va5ESih_Reward&Slash_300_20220605.csv)

### 履歴タイプ：CryptactCustom
![image1](./png/dlSubscanStakingRewardsHistory_CryptactCustom.png)
[DLしたcsvファイル例](./csv_sample/1REAJ1k691g5Eqqg9gL7vvZCBG7FCCZ8zgQkZWd4va5ESih_CryptactCustom_300_20220605.csv)

## 使い方
※静的解析ツールをサポートする開発環境を使用する場合は開発用環境の構築を参照してください。
### パッケージインストール

**venv**や**pyenv**等で仮想環境を作成して下記コマンドを実行してください。
```zsh
pip install -r requirements.txt
```

poetryを使用している場合は下記コマンドを実行してください。  
開発環境を使用する場合は「開発用環境の構築」を参照してください。
```zsh
poetry install --no-dev
```

### 開発用環境の構築
開発環境では以下の静的解析ツールに対応しています。
* [isort](https://pypi.org/project/isort/): import文の自動整理
* [black](https://pypi.org/project/black/): Python向けのコードフォーマッター(PEP8準拠)
* [flake8](https://pypi.org/project/flake8/): 文法チェック
* [mypy](https://pypi.org/project/mypy/): 型アノテーションによる型チェック
* [pytest](https://pypi.org/project/pytest/): Python向けに作成された単体テストを書くためのフレームワーク

開発環境を構築する場合は以下を実行してください。
```zsh
poetry install
```

静的解析ツールの使用方法(コマンド)
```zsh
poetry run isort src tests
poetry run black src tests
poetry run flake8 src tests
poetry run mypy src tests
poetry run pytest -s -vv --cov=. --cov-branch --cov-report=html
```

### SubscanAPIの設定  

アプリ起動後、設定ボタンよりSubscanAPI設定画面を起動し、
APIキー、アドレス、小数点調整値、有効数字桁数を設定してください。  
各設定値は最初の起動画面（以降main画面)で設定したトークン情報に紐づいて表示されます。(詳細は後述)
なお、値を変更した場合は正常に動作しませんのでご注意ください。

![image2](./png/dlSubscanStakingRewardsHistory_setting.png)  

**＜補足＞**  
APIキーはHTTP Request Header情報(```X-API-Key```)で使用しますが、未指定でも値は取得できます。    
ただし、ResponseデータはRate Limiting(参考:[Global Conventions](https://support.subscan.io/#global-conventions))に依存します。  
取得件数に大きい値で指定すると「```429 Too Many Requests```」となり、正しく動作しないことがあリます。利用する際はAPIキーの取得をお願いします。  


### main画面操作実行
#### 画面の名称と詳細
以下ではDocs記載のアドレスを例にして画面の名称(PySimpleGUIモジュールのクラス)ついて説明します。    
PySimpleGUIモジュールのクラスの詳細についてはPySimpleGUIの[ELEMENT AND FUNCTION CALL REFERENCE](https://pysimplegui.readthedocs.io/en/latest/call%20reference/#element-and-function-call-reference)を参照してください。  

![image1](./png/dlSubscanStakingRewardsHistory_Reward&Slash.png)  

**1. 使い方(Button Element)**  
本README.mdを表示するPopUpを表示します。  

**2. 取得対象(Input Element + Spin Element)**  
取得するトークンを選択します。  
トークンはDOT,KSM,ASTRに対応し、```config.toml```の```[SubscanAPI_info]``` ```token_list```で定義します。

**3. 履歴タイプ(Input Element + Spin Element)**  
```Reward&Slash```と```CryptactCustom```の2タイプから選択します。  
```CryptactCustom```を実行する場合は[カスタムファイルの作成方法 / 2.10.ステーキングによる報酬](https://support.cryptact.com/hc/ja/articles/360002571312-%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E4%BD%9C%E6%88%90%E6%96%B9%E6%B3%95#menu210)を参照し、```[cryptact_info]```の```action```,```price```,```counter```,```fee```,```feeccy```,```source_dot/ksm/astr```,```base_dot/ksm/astr```を設定してください。(処理については後述)

**4. 件数(Input Element)**  
取得する件数を入力します。  
入力する値は正の整数とし、履歴より大きい値を入力した場合は上限値に丸めます。

**5. ソートタイプ(Input Element + Spin Element)**  
昇順と降順を選択し、取得結果のデータを並び替えます。

**6. 履歴取得(Button Element)**  
SubscanAPIでHTTP Requestを送信し、受信データを履歴タイプの指定で表形式で表示します

**7. クリア(Button Element)**  
Input Element,Text Elementの表示をクリア(値を空にする)し、非表示にします。

**8. csvファイル保存(Button Element)**  
ファイル保存のPopUpを表示し、Save as指定で指定のファイル名で受信データをcsvファイル形式で保存します。  
ファイル名は```入力したテキスト+.csv```となります。

**9. 設定(Button Element)**  
SubscanAPI設定画面を表示します。  
表示される内容は「1. 取得対象」から決定します。

**10. テーブル初期化(Button Element)**  
「14. テーブル」で表示されるテーブルを初期化します。  
「3. 履歴タイプ」を変更する場合は都度テーブル初期化ボタンを押下してください。(「9. 設定」ボタンを押下しても同様の処理となります。」)  
テーブルの初期化が必要な理由はPySimpleGUIのTableクラスの仕様で値の更新をするためにはwindowsインスタンス作成時にTableインスタンスを作成する必要があるためです。  
また、コンストラクタとして指定する引数にはテーブルの幅、列数、行数、等を指定する必要があるため、トークン毎に設定されたテーブルの要素情報を指定して初期化します。

**11. 取得結果(Text Element)**  
SubscanAPIのResponseデータを表示します。

**12. ファイル保存先(Text Element)**  
「7. csvファイル保存」で指定したパスを表示します。

**13. テーブル表示形式(Text Element)**
「2. 履歴タイプ」で指定した形式を表示します。

**14. テーブル(Column Element + Table Element)**  
「5. 履歴取得」で受信したデータを表示します。データはDataFrameオブジェクトで作成します。  
テーブルのヘッダーはconfig.tomlの```[SubscanAPI_info]```  ```reward_slash_data_header_dot/_ksm/_astr```から作成します。  
テーブルの値(pandas.DataFrame.values)はconfig.tomlの```[SubscanAPI_info]``` ```reward_slash_data_dot/_ksm/_astr```の値(list型)から作成します。 

**15. 選択したテーブルの値(Text Element + InputText Element)**  
「14. テーブル」で選択した値を表示します。  
値はコピー可能な形式にするためInputText Elementで作成します。

### コマンド実行
main.pyを実行するとmain画面が起動します。
```zsh
cd src && python main.py
```

Poetryを使用する場合は以下を実行してください。
```zsh
cd src && poetry run python main.py
```

もしくは以下コマンドで仮想環境の有効化して実行してください。

仮想環境の有効化
```zsh
poetry shell && cd src && python main.py
```

仮想環境の無効化
```zsh
exit
```

## その他
### Cryptactカスタムファイル(ステーキング報酬)について
[カスタムファイルの作成方法 / 2.10.ステーキングによる報酬](https://support.cryptact.com/hc/ja/articles/360002571312-%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E4%BD%9C%E6%88%90%E6%96%B9%E6%B3%95#menu210)の仕様に基づきデータを作成します。
* Cryptactカスタムファイル用のデータはヘッダーと行データで構成されます。ヘッダーはconfig.tomlの```[cryptact_info]
cryptact_custom_header```の値(list型)から作成します。行データは可変値(`block_timestamp`,`amount`,`event_index`)と固定値(`[cryptact_info]`)を合わせたリストで作成します。
* `block_timestamp`はそのままではUNIX時間のため`fromtimestamp()`でローカル時間に変換します。
* 日時情報はクリプタクトの指定に合わせるためフォーマットを指定して文字列に変換します。
* `amount`はそのままでは実際の報酬量と一致しないためSubscanAPI設定画面で設定する小数点調整値(```[SubscanAPI_info]``` ```display_digit_dot/ksw/astr```)を有効数字桁数(```[SubscanAPI_info]``` ```adjust_value_dot/ksw/astr```)を使用して調整します。

### 構造
#### パッケージ図
![パッケージ図](http://www.plantuml.com/plantuml/proxy?src=https://gist.githubusercontent.com/7rikazhexde/b2d9e0dc0ba65489fcc6a69097711bf7/raw)  
[source](https://gist.github.com/7rikazhexde/b2d9e0dc0ba65489fcc6a69097711bf7)

#### クラス図
![クラス図](http://www.plantuml.com/plantuml/proxy?src=https://gist.githubusercontent.com/7rikazhexde/4b86d017691376cd4d6fad2514de068f/raw)  
[source](https://gist.github.com/7rikazhexde/4b86d017691376cd4d6fad2514de068f)
