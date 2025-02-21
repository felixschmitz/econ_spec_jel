"""Helper functions for cleaning the metadata of discussion papers."""

import pandas as pd
import regex as re

MONTH_ORDER = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def _fuzzy_search_series_regex(
    sr: pd.Series, include: str, exclude: str | None = None, error_level: int = 3
) -> pd.Series:
    exclude_pattern = rf"^(?!.*{exclude}).*" if exclude else ""
    re_pattern = rf"{exclude_pattern}(?:{include}){{e<={error_level}}}"
    return sr[
        sr.apply(lambda x: bool(re.search(re_pattern, str(x), flags=re.IGNORECASE)))
    ]


def create_publication_year_month(year: pd.Series, month: pd.Series) -> pd.Series:
    """Create a datetime object from year and month.

    Args:
        year (pd.Series): Year.
        month (pd.Series): Month.

    Returns
    -------
        pd.Series: Year-month.
    """
    month_numerical = month.map(
        {month_name: i + 1 for i, month_name in enumerate(MONTH_ORDER)}
    )
    return pd.to_datetime(
        year.astype("string[pyarrow]") + "-" + month_numerical.astype("string[pyarrow]")
    )


def _get_neither_published_nor_forthcoming(
    sr: pd.Series, published: pd.Series, forthcoming: pd.Series
) -> pd.Series:
    missing_indices = sr.index.difference(published.index.union(forthcoming.index))
    missing_rows = sr.loc[missing_indices]
    return missing_rows[missing_rows.notna()]


def _get_preceded_dp(sr: pd.Series) -> pd.Series:
    sr_notna = sr[sr.notna()]
    preceded = sr_notna[sr_notna < sr_notna.index]
    return pd.Series(data=preceded.index, index=preceded.values)


def _determine_superseded_dp(sr: pd.Series) -> pd.Series:
    iza_dp_pattern = (
        r"(?<!International Institute for Labour Studies\s)"
        r"(?<!ILO Employment\s)"
        r"(?<!OECD Education\s)"
        r"(?<!European Central Bank\s)"
        r"(?<!NBER\s)"
        r"(?<!Cedefop\s)"
        r"(?<!IFS\s)"
        r"(?<!European Investment Bank\s)"
        r"(?:IZA\s*DP(?:\s*No\.?|#)?|IZA\s*Discussion\s*Paper\s*No\.?|DP\s*No\.?|DP\s+)(\d{3,5})"
    )
    dp_numbers = sr.str.extract(iza_dp_pattern, expand=False).astype("uint32[pyarrow]")
    new_rows = _get_preceded_dp(dp_numbers)
    old_rows = dp_numbers.drop(labels=new_rows.values)
    return pd.concat([old_rows, new_rows]).sort_index()


def clean_publication_information(
    sr: pd.Series,
) -> tuple[pd.Series]:
    """Clean publication information.

    Args:
        sr (pd.Series): Publication information.

    Returns
    -------
        tuple[pd.Series]: Published, forthcoming,
        other publication information, and superseded.
    """
    # replace typos of published (pubished, publiched, publishd, pubslished,
    # publlished, publslihed, publiished, publisehd, publilshed, publshed,
    # publishes, pablished, piblished, publishled, publication)
    # and forthcoming
    published = _fuzzy_search_series_regex(sr, "published|publication", "forthcoming")
    forthcoming = _fuzzy_search_series_regex(sr, "forthcoming")
    other_publication_information = _get_neither_published_nor_forthcoming(
        sr, published, forthcoming
    )
    superseded = _determine_superseded_dp(other_publication_information)
    return published, forthcoming, other_publication_information, superseded


def clean_jel_codes(sr: pd.Series) -> pd.Series:
    """Clean JEL codes of discussion paper.

    Args:
        sr (pd.Series): JEL codes.

    Returns
    -------
        pd.Series: Cleaned JEL codes.
    """
    sr_manual_adapted = _apply_manual_adaptations(sr)
    sr_capitalized = _capitalize_jel_codes(sr_manual_adapted)
    sr_leading_i = _replace_leading_one_with_i(sr_capitalized)
    sr_no_leading_zero = _drop_leading_zeros(sr_leading_i)
    sr_proper_codes = _drop_improper_jel_codes(sr_no_leading_zero)
    sr_generalized_codes = _append_zero_for_jel_codes_len_two(sr_proper_codes)
    return _sort_jel_codes(sr_generalized_codes)


