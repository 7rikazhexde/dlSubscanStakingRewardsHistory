import pytest
from tomlkit.toml_file import TOMLFile

from src.cryptact import CryptactInfo

# 1件分のテストコード
# 以下のコードをアサートしてテストする
# テストデータ：CryptactInfoクラスで取得するテーブルのカラムデータ
# 期待値：tomlファイルからデータを取得したカラムデータ
"""
def cryptact_test_1case(token,expect_token):
    config = TOMLFile("./src/config.toml")
    toml_config = config.read()
    config_cryptact_info = toml_config.get("cryptact_info")

    action = config_cryptact_info["action"]
    price = config_cryptact_info["price"]
    counter = config_cryptact_info["counter"]
    fee = config_cryptact_info["fee"]
    feeccy = config_cryptact_info["feeccy"]
    source_token = f"source_{expect_token.lower()}"
    base_token = f"base_{expect_token.lower()}"
    source = config_cryptact_info[source_token]
    base = config_cryptact_info[base_token]

    ci = CryptactInfo(config_cryptact_info, token)

    assert ci.cryptact_info == (action, source, base, price, counter, fee, feeccy)
"""


# tomlファイルからデータを取得して期待値を作成するメソッド
def cryptact_expect_val(token):
    config = TOMLFile("./src/config.toml")
    toml_config = config.read()
    config_cryptact_info = toml_config.get("cryptact_info")

    action = config_cryptact_info["action"]
    price = config_cryptact_info["price"]
    counter = config_cryptact_info["counter"]
    fee = config_cryptact_info["fee"]
    feeccy = config_cryptact_info["feeccy"]
    source_token = f"source_{token.lower()}"
    base_token = f"base_{token.lower()}"
    source = config_cryptact_info[source_token]
    base = config_cryptact_info[base_token]

    return (action, source, base, price, counter, fee, feeccy)


# 複数のテストケースを実行する場合(正常系)
def cryptact_culumn_data_test(token):
    config = TOMLFile("./src/config.toml")
    toml_config = config.read()
    config_cryptact_info = toml_config.get("cryptact_info")
    ci = CryptactInfo(config_cryptact_info, token)
    return ci.cryptact_info


# テストケース1
@pytest.mark.parametrize(
    ("token", "expected"),
    [
        ("DOT", cryptact_expect_val("DOT")),
        ("KSM", cryptact_expect_val("KSM")),
        ("ASTR", cryptact_expect_val("ASTR")),
    ],
)
def test1(token, expected):
    assert cryptact_culumn_data_test(token) == expected


# 複数のテストケースを実行する場合(異常系)
def cryptact_culumn_data_test_ng(token):
    config = TOMLFile("./src/config.toml")
    toml_config = config.read()
    config_cryptact_info = toml_config.get("cryptact_info")
    ci = CryptactInfo(config_cryptact_info, token)
    return ci.cryptact_info


# テストケース2
@pytest.mark.parametrize(
    ("token", "expected"),
    [
        ("DOT", cryptact_expect_val("KSM")),
        ("DOT", cryptact_expect_val("ASTR")),
        ("KSM", cryptact_expect_val("DOT")),
        ("KSM", cryptact_expect_val("ASTR")),
        ("ASTR", cryptact_expect_val("DOT")),
        ("ASTR", cryptact_expect_val("KSM")),
    ],
)
def test2(token, expected):
    assert cryptact_culumn_data_test_ng(token) != expected


# 1件ずつテストする場合
"""
def test():
    cryptact_test_1case("DOT","DOT")
    cryptact_test_1case("KSM","DOT")
    cryptact_test_1case("ASTR","ASTR")
"""
