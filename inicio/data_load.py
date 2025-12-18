# Carga un archivo CSV y devuelve un DataFrame.
import pandas as pd

def cargar_csv(ruta_archivo):
    
    df = pd.read_csv(ruta_archivo)
    return df