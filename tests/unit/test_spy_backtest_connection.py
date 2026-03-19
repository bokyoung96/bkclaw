from src.common.quant_db import QuantDBCredentials


def test_quant_db_credentials_dataclass_holds_expected_fields() -> None:
    creds = QuantDBCredentials(user="tester", password="secret")

    assert creds.user == "tester"
    assert creds.password == "secret"
