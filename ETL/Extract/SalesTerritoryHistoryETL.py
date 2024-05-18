#!/usr/bin/env python
# coding: utf-8



def ETL():
    import polars as pl
    from pathlib import Path
    from datetime import datetime as dt



    PATH = str(Path.cwd() / 'Raw')
    FILE = 'SalesTerritoryHistory'
    EXT = '.csv'

    fullPath = PATH + '//' + FILE+EXT


    schema = {
    'BusinessEntityID': pl.Int32,
    'TerritoryID_KEY': pl.Int32,
    'StartDate': pl.Utf8,
    'EndDate': pl.Utf8,
    'rowguid': pl.Utf8,
    'ModifiedDate': pl.Date
}
    df = pl.read_csv(fullPath,
                    schema = schema,
                    has_header = False,
                    separator= '\t',
                    quote_char = '"',
                    ignore_errors=True)


    ruta = Path.cwd() / 'CleanFiles'
    fecha = dt.now().strftime("%Y%m%d")
    file_out = f'{fecha}_{FILE}{EXT}'

    df.write_csv(str(ruta) + '\\' + file_out)

if __name__ == '__main__':
    ETL()