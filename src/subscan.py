import json
import math
import time
from datetime import datetime

import pandas as pd
import requests

from cryptact import CryptactInfo


class SubscanStakingRewardsDataFrame:
    def __init__(self, config_subscan_api_info, token):
        # トークン情報
        self.__token_data = token

        # Reward&Slashのテーブル作成用のリスト
        # Reward&Slash / Download all data(csv) / header
        self.__reward_slash_data_header_config = (
            f"reward_slash_data_header_{token.lower()}"
        )
        self.__reward_slash_data_header_token = config_subscan_api_info[
            self.__reward_slash_data_header_config
        ]
        # Reward&Slash用のDataFrame作成
        self.__df_stkrwd_header_data = pd.DataFrame(
            columns=self.__reward_slash_data_header_token
        )

        # Responseデータ用のリスト
        # Staking API / reward-slash-v2(DOT,KSM) / Response / data / list
        # V2 API / reward-slash(ASTR) / Response / data / list
        reward_slash_data_config = f"reward_slash_data_{token.lower()}"
        self.__reward_slash_data_token = config_subscan_api_info[
            reward_slash_data_config
        ]

    # Reward&Slash用のDataFrameに対するアクセサ
    def get_stkrwd_header_df(self):
        return self.__df_stkrwd_header_data

    def set_stkrwd_header_df(self, df):
        self.__df_stkrwd_header_data = pd.concat([self.__df_stkrwd_header_data, df])

    df_stkrwd_header_data = property(get_stkrwd_header_df, set_stkrwd_header_df)

    # Responseデータ用のリストに対するアクセサ
    def get_stkrwd_df_token(self):
        return self.__reward_slash_data_token

    def set_stkrwd_df_token(self, df):
        self.__reward_slash_data_token = pd.concat([self.__reward_slash_data_token, df])

    reward_slash_data_token = property(get_stkrwd_df_token, set_stkrwd_df_token)

    # トークン情報に対するアクセサ
    def get_token_data(self):
        return self.__token_data

    token_data = property(get_token_data)

    # 受信したjsonデータのlist要素(item)から取得したいStakingRewardsのlistを作成するメソッド
    def get_reward_slash_data(self, item, response_json):
        stkrwd_data_list = []
        for column_index in self.__reward_slash_data_token:
            event_index_data = response_json["data"]["list"][item][column_index]
            stkrwd_data_list.append(event_index_data)
        # 受信したjsonデータ(list)の1要素分のデータとStakingRewardsのlistとして返す
        return stkrwd_data_list

    # StakingRewardsのlistからDOTとKSM用の値をリスト形式で作成するメソッド
    def get_reward_slash_data_var_dot_ksm(
        self, one_line_headerdata_list, adjust_value, digit
    ):
        # 1行分のjsonデータ用のリスト
        self.__one_line_data_list = []

        # 有効桁数
        digit = "{:." + digit + "f}"

        # 可変値
        # 0 event_index
        # 1 era
        # 2 block_timestamp
        # 3 extrinsic_index
        # 4 amount
        # 5 module_id
        # 6 event_id
        # 7 stash
        # 8 account
        # 9 validator_stash
        self.__event_index = one_line_headerdata_list[0]
        self.__era = one_line_headerdata_list[1]
        self.__date = "'" + (
            datetime.utcfromtimestamp(one_line_headerdata_list[2])
        ).strftime("%Y/%m/%d %H:%M:%S")
        # Blockデータはevent_indexから作成する
        self.__block = self.__event_index.split("-")[0]
        self.__extrinsic_index = one_line_headerdata_list[3]
        self.__value = float(one_line_headerdata_list[4]) * adjust_value
        self.__value = digit.format(self.__value)
        # Actionデータはmodule_idとevent_idから作成する
        self.__action = one_line_headerdata_list[5] + f"({one_line_headerdata_list[6]})"
        self.__stash = one_line_headerdata_list[7]
        self.__reward_account = one_line_headerdata_list[8]

        if self.token_data == "DOT":
            # DotにはValidator Stashが存在するため作成する
            self.__validator_stash = one_line_headerdata_list[9]
            self.__one_line_data_list = [
                self.__event_index,
                self.__era,
                self.__date,
                self.__block,
                self.__extrinsic_index,
                self.__value,
                self.__action,
                self.__stash,
                self.__reward_account,
                self.__validator_stash,
            ]
        elif self.token_data == "KSM":
            self.__one_line_data_list = [
                self.__event_index,
                self.__era,
                self.__date,
                self.__block,
                self.__extrinsic_index,
                self.__value,
                self.__action,
                self.__stash,
                self.__reward_account,
            ]
        return self.__one_line_data_list

    # StakingRewardsのlistからASTR用の値をリスト形式で作成するメソッド
    def get_reward_slash_data_var_astr(
        self, one_line_headerdata_list, adjust_value, digit
    ):
        self.__one_line_data_list = []
        digit = "{:." + digit + "f}"
        # 0 event_index
        # 1 block_timestamp
        # 2 block_num
        # 3 extrinsic_hash
        # 4 amount
        # 5 module_id
        # 6 event_id
        # Event IDデータはevent_indexから作成する
        self.__event_id = one_line_headerdata_list[0]
        self.__date = "'" + (
            datetime.utcfromtimestamp(one_line_headerdata_list[1])
        ).strftime("%Y/%m/%d %H:%M:%S")
        # Blockデータはevent_indexから作成する
        self.__block = self.__event_id.split("-")[0]
        self.__extrinsic_index = one_line_headerdata_list[3]
        self.__value = float(one_line_headerdata_list[4]) * adjust_value
        self.__value = "{:.14f}".format(self.__value)
        # Actionデータはmodule_idとevent_idから作成する
        self.__action = one_line_headerdata_list[5] + f"({one_line_headerdata_list[6]})"

        self.__one_line_data_list = [
            self.__event_id,
            self.__date,
            self.__block,
            self.__extrinsic_index,
            self.__value,
            self.__action,
        ]
        return self.__one_line_data_list

    # 指定されたlistをDataDrameに行指定で追加するメソッド
    def json_to_df(self, df, item, one_line_data_list):
        df.loc[item, :] = one_line_data_list
        return df


