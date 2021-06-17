"""Helper file to open a file, format it and save the new version."""
from typing import List

import pandas as pd


def format_locations(format_name: str, relative_path: str, *filters: List[str]):
    """Open format and save the locations.

    Parameters
    ----------
    format_name
        The save file format name.

    relative_path
        The relative path to read and write the xlsx files.

    *filters
        A list of filters to apply.
    """
    df = pd.read_excel(
        f"{relative_path}data/Locations/FarmerLocationExtract4Interns.xlsx",
        engine="openpyxl",
    )

    #: Drops the nan value rows and applies the filter to the P1_Longitude and P1_Latitude columns.
    for column_name in ["P1_Longitude", "P1_Latitude"]:
        df = df[df[column_name].notna()]
        for fltr in filters:
            df[column_name] = df[column_name].apply(fltr)

    #: Save the result of the applied filters.
    writer = pd.ExcelWriter(
        f"{relative_path}data/Locations/FarmerLocationExtract4Interns_{format_name}.xlsx",
        engine="xlsxwriter",
    )
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()
