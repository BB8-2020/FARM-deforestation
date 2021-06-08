"""Helper file to open and save the formatted file."""
import pandas as pd


def format_locations(extension, *format_filters):
    """Open, format and save the locations."""
    df = pd.read_excel(
        "../../data/locations/FarmerLocationExtract4Interns.xlsx", engine="openpyxl"
    )

    for column_name in ["P1_Longitude", "P1_Latitude"]:
        df = df[df[column_name].notna()]
        for format_filter in format_filters:
            df[column_name] = df[column_name].apply(format_filter)

    writer = pd.ExcelWriter(
        f"../../data/locations/FarmerLocationExtract4Interns_{extension}.xlsx",
        engine="xlsxwriter",
    )
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()
