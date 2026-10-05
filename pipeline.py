"""
Data Processing Pipeline - CLI Template
DS 3500 - MP1
Usage:
python pipeline.py --input data.csv --output clean.csv
python pipeline.py --input data.csv --output results.json --format json --
verbose
"""

import argparse
import logging
import sys
from pathlib import Path
from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(
        level = level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description = "Data Processing Pipeline")
    
    parser.add_argument(
        "--input", "-i",
        required = True,
        help = "Path to the input file"
    )
    
    parser.add_argument(
        "--config",
        required = True,
        help = "Path to the YAML file"
    )
    
    parser.add_argument(
        "--output", "-o",
        required = True,
        help = "Path to the output file"
    )
    
    parser.add_argument(
        "--format",
        choices = ["csv", "json"],
        default = "csv",
        help = "Output format: 'csv' or 'json'; default is 'csv'"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action = "store_true",
        help = "Enable verbose logging"
    )
    
    return parser.parse_args()

def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if not Path(filepath).is_file():
        logger.error(f"Input file is not found: {filepath}")
        return False

    logger.info(f"Input file validated: {filepath}")
    return True
    
def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    
    logger.debug(
        f"Arguments parsed: input = {args.input}, output = {args.output}",
        f"format = {args.format}"
    )
    
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)
        
    try:
        df = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)
    
    df_original = df.copy()
    
    try:
        df_clean = process_data(df, config)
    except ValueError:
        sys.exit(1)
    
    report = create_cleaning_report(df_original, df_clean)
    print(report)
    logger.info(f"Processing complete: {report['rows_before']} -> {report['rows_after']} rows")
    
    df_clean.to_csv(args.output, index = False)
    logger.info(f"Saved clean data to {args.output}")
    
if __name__ == "__main__":
    main()