def _apply_manual_adaptations(sr: pd.Series) -> pd.Series:
    sr.loc[1359] = ["O10", "P2", "J31"]
    sr.loc[2139] = ["F02", "I12", "J16", "I21"]
    sr.loc[3640] = ["A20", "C31", "H43", "H75", "I20", "J24", "L26"]
    sr.loc[7240] = ["L11", "L51", "J8", "L25", "D6"]
    sr.loc[8263] = ["D1", "D7", "D9"]
    sr.loc[8342] = ["I20", "I21", "I22"]
    sr.loc[9279] = ["I10", "I26"]
    sr.loc[9577] = ["J31", "D86"]
    sr.loc[10095] = ["O10", "N00"]
    sr.loc[11031] = ["D00", "G2", "K35"]
    sr.loc[11954] = ["H00", "J60"]
    sr.loc[11982] = ["H00", "C93", "I28", "J10", "J24"]
    sr.loc[12670] = ["I24"]
    sr.loc[12870] = ["E24", "E62", "J20", "J24", "J31", "J45"]
    sr.loc[12897] = ["H12", "J13"]
    sr.loc[13237] = ["H00", "P00"]
    sr.loc[14064] = ["J00"]
    sr.loc[14103] = ["J63", "Z22"]
    sr.loc[14597] = ["I15", "J13", "O15"]
    sr.loc[14837] = ["C80", "H00", "I10", "J00"]
    sr.loc[14883] = ["H00"]
    sr.loc[14923] = ["F01", "P20"]
    sr.loc[15194] = ["K00", "J71"]
    sr.loc[15227] = ["J2", "I18", "I38", "H51", "H75"]
    sr.loc[15264] = ["I15", "J13", "O15", "O47"]
    sr.loc[15285] = ["O15", "O19", "J24", "F16", "F63"]
    sr.loc[15368] = ["I18", "J22"]
    sr.loc[15387] = ["I13", "J22", "J26", "I38", "D64"]
    sr.loc[15393] = ["I24"]
    sr.loc[15399] = ["F22", "O15"]
    sr.loc[15408] = ["J46", "J64", "J68", "O15"]
    sr.loc[15419] = ["I00"]
    sr.loc[15489] = ["I18", "J13"]
    sr.loc[15509] = ["C21", "C45", "C52", "H53", "R23"]
    sr.loc[16285] = ["I00", "J00"]
    sr.loc[16325] = ["I26", "J31", "O14", "O33"]
    sr.loc[16551] = ["D13", "J22", "O13", "O17", "Q53", "Q56"]
    sr.loc[16746] = ["JO8", "J23", "O47", "O31"]
    sr.loc[17026] = ["I21", "I22", "J15", "J24", "J61", "J62", "J71"]
    sr.loc[17322] = ["I32", "J23", "J31", "J42", "R23"]
    sr.loc[17355] = ["F22", "O12", "Z10"]
    sr.loc[17431] = ["N00", "O10"]
    sr.loc[17463] = ["H00", "O10", "N56"]
    sr.loc[17490] = ["I25", "J10", "O10", "O40", "Z10"]
    sr.loc[17610] = ["I25", "J24", "O12", "O15"]
    sr.loc[17622] = ["I20", "I24", "O33"]
    return sr


def _capitalize_jel_codes(sr: pd.Series) -> pd.Series:
    return sr.apply(lambda x: [code.title() for code in x])


def _replace_leading_one_with_i(sr: pd.Series) -> pd.Series:
    return sr.apply(lambda x: [re.sub(r"^1", "I", code) for code in x])


def _drop_leading_zeros(sr: pd.Series) -> pd.Series:
    return sr.apply(lambda x: [re.sub(r"^0", "", code) for code in x])


def _drop_improper_jel_codes(sr: pd.Series) -> pd.Series:
    return sr.apply(
        lambda x: [code for code in x if re.fullmatch(r"[A-Z]\d{1,2}", code)]
    )


def _append_zero_for_jel_codes_len_two(sr: pd.Series) -> pd.Series:
    return sr.apply(
        lambda x: [code + "0" if len(code) == 2 else code for code in x]
    )  # PLR2004


def _sort_jel_codes(sr: pd.Series) -> pd.Series:
    return sr.apply(
        lambda x: sorted(
            x, key=lambda code: (code[0], int(re.search(r"\d+", code).group()))
        )
    )


def drop_dp_with_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """Drop discussion papers with missing data.

    Args:
        df (pd.DataFrame): Metadata.

    Returns
    -------
        pd.DataFrame: Metadata without missing data.

    """
    df_unique_dp = _not_superseded_dp(df)
    return _non_empty_jel(df_unique_dp)


def _not_superseded_dp(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(df[df["superseded"].notna()].index)


def _non_empty_jel(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["jel_codes"].apply(lambda x: x != [])]
