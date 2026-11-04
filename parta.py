import csv
import sys
import math
from pathlib import Path
from models import Castle


def read_csv():
    """Reads edinburgh_castle.csv row by row and instantiates Castle objects.

    Expects:
        No arguments. Relies on edinburgh_castle.csv in the directory tree.

    Returns:
        list[Castle]: A list of populated Castle objects.
    """
    castles = []
    
    # Path(__file__).resolve() locates this python file's absolute path.
    # .parents[2] navigates up 2 directory levels to find the root location of edinburgh_castle.csv.
    csv_path = Path(__file__).resolve().parents[2] / "edinburgh_castle.csv"

    # try/except block handles missing file errors gracefully without generating a traceback
    try:
        with open(csv_path, "r", newline="") as file:
            # csv.DictReader uses the CSV header line to turn each row into a dictionary key-value map
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric string fields into floats before passing to Castle constructor
                castle = Castle(
                    row["date"],
                    float(row["max_temp_c"]),
                    float(row["max_wind_mph"])
                )
                castles.append(castle)
    except FileNotFoundError:
        # Print helpful user message and exit cleanly with status code 1
        print(f"Error: The data file '{csv_path.name}' could not be found.")
        sys.exit(1)

    return castles


def calculate_mean(value, dataset):
    """Calculates the mean value for a given weather metric.

    Expects:
        value (str): Attribute name to average ("max_temp_c" or "max_wind_mph").
        dataset (list[Castle]): List of Castle data instances.

    Returns:
        str: Mean value formatted to 1 decimal place, or None if dataset is empty.
    """
    # Guard clause: returns None if the provided list contains no data
    if not dataset:
        return None

    total = 0.0
    for castle in dataset:
        # Check which attribute to sum up based on the value parameter
        if value == "max_wind_mph":
            total += castle.max_wind_mph
        elif value == "max_temp_c":
            total += castle.max_temp_c
        else:
            # Raise explicit ValueError if an invalid column name is requested
            raise ValueError("Value must be 'max_wind_mph' or 'max_temp_c'")

    # Calculate average after loop finishes accumulating all rows
    mean = total / len(dataset)
    
    # Return string formatted to 1 decimal place
    return f"{mean:.1f}"


def find_extreme(value, dataset):
    """Finds the maximum value for a metric and records the earliest date it occurred.

    Expects:
        value (str): Attribute name to evaluate ("max_temp_c" or "max_wind_mph").
        dataset (list[Castle]): List of Castle data instances.

    Returns:
        str: Description string "VALUE on DATE", or None if dataset is empty.
    """
    # Guard clause: handle empty dataset safely
    if not dataset:
        return None

    # Initialize comparison baseline using the first record in the dataset
    if value == "max_wind_mph":
        max_val = dataset[0].max_wind_mph
    elif value == "max_temp_c":
        max_val = dataset[0].max_temp_c
    else:
        raise ValueError("Value must be 'max_wind_mph' or 'max_temp_c'")

    max_date = dataset[0].date

    # Slice dataset[1:] to iterate through remaining days starting from the second entry
    for castle in dataset[1:]:
        if value == "max_wind_mph":
            current_val = castle.max_wind_mph
        elif value == "max_temp_c":
            current_val = castle.max_temp_c

        # Strict '>' comparison ensures that if a tie occurs, max_val is NOT overwritten,
        # thereby retaining the earlier date as required by specification
        if current_val > max_val:
            max_val = current_val
            max_date = castle.date

    return f"{max_val} on {max_date}"


def build_report_text(csvdata):
    """Formats the summary weather report into a multi-line string.

    Expects:
        csvdata (list[Castle]): List of Castle data instances.

    Returns:
        str: Formatted report ready for printing or writing.
    """
    if not csvdata:
        return "No data available to report."

    # Derive total count and chronological date boundaries
    num_days = len(csvdata)
    period_start = csvdata[0].date
    period_end = csvdata[-1].date

    # Build multiline f-string containing overall report metadata and calculated weather stats
    report = f"""Edinburgh Castle Station:
Period covered: {period_start} to {period_end}
Total days of data: {num_days}
Average highest temperature is {calculate_mean("max_temp_c", csvdata)} celsius
Average maximum wind speed is {calculate_mean("max_wind_mph", csvdata)} mph
Highest recorded temperature was {find_extreme("max_temp_c", csvdata)}
Highest wind speed in mph was {find_extreme("max_wind_mph", csvdata)}"""

    return report


def save_report_text(report_content):
    """Writes the formatted report text to castle_report.txt.

    Expects:
        report_content (str): Text string to be saved.

    Returns:
        None
    """
    # Open file in write mode ("w"), creating it or overwriting existing contents
    with open("castle_report.txt", "w") as file:
        file.write(report_content)


def test_calculations():
    """Validates calculation logic against ordinary and edge-case (tie) datasets."""
    # Standard test dataset matching specification verification example
    test_data = [
        Castle("2025-11-01", 6.0, 20.0),
        Castle("2025-11-02", 8.0, 30.0),
        Castle("2025-11-03", 10.0, 25.0)
    ]

    # Use math.isclose() when comparing calculated floating-point numbers to avoid precision issues
    assert math.isclose(float(calculate_mean("max_temp_c", test_data)), 8.0)
    assert math.isclose(float(calculate_mean("max_wind_mph", test_data)), 25.0)
    assert find_extreme("max_temp_c", test_data) == "10.0 on 2025-11-03"
    assert find_extreme("max_wind_mph", test_data) == "30.0 on 2025-11-02"

    # Awkward case test: Tie scenario where two days share identical high values
    tie_data = [
        Castle("2025-11-01", 12.0, 15.0),
        Castle("2025-11-02", 12.0, 10.0)
    ]
    # Asserts that the earlier date ('2025-11-01') is retained during ties
    assert find_extreme("max_temp_c", tie_data) == "12.0 on 2025-11-01"

    print("All assertions passed successfully.")


def main():
    # 1. Run local test suite assertions first
    test_calculations()

    # 2. Read dataset from CSV file
    csvdata = read_csv()

    # 3. Construct formatted string report
    report = build_report_text(csvdata)

    # 4. Print report to terminal output and save copy to text file
    print(report)
    save_report_text(report)


# Guard ensures script execution sequence runs only when executed directly, not when imported
if __name__ == "__main__":
    main()