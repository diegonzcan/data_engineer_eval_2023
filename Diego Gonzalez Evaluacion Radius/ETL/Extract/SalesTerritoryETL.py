#!/usr/bin/env python
# coding: utf-8


def ETL():
    """FUNCION para EL de SalesTerritory y generacion de schema"""
    import polars as pl
    from pathlib import Path
    from datetime import datetime as dt


    PATH = str(Path.cwd() / 'Raw')
    FILE = 'SalesTerritory'
    EXT = '.csv'

    fullPath = PATH + '//' + FILE+EXT
    schema = {
        'TerritoryID': pl.Int32,
        'Name': pl.Utf8,
        'CountryRegionCode': pl.Utf8,
        'Group': pl.Utf8,
        'SalesYTD': pl.Float64,
        'SalesLastYear': pl.Float64,
        'CostYTD': pl.Float64,
        'CostLastYear': pl.Float64,
        'rowguid': pl.Utf8,
        'ModifiedDate': pl.Utf8 
    }
    
    df = pl.read_csv(fullPath,
                     has_header = False, 
                    separator= '\t',
                    quote_char = '"',
                    ignore_errors=True, 
                    schema = schema
    )


    ruta = Path.cwd() / 'CleanFiles'
    fecha = dt.now().strftime("%Y%m%d")

    file_out = f'{fecha}_{FILE}{EXT}'

    df.write_csv(str(ruta) + '\\' + file_out)

if __name__ == '__main__':
    ETL()