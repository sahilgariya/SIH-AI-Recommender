# Data preprocessing functions
"""
Data preprocessing and feature engineering functions.
"""

import pandas as pd


def load_dataset(file_path):
    """
    Load the SIH dataset from a CSV file.
    """

    df = pd.read_csv(file_path)

    return df


def clean_dataset(df):
    """
    Clean missing values, duplicate rows,
    and unnecessary whitespace.
    """

    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert important columns to clean strings
    columns = [
        "Problem Statement Title",
        "PS Number",
        "Theme",
        "Category",
        "Details"
    ]

    for column in columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    # Reset index
    df = df.reset_index(drop=True)

    return df


def create_weighted_text(
    df,
    title_weight=3,
    theme_weight=2,
    category_weight=1,
    details_weight=1
):
    """
    Create weighted text for TF-IDF.

    Important information such as the problem title
    receives more importance.
    """

    df = df.copy()

    title_text = (
        df["Problem Statement Title"]
        .fillna("")
        .astype(str)
        + " "
    ) * title_weight

    theme_text = (
        df["Theme"]
        .fillna("")
        .astype(str)
        + " "
    ) * theme_weight

    category_text = (
        df["Category"]
        .fillna("")
        .astype(str)
        + " "
    ) * category_weight

    details_text = (
        df["Details"]
        .fillna("")
        .astype(str)
        + " "
    ) * details_weight

    df["weighted_text"] = (
        title_text
        + theme_text
        + category_text
        + details_text
    )

    # Remove extra spaces
    df["weighted_text"] = (
        df["weighted_text"]
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
        .str.strip()
    )

    return df


def preprocess_dataset(file_path):
    """
    Complete preprocessing pipeline.
    """

    df = load_dataset(file_path)

    df = clean_dataset(df)

    df = create_weighted_text(df)

    return df