import webbrowser

import PySimpleGUI as sg
from tomlkit.toml_file import TOMLFile

from gui import CreateGui
from subscan import (
    SubscanStakingRewardDataProcess,
    SubscanStakingRewardsDataProcessForCryptact,
)


class SgWindowProcess:
    def __init__(self):
        # iniファイルから設定を読み込む
        self.__font_info = "游ゴシック Medium"
        self.__toml_config = TOMLFile("./config.toml")
        self.__config = self.__toml_config.read()
        self.__config_subscan_api_info = self.__config.get("subscan_api_info")
        self.__config_subscan_api_doc = self.__config_subscan_api_info[
            "subscan_api_doc"
        ]
        self.__config_ui_info = self.__config["ui_info"]
        self.__config_cryptact_info = self.__config["cryptact_info"]

    def main(self):
        # CreateGuiクラスのインスタンス作成
        sg_gui = CreateGui(
            self.__config_subscan_api_info,
            self.__config_ui_info,
            self.__config_cryptact_info,
        )
        window = sg_gui.main_window()

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "-RELOAD-":
                # 取引対象と履歴タイプを選択した値で表示するため現在の値をSetする
                sg_gui.token_data = values["-TOKEN-"]
                sg_gui.history_type = values["-HISTORY-"]
                sg_gui.sort_type = values["-SORT-"]
                window.close()
                window = sg_gui.main_window()
            if event == "-SHOW-":
                window["-OUTPUT2-"].update("")
                input_num = values["-INPUT-"]

                address_token = f"address_{(sg_gui.token_data).lower()}"
                address_token_value = self.__config_subscan_api_info[address_token]
                decimal_point_adjust_token = (
                    f"adjust_value_{(sg_gui.token_data).lower()}"
                )
                decimal_point_adjust_token_value = self.__config_subscan_api_info[
                    decimal_point_adjust_token
                ]
                display_digit_token = f"display_digit_{(sg_gui.token_data).lower()}"
                display_digit_token_value = self.__config_subscan_api_info[
                    display_digit_token
                ]

                # Subscan API設定値の確認
                if (
                    address_token_value == ""
                    or decimal_point_adjust_token_value == ""
                    or display_digit_token_value == ""
                ):
                    sg.popup_ok(
                        "ERROR\nSubscan API設定を確認してください。\nアプリを終了します。",
                        font=(self.__font_info, 20),
                        button_color="red",
                    )
                    window.close()
                    quit()
                # 入力値の異常値判定
                if (
                    (input_num.isnumeric()) is False
                    or input_num == ""
                    or int(input_num) <= 0
                ):
                    sg.popup_ok(
                        "ERROR\n件数は1以上の整数で入力してください。アプリを終了します。",
                        font=(self.__font_info, 20),
                        button_color="red",
                    )
                    window.close()
                    quit()
                # 件数(文字列)が数を表す文字か判定(1以上が真)
                if input_num.isnumeric():
                    if values["-HISTORY-"] == "Reward&Slash":
                        stkrwd = SubscanStakingRewardDataProcess(
                            input_num,
                            self.__config_subscan_api_info,
                            values["-TOKEN-"],
                            values["-SORT-"],
                        )
                        (
                            response_code,
                            api_endpoint,
                            response_status_code,
                            header_list,
                            response_data,
                            df_csv,
                            list_num,
                        ) = stkrwd.get_subscan_stakerewards()
                    elif values["-HISTORY-"] == "CryptactCustom":
                        cyrptactcustom = SubscanStakingRewardsDataProcessForCryptact(
                            input_num,
                            self.__config_subscan_api_info,
                            self.__config_cryptact_info,
                            values["-TOKEN-"],
                            values["-SORT-"],
                        )
                        (
                            response_code,
                            api_endpoint,
                            response_status_code,
                            header_list,
                            response_data,
                            df_csv,
                            list_num,
                        ) = cyrptactcustom.create_stakerewards_cryptact_cutom_df()

                    # 受信データエラー判定
                    # codeエラーの場合
                    if response_code != 0:
                        text = f"code: {response_code}\n\nError Details: Invalid Account Address.\nPlease Check Account Address:\n"
                        sg.popup_scrolled(
                            "error", text, size=(40, 6), font=(self.__font_info, 20)
                        )
                        window.close()
                        quit()

                    # HTTP Status Codesエラー
                    if response_status_code != 200:
                        text = f"HTTP Status Codes: {response_status_code}\n\nPlease Check Subscan API Documents:\n{self.__config_subscan_api_doc}\n"
                        sg.popup_scrolled(
                            "error", text, size=(40, 6), font=(self.__font_info, 20)
                        )
                        window.close()
                        quit()

                    if list_num == 0:
                        text = (
                            "値を取得できませんでした。\nアカウントアドレス、または、取得した値を確認してください。\nアプリを終了します。"
                        )
                        sg.popup_scrolled(
                            "error", text, size=(40, 5), font=(self.__font_info, 20)
                        )
                        window.close()
                        quit()

                    # テーブル要素取得
                    table = window["-TABLE-"]

                    # response_data_layoutでTableの値(pandas.DataFrame)を表示するために
                    # tkinterのイベントを追加(クリック時にeventが-TABLE-CLICK-で通知される)
                    # https://stackoverflow.com/questions/68173962/how-to-obtain-the-row-and-column-of-selected-cell-in-pysimplegui
                    table.bind("<Button-1>", "CLICK-")

                    # Table Elementにテーブル属性はあるが、updateメソッドが存在しないためheading情報を指定して更新する
                    # windowsインスタンスではAttributeError: 'NoneType'となるため見出しを取得するためWidgetプロパティを指定する
                    # https://github.com/PySimpleGUI/PySimpleGUI/issues/1307
                    sg_gui.update_title(table.Widget, header_list)

                    # cURLで受信した値で更新する
                    window["-TABLE-"].update(response_data)

                    # ColumnとTableを表示するためvisibleをTrueにする
                    # https://github.com/PySimpleGUI/PySimpleGUI/issues/2102
                    window["-COL-"].update(visible=True)
                    # csvファイル保存ボタンを有効化
                    window["-SAVE-"].update(disabled=False)
                    if int(input_num) > int(len(df_csv)):
                        supplement = " ( ※存在する履歴の上限値まで取得しました )"
                    else:
                        supplement = ""
                    output_string = f"取得結果:\n-- API Endpoint: {api_endpoint}\n-- HTTP Status Codes: {response_status_code}\n-- 取得件数: {len(df_csv)}{supplement}\n"
                    window["-OUTPUT1-"].update(output_string)
                    if values["-HISTORY-"] == "Reward&Slash":
                        table_title_string = "テーブル表示形式:Reward&Slash形式"
                    elif values["-HISTORY-"] == "CryptactCustom":
                        table_title_string = "テーブル表示形式:クリプタクトカスタムファイル"

                    window["-SHOW_TABLE-"].update(table_title_string)
                else:
                    sg.popup_error(
                        "値を取得できませんでした。\nSubscan APIの設定、または入力した情報を確認してください。\nアプリを終了します。",
                        font=(self.__font_info, 20),
                    )
                    window.close()
                    quit()
            if event == "-UNSHOW-":
                window["-COL-"].update(visible=False)
                # テーブルクリア後はcsvファイル保存のボタンを無効化する
                window["-SAVE-"].update(disabled=True)
                window["-OUTPUT1-"].update("")
                window["-OUTPUT2-"].update("")
                window["-TABLE_DATA-"].update("")
                window["-TABLE_DATA_TITLE-"].update("")
                window["-SHOW_TABLE-"].update("")
            if event == "-SAVE-":
                result = sg.popup_get_file("Save as", no_window=True, save_as=True)
                if result != "":
                    # パスが空でなければindex指定なしで指定のパスにcsvファイルを保存する
                    file_path = result + ".csv"
                    df_csv.to_csv(file_path, index=False, encoding="utf-8")
                    save_location = file_path
                    output_string = f"ファイル保存先:\n-- Save Location: {save_location}\n"
                    window["-OUTPUT2-"].update(output_string)
            if event == "-SETTING-":
                # 取引対象と履歴タイプを選択した値で表示するため現在の値をSetする
                sg_gui.token_data = values["-TOKEN-"]
                sg_gui.history_type = values["-HISTORY-"]
                sg_gui.sort_type = values["-SORT-"]
                window.close()
                window = sg_gui.config_window(
                    self.__config_subscan_api_info, values["-TOKEN-"]
                )
            if event == "-CONFIG_UPDATE-":
                toml_config = TOMLFile("./config.toml")
                edit = toml_config.read()
                edit_subscan = edit.get("subscan_api_info")
                address_token_value = f"-SUBSCAN_ADDRESS_{sg_gui.token_data}-"
                address_token = f"address_{(sg_gui.token_data).lower()}"

                decimal_point_adjust_token_value = (
                    f"-SUBSCAN_ADJUST_VALUE_{sg_gui.token_data}-"
                )
                decimal_point_adjust_token = (
                    f"adjust_value_{(sg_gui.token_data).lower()}"
                )

                display_digit_token_value = (
                    f"-SUBSCAN_DISPLAY_DIGIT_{sg_gui.token_data}-"
                )
                display_digit_token = f"display_digit_{(sg_gui.token_data).lower()}"

                edit_subscan[address_token] = values[address_token_value]
                edit_subscan[display_digit_token] = int(
                    values[display_digit_token_value]
                )
                edit_subscan[decimal_point_adjust_token] = float(
                    values[decimal_point_adjust_token_value]
                )

                edit_subscan["api_key"] = str(values["-SUBSCAN_API-"])
                toml_config.write(edit)
                window.close()
                self.__toml_config = TOMLFile("./config.toml")
                self.__config = self.__toml_config.read()
                self.__config_subscan_api_info = self.__config.get("subscan_api_info")
                self.__config_subscan_api_doc = self.__config_subscan_api_info[
                    "subscan_api_doc"
                ]
                self.__config_ui_info = self.__config["ui_info"]
                self.__config_cryptact_info = self.__config["cryptact_info"]
                window = sg_gui.main_window()
            if event == "-CANCEL-":
                window.close()
                window = sg_gui.main_window()
            if event == "-TABLE-CLICK-":
                e = table.user_bind_event
                region = table.Widget.identify("region", e.x, e.y)
                # 選択する領域を識別(cellのみ値を取得する)
                if region == "heading":
                    continue
                elif region == "cell":
                    row = int(table.Widget.identify_row(e.y))
                elif region == "separator":
                    continue
                else:
                    continue
                column = int(table.Widget.identify_column(e.x)[1:])
                table_data = df_csv.iat[row - 1, column - 1]
                table_data_string = table_data

                # テーブル上で選択した値でresponse_data_layoutを更新
                window["-TABLE_DATA_TITLE-"].update("選択したテーブルの値:")
                window["-TABLE_DATA-"].update(table_data_string)
                window["-TABLE_DATA-"].Widget.config(
                    readonlybackground=sg.theme_background_color("white")
                )
                window["-TABLE_DATA-"].Widget.config(borderwidth=0)
            if event == "-USAGE-":
                self.__font_info = "游ゴシック Medium"
                result = sg.popup_ok_cancel(
                    "GithubのREADME.mdへ移動します", font=(self.__font_info, 20)
                )
                if result == "OK":
                    webbrowser.open(
                        "https://github.com/7rikazhexde/dlSubscanStakingRewardsHistory/blob/main/README.md"
                    )
            if event == "-RETURN_MAIN_WINDOW-":
                window.close()
                window = sg_gui.main_window()

        window.close()


if __name__ == "__main__":
    sg_window_process = SgWindowProcess()
    sg_window_process.main()
