import PySimpleGUI as sg

sg.theme("Reddit")


class CreateGui:
    def __init__(self, config_subscan_api_info, config_ui_info, config_cryptact_info):
        # token_list読み込み
        self.__token_data_list = config_subscan_api_info["token_list"]
        self.__token_data = self.__token_data_list[0]

        # history_type_list読み込み
        self.__history_type_list = config_ui_info["history_type_list"]
        self.__history_type = self.__history_type_list[0]

        # sort_list読み込み
        self.__sort_list = config_ui_info["sort_list"]
        self.__sort_type = self.__sort_list[0]

        # CryptactCustom用ヘッダーファイル読み込み
        self.__cryptact_header_data = config_cryptact_info["cryptact_custom_header"]

        # Reward&Slash用ヘッダーファイル読み込み
        reward_slash_data_header_config = (
            f"reward_slash_data_header_{self.__token_data.lower()}"
        )
        self.__reward_slash_data_header_token = config_subscan_api_info[
            reward_slash_data_header_config
        ]

    # コイン情報を処理するためにget_token_dataメソッドとset_token_dataメソッドをプロパティ化
    def get_token_data(self):
        return self.__token_data

    def set_token_data(self, token):
        self.__token_data = token

    token_data = property(get_token_data, set_token_data)

    def get_history_type(self):
        return self.__history_type

    def set_history_type(self, history_type_data):
        self.__history_type = history_type_data

    history_type = property(get_history_type, set_history_type)

    # ソート処理するためにget_sort_typeメソッドとset_sort_typeメソッドをプロパティ化
    def get_sort_type(self):
        return self.__sort_type

    def set_sort_type(self, sort_type_data):
        self.__sort_type = sort_type_data

    sort_type = property(get_sort_type, set_sort_type)

    def main_window(self):
        # テーブル要素(cURLで受信した値を表示するレイアウト)
        # Tableでvisible=Falseにするとスクロールバーのみ表示されるためColumnの指定で非表示にする(culumn_layout参照)
        # Tableの値を更新するためベースのTableを作成する（ヘッダーはconfig.iniで定義した値,表の値はvaluesで指定する)
        # valuesは10行15列のテーブル指定で初期化する(テーブルはこの値に依存するためnum_rowsの指定と合わせる)
        data = [[0 for j in range(10)] for i in range(15)]

        # 初期値で生成したTableを表示するためvisible_columnsをTrue(リスト指定)にする
        vclum = True
        font_info = "游ゴシック Medium"

        if self.__history_type == "Reward&Slash":
            # 列数と列幅をトークン毎に設定する
            if self.__token_data == "DOT":
                visible_columns = [vclum for x in range(10)]
                col_widths_token = [14, 6, 17, 10, 13, 12, 15, 15, 15, 15]
            elif self.__token_data == "KSM":
                visible_columns = [vclum for x in range(9)]
                col_widths_token = [14, 6, 17, 10, 13, 12, 15, 15, 15]
            elif self.__token_data == "ASTR":
                visible_columns = [vclum for x in range(6)]
                col_widths_token = [11, 17, 8, 15, 20, 20]
            table_layout = sg.Table(
                values=data,
                headings=self.__reward_slash_data_header_token,
                font=(font_info, 15),
                visible_column_map=visible_columns,
                # 各列が占める文字数指定
                col_widths=col_widths_token,
                # Trueにすると列幅が固定になるためFalseとする
                # https://github.com/PySimpleGUI/PySimpleGUI/issues/4375
                auto_size_columns=False,
                # 一度に表示するテーブルの行数を指定(表示するテーブルの行数<初期化したテーブルの行数)
                num_rows=min(5, len(data)),
                enable_events=True,
                key="-TABLE-",
            )
        elif self.__history_type == "CryptactCustom":
            visible_columns = [vclum for x in range(10)]
            table_layout = sg.Table(
                values=data,
                headings=self.__cryptact_header_data,
                font=(font_info, 15),
                visible_column_map=visible_columns,
                # 各列が占める文字数指定(トークン共通)
                col_widths=[17, 8, 20, 6, 20, 6, 8, 6, 8, 13],
                # Trueにすると列幅が固定になるためFalseとする
                # https://github.com/PySimpleGUI/PySimpleGUI/issues/4375
                auto_size_columns=False,
                # 一度に表示するテーブルの行数を指定(表示するテーブルの行数<初期化したテーブルの行数)
                num_rows=min(5, len(data)),
                enable_events=True,
                key="-TABLE-",
            )

        # UI起動時に表示するレイアウト
        show_layout = (
            [
                sg.Text(
                    "DL Subscan Staking Rewards History",
                    font=(font_info, 25),
                    justification="center",
                    text_color="#483d8b",
                )
            ],
            [sg.HorizontalSeparator()],
            [
                sg.Button(
                    "使い方",
                    font=(font_info, 20),
                    size=(5, 1),
                    button_color=("#FFFFFF", "#1f3134"),
                    key="-USAGE-",
                )
            ],
            [sg.HorizontalSeparator()],
            [
                sg.Text("取得対象:", font=(font_info, 20), size=(7, 1)),
                sg.Spin(
                    values=self.__token_data_list,
                    font=(font_info, 20),
                    initial_value=self.__token_data,
                    size=(4, 1),
                    key="-TOKEN-",
                ),
                sg.Text("履歴タイプ:", font=(font_info, 20), size=(10, 1)),
                sg.Spin(
                    values=self.__history_type_list,
                    font=(font_info, 20),
                    initial_value=self.__history_type,
                    size=(12, 1),
                    key="-HISTORY-",
                ),
                sg.Button(
                    "テーブル初期化", font=(font_info, 20), size=(11, 1), key="-RELOAD-"
                ),
                sg.Button("設定", font=(font_info, 20), size=(5, 1), key="-SETTING-"),
            ],
            [sg.HorizontalSeparator()],
            [
                sg.Text("件数:", font=(font_info, 20), size=(7, 1)),
                sg.Input(font=(font_info, 20), size=(5, 1), key="-INPUT-"),
                # ソートタイプ: テーブルの一番下を基準に昇順(1,2,3,...),降順(...,3,2,1)
                sg.Text("ソートタイプ:", font=(font_info, 20), size=(10, 1)),
                sg.Spin(
                    values=self.__sort_list,
                    font=(font_info, 20),
                    initial_value=self.__sort_type,
                    size=(5, 1),
                    key="-SORT-",
                ),
                sg.Button("履歴取得", font=(font_info, 20), key="-SHOW-"),
                sg.Button("クリア", font=(font_info, 20), size=(5, 1), key="-UNSHOW-"),
                sg.Button(
                    "csvファイル保存", font=(font_info, 20), disabled=True, key="-SAVE-"
                ),
            ],
            [sg.HorizontalSeparator()],
        )

        # cURLで受信した結果を表示するレイアウト
        response_result_layout = (
            [sg.Text("", font=(font_info, 20), key="-OUTPUT1-")],
            [sg.Text("", font=(font_info, 20), key="-OUTPUT2-")],
        )

        # コンテナ要素(culumn_layoutではTable要素を指定するレイアウト)
        # Tableでvisible=Falseにするとスクロールバーのみ表示されるため
        # Column上にTableを埋め込みColumnのvisible=Falseに指定してTableを非表示にする
        # Columnのscrollableは表示しないためFalseに指定する
        # https://github.com/PySimpleGUI/PySimpleGUI/issues/2102
        culumn_layout = sg.Column(
            [[table_layout]], scrollable=False, visible=False, key="-COL-"
        )

        # Tableの値(pandas.DataFrame)を表示するレイアウト
        # テキストは選択時のみ表示するため空の文字列を指定する
        response_data_layout = (
            sg.Text("", font=(font_info, 20), key="-TABLE_DATA_TITLE-"),
            # Textデータをコピー可能にする
            # https://github.com/PySimpleGUI/PySimpleGUI/issues/2928
            sg.InputText(
                "",
                font=(font_info, 20),
                use_readonly_for_disable=True,
                disabled=False,
                border_width=0,
                background_color="white",
                key="-TABLE_DATA-",
            ),
        )

        # 履歴表示テーブル
        table_title_layout = sg.Text("", font=(font_info, 20), key="-SHOW_TABLE-")

        # レイアウト
        layout = [
            [show_layout],
            [response_result_layout],
            [table_title_layout],
            [culumn_layout],
            [response_data_layout],
        ]

        # ウインドウ位置
        return sg.Window(
            "DL Subscan Staking Rewards History",
            layout,
            resizable=True,
            grab_anywhere=True,
        )

    def config_window(self, config, token):
        font_info = "游ゴシック Medium"

        api_key_layout = [
            sg.Text("APIキー:", font=(font_info, 20), size=(15, 1)),
            sg.Input(
                config["api_key"],
                password_char="*",
                font=(font_info, 20),
                key="-SUBSCAN_API-",
                size=(30, 1),
            ),
        ]

        address_layout_text_value = f"{token}アドレス:"
        address_cnfig = f"address_{token.lower()}"
        address_layout_key = f"-SUBSCAN_ADDRESS_{token}-"
        address_layout = [
            sg.Text(address_layout_text_value, font=(font_info, 20), size=(15, 1)),
            sg.Input(
                config[address_cnfig],
                font=(font_info, 20),
                key=address_layout_key,
                size=(47, 1),
            ),
        ]

        adjust_val_layout_text_value = "小数点調整値:"
        adjust_val_cnfig = f"adjust_value_{token.lower()}"
        adjust_val_layout_key = f"-SUBSCAN_ADJUST_VALUE_{token}-"
        adjust_val_layout = [
            sg.Text(adjust_val_layout_text_value, font=(font_info, 20), size=(15, 1)),
            sg.Input(
                config[adjust_val_cnfig],
                font=(font_info, 20),
                key=adjust_val_layout_key,
                size=(30, 1),
            ),
        ]

        # (ex.3桁:1.234->1.23)
        display_digit_layout_text_value = "有効数字桁数:"
        display_digit_config = f"display_digit_{token.lower()}"
        display_digit_layout_key = f"-SUBSCAN_DISPLAY_DIGIT_{token}-"
        display_digit_layout = [
            sg.Text(
                display_digit_layout_text_value, font=(font_info, 20), size=(15, 1)
            ),
            sg.Input(
                config[display_digit_config],
                key=display_digit_layout_key,
                font=(font_info, 20),
                size=(5, 1),
            ),
        ]

        config_layout = [
            [
                sg.Text(
                    "Subscan API 設定",
                    font=("游ゴシック Medium", 22),
                    justification="center",
                    text_color="#483d8b",
                    pad=(0, 10),
                )
            ],
            [api_key_layout],
            [address_layout],
            [adjust_val_layout],
            [display_digit_layout],
            [sg.Text("(ex.3桁:1.234->1.23)", font=(font_info, 20), size=(15, 1))],
            [
                sg.Button(
                    "更新",
                    font=(font_info, 20),
                    key="-CONFIG_UPDATE-",
                    size=(5, 1),
                    pad=((300, 10), (20, 20)),
                ),
                sg.Button(
                    "キャンセル",
                    font=(font_info, 20),
                    key="-CANCEL-",
                    size=(8, 1),
                    pad=((10, 300), (20, 20)),
                ),
            ],
        ]

        return sg.Window(
            "DL Subscan Staking Rewards History", config_layout, finalize=True
        )

    def usage_window(self):
        font_info = "游ゴシック Medium"

        usage_window_layout = [
            [
                sg.Text(
                    "DL Subscan Staking Rewards History",
                    font=(font_info, 25),
                    justification="center",
                    text_color="#483d8b",
                )
            ],
            [sg.Image("./usage.png")],
            [
                sg.Button(
                    "戻る",
                    font=(font_info, 20),
                    button_color=("#000000", "#1f3134"),
                    key="-RETURN_MAIN_WINDOW-",
                    size=(5, 1),
                    pad=(180, 20),
                )
            ],
        ]
        return sg.Window("使い方", usage_window_layout, finalize=True)

    def update_title(self, table, headings):
        if self.__history_type == "Reward&Slash":
            header_data = self.__reward_slash_data_header_token
        elif self.__history_type == "CryptactCustom":
            header_data = self.__cryptact_header_data
        # テーブルのヘッダー更新
        for cid, text in zip(header_data, headings):
            table.heading(cid, text=text)
