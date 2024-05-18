#!/usr/bin/env python
# coding: utf-8

def ETL(): 
    """Funcion que toma archivos 'raw' y deposita en el directorio CleanFiles para cargar a la bd"""
    import polars as pl
    from pathlib import Path
    from datetime import datetime as dt



    file = 'SalesOrderDetail.csv'
    ruta = Path.cwd() / 'Raw' / file # Se crea un objeto de WindowsPath relativo al cwd
    dtypes = {'column_8': pl.Float64} # se forza a tomar la columna 8 como float

    schema =  {
    'SalesOrderID': pl.Int32,
    'SalesOrderDetailID': pl.Int32,
    'CarrierTrackingNumber': pl.Utf8,
    'OrderQTY': pl.Int32,
    'ProductID': pl.Int32,
    'SpecialOfferID': pl.Int32,
    'UnitPrice': pl.Float64,
    'UnitPriceDiscount': pl.Float64,
    'LineTotal': pl.Float64,
    'rowguid': pl.Utf8,
    'ModifiedDate': pl.Utf8
                                }
    df = pl.read_csv(ruta, 
    schema = schema,
    separator = '\t',
    has_header = False,
    dtypes = dtypes)


    fecha = dt.now().strftime("%Y%m%d")
    file_out = f'{fecha}_{file}'

    sink = Path.cwd() / 'CleanFiles' / file_out
    df.write_csv(sink)

if __name__ == "__main__":
    ETL()