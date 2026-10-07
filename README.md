# MP1 Data Pipeline
This project is a command-line data processing pipeline that loads data from a raw CSV file, validates it, cleans it according to a configurable set of rules, and saves the result to an output file along with a summary report. The data is parsed alongside a YAML configuration file, then checked against required and numeric column rules, then cleaned (duplicate removal, missing-value handling, and outlier removal) based on which steps are enabled in the configuration, and finally written back out to disk as CSV. The codebase is organized into a src package containing one module per responsibility, with pipeline.py at the repository root acting as the CLI entry point that wires every module together. data_loaders.py is responsible for reading CSV and YAML files from disk into Python objects. data_validator.py checks that required columns exist and that configured numeric columns actually contain valid numeric values, dropping any rows that fail validation. data_processor.py applies the configured cleaning steps (duplicate removal, missing-value handling, and IQR/z-score outlier removal) and builds the final before/after cleaning report. data_output.py saves the cleaned DataFrame to the requested output path, creating directories as needed. utils.py holds shared helpers such as logging setup and input-file validation used across the other modules.

## Example Command
```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Example Output
17:57:28 DEBUG    __main__ — Arguments parsed: input = fixtures/sample_data.csv, output = output/clean.csv, format = csv
17:57:28 INFO     src.utils — Input file validated: fixtures/sample_data.csv
17:57:28 INFO     src.utils — Input file validated: config/config.yaml
17:57:28 INFO     src.data_loaders — Loaded CSV file: fixtures\sample_data.csv (100 rows)
17:57:28 INFO     src.data_loaders — Loaded YAML file: config\config.yaml
17:57:28 WARNING  src.data_validator — Invalid numeric value in rating at row 94: not_available
17:57:28 WARNING  src.data_validator — Invalid numeric value in rating at row 95: error
17:57:28 DEBUG    src.data_validator — Valid rows: 98, removed rows: 2
17:57:28 INFO     __main__ — Validation complete: 100 -> 98 rows
17:57:28 DEBUG    src.data_processor — 2 rows removed
17:57:28 DEBUG    src.data_processor — 2 rows removed
17:57:28 DEBUG    src.data_processor — {'Column': {'rating'}, 'Method': {'iqr'}, 'Threshold': {1.5}, 'Rows removed': {2}}
17:57:28 DEBUG    src.data_output — Saved 92 rows to output\clean.csv
17:57:28 INFO     __main__ — Saved clean data to output\clean.csv
{'rows_before': 100, 'rows_after': 92, 'rows_removed': 8, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
17:57:28 INFO     __main__ — Processing complete: 100 -> 92 rows