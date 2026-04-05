import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/sales_data.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 FreshBite Foods Co. Sales Dashboard",
            style={"textAlign": "center"}),

    # Filters
    html.Div([
        html.Div([
            html.Label("Select City:"),
            dcc.Dropdown(
                id="city-filter",
                options=[{"label": c, "value": c} for c in df["City"].unique()],
                value=df["City"].unique().tolist(),
                multi=True
            )
        ], style={"width": "45%", "display": "inline-block"}),

        html.Div([
            html.Label("Select Category:"),
            dcc.Dropdown(
                id="category-filter",
                options=[{"label": c, "value": c} for c in df["Category"].unique()],
                value=df["Category"].unique().tolist(),
                multi=True
            )
        ], style={"width": "45%", "display": "inline-block"})
    ]),

    html.Br(),

    # KPI Cards
    html.Div([
        html.Div(id="total-revenue", style={
            "width": "30%", "display": "inline-block",
            "textAlign": "center", "padding": "20px",
            "border": "1px solid #ddd"
        }),

        html.Div(id="total-quantity", style={
            "width": "30%", "display": "inline-block",
            "textAlign": "center", "padding": "20px",
            "border": "1px solid #ddd"
        }),

        html.Div(id="avg-price", style={
            "width": "30%", "display": "inline-block",
            "textAlign": "center", "padding": "20px",
            "border": "1px solid #ddd"
        })
    ], style={"textAlign": "center"}),

    html.Br(),

    # Charts
    dcc.Graph(id="revenue-bar"),
    dcc.Graph(id="sales-line"),
    dcc.Graph(id="category-pie")
])


@app.callback(
    Output("revenue-bar", "figure"),
    Output("sales-line", "figure"),
    Output("category-pie", "figure"),
    Output("total-revenue", "children"),
    Output("total-quantity", "children"),
    Output("avg-price", "children"),
    Input("city-filter", "value"),
    Input("category-filter", "value")
)
def update_dashboard(selected_cities, selected_categories):

    filtered_df = df[
        (df["City"].isin(selected_cities)) &
        (df["Category"].isin(selected_categories))
    ]

    if filtered_df.empty:
        return (
            px.bar(title="No data"),
            px.line(title="No data"),
            px.pie(title="No data"),
            "No Data", "No Data", "No Data"
        )

    # KPI calculations
    total_revenue = filtered_df["Revenue"].sum()
    total_quantity = filtered_df["Quantity"].sum()
    avg_price = round(filtered_df["Price"].mean(), 2)

    # Bar chart (Revenue per Product)
    bar_fig = px.bar(
        filtered_df,
        x="Product",
        y="Revenue",
        color="City",
        title="Revenue by Product"
    )

    # Line chart (Sales over time)
    line_fig = px.line(
        filtered_df,
        x="Date",
        y="Revenue",
        color="City",
        title="Revenue Over Time"
    )

    # Pie chart (Category share)
    pie_fig = px.pie(
        filtered_df,
        names="Category",
        title="Sales by Category"
    )

    return (
        bar_fig,
        line_fig,
        pie_fig,
        f"💰 Total Revenue: ₱{total_revenue:,}",
        f"📦 Total Quantity: {total_quantity}",
        f"💲 Avg Price: ₱{avg_price}"
    )


if __name__ == "__main__":
    app.run(debug=True)