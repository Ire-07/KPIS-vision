#normalizar datos 
def normalizar_columnas(df):
    """
    Convierte nombres de columnas a minúsculas
    y elimina espacios.
    """
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )
    return df
