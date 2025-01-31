from util import output
from util.token import Token


class TestOutput:
    def test_format_biggest_holders(self):
        input_dict = {
            "holder_1": 1,
            "holder_2": 3,
            "GUfCR9mK6azb9vcpsxgXyj7XRPAKJd4KMHTTVvtncGgp": 50,
            "3D49QorJyNaL4rcpiynbuS3pRH4Y7EXEM6v6ZGaqfFGK": 1,
            "4pUQS4Jo2dsfWzt3VgHXy3H6RYnEDd11oWPiaM2rdAPw": 2,
            "F4ghBzHFNgJxV4wEQDchU5i7n4XWWMBSaq7CuswGiVsr": 4,
        }
        expected = """
Total tokens: 300
Total Holder Wallets: 6

Biggest holders:
----------
GUfCR9mK6azb9vcpsxgXyj7XRPAKJd4KMHTTVvtncGgp: 50 (MagicEden)
F4ghBzHFNgJxV4wEQDchU5i7n4XWWMBSaq7CuswGiVsr: 4 (DigitalEyes)
holder_2: 3
4pUQS4Jo2dsfWzt3VgHXy3H6RYnEDd11oWPiaM2rdAPw: 2 (AlphaArt)
holder_1: 1
3D49QorJyNaL4rcpiynbuS3pRH4Y7EXEM6v6ZGaqfFGK: 1 (Solanart)
"""

        result = output.format_biggest_holders(300, input_dict)
        assert result == expected

    def test_format_trait_frequency(self):
        input_dict = {
            "Eyes": {
                "holder_1": 2,
                "holder_2": 2,
            },
            "Hair": {
                "holder_1": 1,
                "holder_2": 6,
            },
        }
        expected = """
7 tokens with metadata

Attributes:
----------

Eyes
holder_1: 2 (2/7, 0.285714)
holder_2: 2 (2/7, 0.285714)

Hair
holder_1: 1 (1/7, 0.142857)
holder_2: 6 (6/7, 0.857143)
"""

        result = output.format_trait_frequency(7, input_dict)
        assert result == expected

    def test_sort_dict_by_values(self):
        input_dict = {
            "a": 2,
            "b": 4,
            "c": 1,
            "d": 3,
        }
        expected = {
            "c": 1,
            "a": 2,
            "d": 3,
            "b": 4,
        }

        result = output.sort_dict_by_values(input_dict)
        assert result == expected

    def test_sort_dict_by_values_reverse(self):
        input_dict = {
            "a": 2,
            "b": 4,
            "c": 1,
            "d": 3,
        }
        expected = {
            "b": 4,
            "d": 3,
            "a": 2,
            "c": 1,
        }

        result = output.sort_dict_by_values(input_dict, reverse=True)
        assert result == expected

    def test_holder_snapshot(self, mocker):
        input_dict = {
            "token_addr_1": Token(
                token="token_addr_1",
                holder_address="owner_1",
                amount=1,
                name="Token #1",
                id="1",
                image="https://www.iana.org/_img/2022/iana-logo-header.svg",
                traits={"Trait1": "Value1"},
            )
        }
        headers = [
            "Number",
            "TokenName",
            "Token",
            "HolderAddress",
            "TotalHeld",
            "Image",
            "Rank",
            "Rarity",
            "Trait1",
        ]
        expected = [
            [
                "1",
                "Token #1",
                "token_addr_1",
                "owner_1",
                1,
                "https://www.iana.org/_img/2022/iana-logo-header.svg",
                1,
                "100.00000000000000000000%",
                "Value1",
            ]
        ]
        test_outfile_name = "outfile.csv"
        pd_mock = mocker.patch("pandas.DataFrame")
        output.holder_snapshot(input_dict, test_outfile_name)
        pd_mock.assert_called_once_with(expected, columns=headers)
        pd_mock.return_value.to_csv.assert_called_once_with(test_outfile_name)

    def test_get_trait_map(self):
        input_dict = {
            "token_1": Token(token="token_1", traits={"hair": "white", "eyes": "blue"}),
            "token_2": Token(token="token_2", traits={"hair": "white", "eyes": ""}),
            "token_3": Token(token="token_3", traits={"jacket": "yes"}),
        }
        expected = {"hair": 0, "eyes": 1, "jacket": 2}
        result = output.get_trait_map(input_dict)
        assert result == expected

    def test_format_token_rarity(self):
        input_dict = {
            "token_1": Token(token="token_1", traits={"hair": "white", "eyes": "blue"}),
            "token_2": Token(token="token_2", traits={"hair": "white", "eyes": ""}),
            "token_3": Token(token="token_3", traits={"jacket": "yes"}),
        }
        expected = """
Token token_2
----------
Rank: 3
Rarity: 0.29629629629629627985

Traits
-----
hair: white (2/3, 0.666667)
eyes:  (2/3, 0.666667)
jacket:  (2/3, 0.666667)
"""
        result = output.format_token_rarity("token_2", input_dict)
        assert result == expected
