"""Helper file to open and save the formatted file."""
import pandas as pd


def format_locations(extension, *format_filters):
    """Open, format and save the locations."""
    df = pd.read_excel(
        "data/Locations/FarmerLocationExtract4Interns.xlsx", engine="openpyxl"
    )

    # Drops the nan value rows and applies the filter to the P1_Longitude and P1_Latitude columns.
    for column_name in ["P1_Longitude", "P1_Latitude"]:
        df = df[df[column_name].notna()]
        for format_filter in format_filters:
            df[column_name] = df[column_name].apply(format_filter)

    # Save the result of the applied filters.
    writer = pd.ExcelWriter(
        f"data/Locations/FarmerLocationExtract4Interns_{extension}.xlsx",
        engine="xlsxwriter",
    )
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()