class SubscanStakingRewardsDataFrameForCryptact(SubscanStakingRewardsDataFrame):
    def __init__(self, config_subscan_api_info, config_cryptact_info, token):
        super().__init__(config_subscan_api_info, token)
        # クリプタクトカスタムファイル用のDataFrameを作成
        self.__cryptact_heder_data = config_cryptact_info["cryptact_custom_header"]
        self.__df_cryptact_header_data = pd.DataFrame(
            columns=self.__cryptact_heder_data
        )

    # クリプタクトカスタムファイル用のDataFrameに対するアクセサ
    def get_cryptact_header_df(self):
        return self.__df_cryptact_header_data

    def set_cryptact_header_df(self, df):
        self.__df_cryptact_header_data = pd.concat([self.__df_cryptact_header_data, df])

    df_cryptact_header_data = property(get_cryptact_header_df, set_cryptact_header_df)

    def get_reward_slash_data_var_cryptact(
        self, one_line_headerdata_list, cryptact_info_data, adjust_value, digit
    ):
        self.__one_line_data_list = []
        digit = "{:." + digit + "f}"
        # 固定値
        (
            action,
            source,
            base,
            price,
            counter,
            fee,
            feeccy,
        ) = cryptact_info_data.cryptact_info

        # 可変値
        # 0 event_index
        # 1 era
        # 2 block_timestamp
        # 3 extrinsic_index
        # 4 amount
        # 5 module_id
        # 6 event_id
        # 7 stash
        # 8 account
        # 9 validator_stash
        if self.token_data == "DOT" or self.token_data == "KSM":
            self.__event_index = one_line_headerdata_list[0]
            self.__date = "'" + (
                datetime.fromtimestamp(one_line_headerdata_list[2])
            ).strftime("%Y/%m/%d %H:%M:%S")
            self.__value = float(one_line_headerdata_list[4]) * adjust_value
            self.__value = digit.format(self.__value)
            self.__one_line_data_list = [
                self.__date,
                action,
                source,
                base,
                self.__value,
                price,
                counter,
                fee,
                feeccy,
                self.__event_index,
            ]
        # 0 event_index
        # 1 block_timestamp
        # 2 block_num
        # 3 extrinsic_hash
        # 4 amount
        # 5 module_id
        elif self.token_data == "ASTR":
            self.__event_id = one_line_headerdata_list[0]
            self.__date = "'" + (
                datetime.fromtimestamp(one_line_headerdata_list[1])
            ).strftime("%Y/%m/%d %H:%M:%S")
            self.__value = float(one_line_headerdata_list[4]) * adjust_value
            self.__value = digit.format(self.__value)
            self.__one_line_data_list = [
                self.__date,
                action,
                source,
                base,
                self.__value,
                price,
                counter,
                fee,
                feeccy,
                self.__event_id,
            ]
        return self.__one_line_data_list


