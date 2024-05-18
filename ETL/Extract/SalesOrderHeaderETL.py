#!/usr/bin/env python
# coding: utf-8

def ETL(): 
    """Funcion que toma archivos 'raw' y deposita en el directorio CleanFiles para cargar a la bd"""
    import polars as pl
    from pathlib import Path
    from datetime import datetime as dt



    file = 'SalesOrderHeader.csv'
    ruta = Path.cwd() / 'Raw' / file # Se crea un objeto de WindowsPath relativo al cwd
    
    df = pl.read_csv(ruta, separator = '\t', has_header = False)

    ### se depuran columnas que no entran en el schema delimitado
    colNum = ['11','12','14','15','16','17','18','24']
    for num in colNum:
        df = df.drop(f'column_{num}')
    
    df.write_csv(ruta)
    schema =   {
    'SalesOrderID': pl.Utf8,
    'RevisionNumber': pl.Int64,
    'OrderDate': pl.Datetime,
    'DueDate': pl.Datetime,
    'Status': pl.Utf8,
    'OnlineOrderFlag': pl.Utf8,
    'SalesOrderNumber': pl.Utf8,
    'PurchaseOrderNumber': pl.Utf8,
    'AccountNumber': pl.Utf8,
    'TerritoryID': pl.Utf8,
    'CreditCardApprovalCode': pl.Utf8,
    'SubTotal': pl.Float64,
    'TaxAmt': pl.Float64,
    'Freight': pl.Float64,
    'TotalDue': pl.Float64,
    'Comment': pl.Utf8,
    'rowguid': pl.Utf8,
    'ModifiedDate': pl.Utf8
                            }
    df = pl.read_csv(ruta, schema = schema, has_header = True)


    fecha = dt.now().strftime("%Y%m%d")
    file_out = f'{fecha}_{file}'

    sink = Path.cwd() / 'CleanFiles' / file_out
    df.write_csv(sink)

if __name__ == "__main__":
    ETL()