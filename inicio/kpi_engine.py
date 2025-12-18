# kpis de ventas y leads
import plotly.graph_objects as go


def kpis_ventas(self):
    total = self.df["monto"].sum()
    promedio = self.df["monto"].mean()
    cantidad = len(self.df)

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number",
        value=total,
        title={"text": "💰 Total Ventas"},
        domain={"row": 0, "column": 0}
    ))

    fig.add_trace(go.Indicator(
        mode="number",
        value=round(promedio, 2),
        title={"text": "🎯 Ticket Promedio"},
        domain={"row": 0, "column": 1}
    ))

    fig.add_trace(go.Indicator(
        mode="number",
        value=cantidad,
        title={"text": "📦 Cantidad de Ventas"},
        domain={"row": 0, "column": 2}
    ))

    fig.update_layout(
        grid={"rows": 1, "columns": 3, "pattern": "independent"}
    )

    return fig



def kpis_leads(self):
    total = len(self.df)
    ganados = len(self.df[self.df["estado"] == "ganado"])
    conversion = (ganados / total) * 100 if total > 0 else 0

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="number",
        value=total,
        title={"text": "👥 Total Leads"},
        domain={"row": 0, "column": 0}
    ))

    fig.add_trace(go.Indicator(
        mode="number",
        value=ganados,
        title={"text": "✅ Leads Ganados"},
        domain={"row": 0, "column": 1}
    ))

    fig.add_trace(go.Indicator(
        mode="number",
        value=round(conversion, 2),
        title={"text": "% Conversión"},
        domain={"row": 0, "column": 2}
    ))

    fig.update_layout(
        grid={"rows": 1, "columns": 3, "pattern": "independent"}
    )

    return fig