class SubscanApiInfo:
    def __init__(self, config_subscan_api_info, token):
        self.__api_key = config_subscan_api_info["api_key"]

        request_url_config = f"request_url_{token.lower()}"
        api_host_config = f"api_host_{token.lower()}"
        address_cnfig = f"address_{token.lower()}"
        adjust_value_config = f"adjust_value_{token.lower()}"

        self.__request_url = config_subscan_api_info[request_url_config]
        self.__api_host = config_subscan_api_info[api_host_config]
        self.__address = config_subscan_api_info[address_cnfig]
        self.__adjust_value = float(config_subscan_api_info[adjust_value_config])

        self.__api_endpoint = self.__api_host + self.__request_url
        # Subscan APIを使用しrequestsモジュールでPOSTリクエストする
        # header情報
        self.__headers_dict = {
            "Content-Type": "application/json",
            "X-API-Key": self.__api_key,
        }
        # data-raw情報
        # rowの指定のみでlistの情報は取得できるためpageは0固定とする
        # rowは上限100まで
        self.__data_dict = {"row": 0, "page": 0, "address": self.__address}

    def get_subscan_api_info(self):
        return (
            self.__api_endpoint,
            self.__headers_dict,
            self.__data_dict,
            self.__adjust_value,
        )

    subscan_api_info = property(get_subscan_api_info)


