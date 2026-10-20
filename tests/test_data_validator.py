import pytest
import pandas as pd
from src import validate_dataframe


def test_validate_dataframe_removes_invalid_ratings(sample_df):
    # TODO: Set the required and numeric column names.
    # TODO: Call validate_dataframe().
    # TODO: Assert that 98 rows remain and all five columns are preserved.
    required_columns = ["record_id", "name", "rating", "category", "status"]
    numeric_columns = ["rating"]

    result = validate_dataframe(sample_df, required_columns, numeric_columns)

    assert len(result) == 98
    assert list(result.columns) == required_columns
    assert pd.api.types.is_numeric_dtype(result["rating"])

def test_validate_dataframe_with_missing_column(sample_df):
    # TODO: Set required_columns to include a nonexistent column.
    # TODO: Use pytest.raises(ValueError) around validate_dataframe().
    required_columns = ["record_id", "nonexistent_column"]
    numeric_columns = ["rating"]

    with pytest.raises(ValueError):
        validate_dataframe(sample_df, required_columns, numeric_columns)