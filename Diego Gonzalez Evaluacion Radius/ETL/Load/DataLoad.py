import os
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
import logging
import configparser
from datetime import datetime as dt


path_actual = os.path.dirname(os.path.abspath(__file__))
path_config = os.path.join(path_actual, '..', 'Config', 'config.ini')

config = configparser.ConfigParser()
config.read(path_config)


# Configuramos logging para mantener control de las transacciones
logging.basicConfig(filename='flujo_data.log', level=logging.INFO)

# CONSTANTES PARA LAS VARIABLES CREADAS
DB_USERNAME = config['MySQL']['DB_USERNAME']
DB_PASSWORD = config['MySQL']['DB_PASSWORD']
DB_HOST     = config['MySQL']['DB_HOST']
DB_PORT     = config['MySQL']['DB_PORT']
DB_NAME     = config['MySQL']['DB_NAME']

engine = create_engine(f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

csv_dir = str(Path.cwd() / 'CleanFiles')
 

def insert_csv_data(csv, table_name):
    try:
        fecha = dt.now().strftime("%Y%m%d")
        file_out = f'{fecha}_{csv}'
        
        df = pd.read_csv(os.path.join(csv_dir, file_out))

        validate_data(df, table_name)

        with engine.connect() as connection:
            with connection.begin():
                    df.to_sql(name=table_name, con=connection, index=False, if_exists="replace")
                    logging.info(f"Carga existosa de archivo: {csv_file}, tabla: {table_name}.")
    except pd.errors.EmptyDataError:
        logging.warning(f"archivo CSV {csv_file} vacio!")
    except pd.errors.ParserError as e:
        logging.error(f"Error en parsing del archivo: {csv_file}: {str(e)}")
    except Exception as e:
        logging.error(f"Error en carga de tabla {table_name}: {str(e)}")

def validate_data(df, table_name):
    columnas = pd.read_sql(f"DESCRIBE {table_name}", engine)['Field'].tolist()
    # Validamos columnas
    if not set(df.columns).issubset(set(columnas)):
        raise ValueError(f"Error en columnas tabla: {table_name}")
def main():
    try:
        # Hacemos un loop por el directorio
        archivos_csv = [f'{fecha}_SalesOrderDetail.csv',
                        f'{fecha}_SalesOrderHeader.csv',
                        f'{fecha}_SalesTerritory.csv',
                        f'´{fecha}_SalesTerritoryHistory.csv']

        for csv_file in archivos_csv:
            table_name = os.path.splitext(csv_file)[0]

            # llamamos la funcion de insertar 
            insert_csv_data(csv_file, table_name)

        logging.info("Carga exitosa.")
    except Exception as e:
        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()