class SubscanStakingRewardDataProcess:
    def __init__(self, input_num, config_subscan_api_info, token, sort):
        # インスタンス作成
        self.subscan_stkrwd_df = SubscanStakingRewardsDataFrame(
            config_subscan_api_info, token
        )
        self.subscan_api_data = SubscanApiInfo(config_subscan_api_info, token)

        # get_stkrwd_header_dfメソッドでdataframe初期化
        self.df_header = self.subscan_stkrwd_df.df_stkrwd_header_data

        # get_stkrwd_header_dfでヘッダー作成
        self.header_list = self.subscan_stkrwd_df.df_stkrwd_header_data

        # API情報取得
        (
            self.api_endpoint,
            self.headers_dict,
            self.data_dict,
            self.adjust_value,
        ) = self.subscan_api_data.subscan_api_info

        # 取得件数入力
        self.input_num = int(input_num)

        # API情報更新(件数で上書き)
        self.data_dict["row"] = self.input_num

        self.token = token

        # ソート情報生成
        if sort == "昇順":
            self.sort_type = True
        else:
            self.sort_type = False

        # 受信データ初期化
        self.response_data = []
        data_list = [["data1", 1], ["data2", 2]]
        self.sort_df_retrieve = pd.DataFrame(data_list, columns=["culumn1", "culumn2"])

        # Config情報取得
        display_digit_config = f"display_digit_{token.lower()}"
        # 有効桁数はformatメソッドで処理するため-1する
        self.digit = str(int(config_subscan_api_info[display_digit_config]) - 1)

    def get_subscan_stakerewards(self):
        # list要素数初期化
        list_num = 0

        # list要素の合計値初期化
        list_num_sum = 0

        # input_numが100より大きい場合、rowは上限値100のため、分割処理するため件数から処理回数を計算する
        if self.input_num > 100:
            # 取得するページ数の最大値を計算
            # ex)120->1.2->1,1+1で2となる
            page_renge = math.floor(self.input_num / 100) + 1
            # rowを更新(rowの上限値は100のため100row/pageとする)
            self.data_dict["row"] = 100

            for page in range(page_renge):
                # API rate limit exceededを考慮して0.2秒sleep
                time.sleep(0.2)
                # pegeを更新
                self.data_dict["page"] = page

                # Staking API / rewards-slash指定 / row:100, page:pageで送信
                response = requests.post(
                    self.api_endpoint,
                    headers=self.headers_dict,
                    data=json.dumps(self.data_dict),
                )

                # HTTP Status Codes
                response_status_code = response.status_code

                # レスポンスデータ(JSON形式)
                response_json = response.json()

                # エラーチェック
                try:
                    response_code = response_json["code"]
                except Exception as e:
                    # ex)API rate limit exceeded
                    print(e)
                    break

                try:
                    # アドレス不正でなければlistの要素数を取得
                    if response_code != 400:
                        list_num = len(response_json["data"]["list"])
                except TypeError as e:
                    count = response_json["data"]["count"]
                    print(
                        f"TypeError, but at this point, the data reading process has been executed up to the upper limit, so the iterative process is terminated. / count: {count}\n"
                    )
                    print(e)
                    break

                # 1ページ毎にlist要素数を加算する
                list_num_sum += list_num

                # Response結果にエラーがなく、リストが存在すれば受信データを作成する
                if (
                    response_status_code == 200
                    and response_code == 0
                    and list_num_sum != 0
                ):
                    for item in range(list_num):
                        one_line_headerdata_list = (
                            self.subscan_stkrwd_df.get_reward_slash_data(
                                item, response_json
                            )
                        )
                        if self.token == "DOT" or self.token == "KSM":
                            one_line_data_list = self.subscan_stkrwd_df.get_reward_slash_data_var_dot_ksm(
                                one_line_headerdata_list, self.adjust_value, self.digit
                            )
                        elif self.token == "ASTR":
                            one_line_data_list = (
                                self.subscan_stkrwd_df.get_reward_slash_data_var_astr(
                                    one_line_headerdata_list,
                                    self.adjust_value,
                                    self.digit,
                                )
                            )
                        df_page = self.subscan_stkrwd_df.json_to_df(
                            self.df_header, item, one_line_data_list
                        )
                    # setterでlistからDataFrame作成(結合)
                    self.subscan_stkrwd_df.df_stkrwd_header_data = df_page
                    # getterで作成(結合)されたDataFrameを取得
                    concat_df = self.subscan_stkrwd_df.df_stkrwd_header_data
                    # 重複行削除
                    concat_df_duplicates = concat_df.drop_duplicates()
                    # page_renge分取得したデータから件数分抽出する
                    df_retrieve = concat_df_duplicates.iloc[: self.input_num, :]
                    # ソート
                    self.sort_df_retrieve = self.sort_dataframe(
                        df_retrieve, self.sort_type
                    )
                    # 抽出後のデータをリスト化
                    self.response_data = self.sort_df_retrieve.values.tolist()
                    # list要素の合計値で上書き
                    list_num = list_num_sum

        else:
            # self.input_num <= 100
            # Staking API / rewards-slash指定
            response = requests.post(
                self.api_endpoint,
                headers=self.headers_dict,
                data=json.dumps(self.data_dict),
            )

            # HTTP Status Codes
            response_status_code = response.status_code

            # レスポンスデータ(JSON形式)
            response_json = response.json()
            response_code = response_json["code"]

            # listの要素数を取得
            if response_code != 400:
                list_num = len(response_json["data"]["list"])

            # Response結果にエラーがなく、リストが存在すれば受信データを作成する
            if response_status_code == 200 and response_code == 0 and list_num != 0:
                # 受信データ数分処理する
                for item in range(list_num):
                    one_line_headerdata_list = (
                        self.subscan_stkrwd_df.get_reward_slash_data(
                            item, response_json
                        )
                    )
                    if self.token == "DOT" or self.token == "KSM":
                        one_line_data_list = (
                            self.subscan_stkrwd_df.get_reward_slash_data_var_dot_ksm(
                                one_line_headerdata_list, self.adjust_value, self.digit
                            )
                        )
                    elif self.token == "ASTR":
                        one_line_data_list = (
                            self.subscan_stkrwd_df.get_reward_slash_data_var_astr(
                                one_line_headerdata_list, self.adjust_value, self.digit
                            )
                        )
                    df_page = self.subscan_stkrwd_df.json_to_df(
                        self.df_header, item, one_line_data_list
                    )
                # ソート
                self.sort_df_retrieve = self.sort_dataframe(df_page, self.sort_type)
                # 抽出後のデータをリスト化
                self.response_data = self.sort_df_retrieve.values.tolist()
        return (
            response_code,
            self.api_endpoint,
            response_status_code,
            self.header_list,
            self.response_data,
            self.sort_df_retrieve,
            list_num,
        )

    def sort_dataframe(self, df, sort_type):
        num = len(df)
        sort_Column = list(range(num))
        df_s1 = df.assign(SortColumn=sort_Column)
        df_s2 = df_s1.sort_values("SortColumn", ascending=sort_type)
        df_s3 = df_s2.drop("SortColumn", axis=1)
        return df_s3


