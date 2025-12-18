# gráficos interactivos
import plotly.express as px

def grafico_ventas_por_fecha(df):
    fig = px.line(
        df,
        x="fecha",
        y="monto",
        title="Evolución de Ventas"
    )
    return fig
