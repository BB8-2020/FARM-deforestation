"""Helper file to open and save the formatted file."""
from typing import List

import pandas as pd


def format_locations(format_name: str, *filters: List[str]):
    """Open format and save the locations.

    Parameters
    ----------
    format_name
        The save file format name.

    *filters
        A list of filters to apply.

    """
    df = pd.read_excel(
        "../../data/Locations/FarmerLocationExtract4Interns.xlsx", engine="openpyxl"
    )

    #: Drops the nan value rows and applies the filter to the P1_Longitude and P1_Latitude columns.
    for column_name in ["P1_Longitude", "P1_Latitude"]:
        df = df[df[column_name].notna()]
        for fltr in filters:
            df[column_name] = df[column_name].apply(fltr)

    #: Save the result of the applied filters.
    writer = pd.ExcelWriter(
        f"../../data/Locations/FarmerLocationExtract4Interns_{format_name}.xlsx",
        engine="xlsxwriter",
    )
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()