class SubscanStakingRewardsDataProcessForCryptact(SubscanStakingRewardDataProcess):
    def __init__(
        self, input_num, config_subscan_api_info, config_cryptact_info, token, sort
    ):
        # インスタンス作成
        self.subscan_stkrwd_df_for_cryptact = SubscanStakingRewardsDataFrameForCryptact(
            config_subscan_api_info, config_cryptact_info, token
        )
        self.subscan_api_data = SubscanApiInfo(config_subscan_api_info, token)
        self.cryptact_info_data = CryptactInfo(config_cryptact_info, token)

        # get_cryptact_header_dfメソッドでdataframe初期化
        self.df_header = self.subscan_stkrwd_df_for_cryptact.df_cryptact_header_data

        # get_cryptact_header_dfメソッドでヘッダー作成
        self.header_list = self.subscan_stkrwd_df_for_cryptact.df_cryptact_header_data

        # API情報取得
        (
            self.api_endpoint,
            self.headers_dict,
            self.data_dict,
            self.adjust_value,
        ) = self.subscan_api_data.subscan_api_info

        # 取得件数入力
        self.input_num = int(input_num)

        # API情報更新(件数で上書き)
        self.data_dict["row"] = self.input_num

        # ソート情報生成
        if sort == "昇順":
            self.sort_type = True
        else:
            self.sort_type = False

        # 受信データ初期化
        self.response_data = []
        data_list = [["data1", 1], ["data2", 2]]
        self.sort_df_retrieve = pd.DataFrame(data_list, columns=["culumn1", "culumn2"])

        # Config情報取得
        display_digit_config = f"display_digit_{token.lower()}"
        # 有効桁数はformatメソッドで処理するため-1する
        self.digit = str(int(config_subscan_api_info[display_digit_config]) - 1)

    def create_stakerewards_cryptact_cutom_df(self):
        # listの要素数初期化
        list_num = 0

        # list要素の合計値初期化
        list_num_sum = 0

        # input_numが100より大きい場合、rowは上限値100のため、分割処理するため件数から処理回数を計算する
        if self.input_num > 100:
            # 取得するページ数の最大値を計算
            # ex)120->1.2->1,1+1で2となる
            page_renge = math.floor(self.input_num / 100) + 1
            # rowを更新(rowの上限値は100のため100row/pageとする)
            self.data_dict["row"] = 100

            for page in range(page_renge):
                # API rate limit exceededを考慮して0.2秒sleep
                time.sleep(0.2)

                # pegeを更新
                self.data_dict["page"] = page

                # Staking API / rewards-slash指定 / row:100, page:pageで送信
                response = requests.post(
                    self.api_endpoint,
                    headers=self.headers_dict,
                    data=json.dumps(self.data_dict),
                )

                # HTTP Status Codes
                response_status_code = response.status_code

                # レスポンスデータ(JSON形式)
                response_json = response.json()

                # エラーチェック
                try:
                    response_code = response_json["code"]
                except Exception as e:
                    # ex)API rate limit exceeded
                    print(e)
                    break
                try:
                    # アドレス不正でなければlistの要素数を取得
                    if response_code != 400:
                        list_num = len(response_json["data"]["list"])
                except TypeError as e:
                    count = response_json["data"]["count"]
                    print(
                        f"TypeError, but at this point, the data reading process has been executed up to the upper limit, so the iterative process is terminated. / count: {count}\n"
                    )
                    print(e)
                    break

                # 1ページ毎にlist要素数を加算する
                list_num_sum += list_num

                # Response結果にエラーがなく、リストが存在すれば受信データを作成する
                if (
                    response_status_code == 200
                    and response_code == 0
                    and list_num_sum != 0
                ):
                    for item in range(list_num):
                        one_line_headerdata_list = (
                            self.subscan_stkrwd_df_for_cryptact.get_reward_slash_data(
                                item, response_json
                            )
                        )
                        one_line_data_list = self.subscan_stkrwd_df_for_cryptact.get_reward_slash_data_var_cryptact(
                            one_line_headerdata_list,
                            self.cryptact_info_data,
                            self.adjust_value,
                            self.digit,
                        )
                        df_page = self.subscan_stkrwd_df_for_cryptact.json_to_df(
                            self.df_header, item, one_line_data_list
                        )
                    # setterでlistからDataFrame作成(結合)
                    self.subscan_stkrwd_df_for_cryptact.df_cryptact_header_data = (
                        df_page
                    )
                    # getterで作成(結合)されたDataFrameを取得
                    concat_df = (
                        self.subscan_stkrwd_df_for_cryptact.df_cryptact_header_data
                    )
                    # 重複行削除
                    concat_df_duplicates = concat_df.drop_duplicates()
                    # page_renge分取得したデータから件数分抽出する
                    df_retrieve = concat_df_duplicates.iloc[: self.input_num, :]
                    # ソート
                    self.sort_df_retrieve = self.sort_dataframe(
                        df_retrieve, self.sort_type
                    )
                    # 抽出後のデータをリスト化
                    self.response_data = self.sort_df_retrieve.values.tolist()
                    # list要素の合計値で上書き
                    list_num = list_num_sum

        else:
            # self.input_num <= 100
            # Staking API / rewards-slash指定
            response = requests.post(
                self.api_endpoint,
                headers=self.headers_dict,
                data=json.dumps(self.data_dict),
            )

            # HTTP Status Codes
            response_status_code = response.status_code

            # レスポンスデータ(JSON形式)
            response_json = response.json()
            response_code = response_json["code"]

            # listの要素数を取得
            if response_code != 400:
                list_num = len(response_json["data"]["list"])

            # Response結果にエラーがなく、リストが存在すれば受信データを作成する
            if response_status_code == 200 and response_code == 0 and list_num != 0:
                # 受信データ数分処理する
                for item in range(list_num):
                    one_line_headerdata_list = (
                        self.subscan_stkrwd_df_for_cryptact.get_reward_slash_data(
                            item, response_json
                        )
                    )
                    one_line_data_list = self.subscan_stkrwd_df_for_cryptact.get_reward_slash_data_var_cryptact(
                        one_line_headerdata_list,
                        self.cryptact_info_data,
                        self.adjust_value,
                        self.digit,
                    )
                    df_page = self.subscan_stkrwd_df_for_cryptact.json_to_df(
                        self.df_header, item, one_line_data_list
                    )
                # ソート
                self.sort_df_retrieve = self.sort_dataframe(df_page, self.sort_type)
                # 抽出後のデータをリスト化
                self.response_data = self.sort_df_retrieve.values.tolist()
        return (
            response_code,
            self.api_endpoint,
            response_status_code,
            self.header_list,
            self.response_data,
            self.sort_df_retrieve,
            list_num,
        )
