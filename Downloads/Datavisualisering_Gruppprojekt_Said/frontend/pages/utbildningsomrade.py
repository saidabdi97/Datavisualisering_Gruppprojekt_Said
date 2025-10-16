import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px

# ---------- Line chart över tid
def student_area_graph():
    df = pd.read_excel("data/Antalet studerande i YH inom olika utbildningsområden 2012-2024.xlsx")
    df_long = df.melt(id_vars='År', var_name='Utbildningsområde', value_name='Antal studerande')

    blue_colors = [
        "#057DA8", "#39B8E4", "#839CF1", "#667fd2",
        "#2141ab", "#61BDB3", "#27C557", "#3b82f6", "#06b6d4"
    ]

    fig = px.line(
        df_long,
        x='År',
        y='Antal studerande',
        color='Utbildningsområde',
        labels={'År': 'År', 'Antal studerande': 'Antal studerande'},
        template='plotly_white',
        color_discrete_sequence=blue_colors
    )

    visible_areas = [
        "Ekonomi, administration och försäljning",
        "Teknik och tillverkning",
        "Hälso- och sjukvård samt socialt arbete",
        "Data/It"  # behåll exakt kolumnnamn som i filen
    ]
    for tr in fig.data:
        tr.visible = True if tr.name in visible_areas else "legendonly"

    fig.update_xaxes(showgrid=False, ticks="outside", showline=True, linecolor='grey', type='category')
    fig.update_yaxes(showgrid=False, ticks="outside", showline=True, linecolor='grey')
    fig.update_layout(legend_title_text='Utbildningsområde', xaxis_title='')
    return fig

student_area_graph = student_area_graph()

# ---------- Bar chart med år-väljare
_df = pd.read_excel("data/Antalet studerande i YH inom olika utbildningsområden 2012-2024.xlsx")
df_long = _df.melt(id_vars='År', var_name='Utbildningsområde', value_name='Antal studerande')
df_long['Utbildningsområde'] = df_long['Utbildningsområde'].astype(str).str.strip()

years = sorted(df_long['År'].dropna().astype(str).unique().tolist())
selected_year = years[-1]  # ✅ visa SENASTE år först

def make_figure(year):
    filtered = df_long[df_long['År'].astype(str) == year].copy()
    fig = px.bar(
        filtered,
        y='Utbildningsområde',
        x='Antal studerande',
        orientation='h',
        labels={'Utbildningsområde': 'Utbildningsområde', 'Antal studerande': 'Antal studerande'},
        template='plotly_white'
    )
    for tr in fig.data:
        tr.marker.color = '#51abcb'
    fig.update_layout(
        xaxis=dict(title='Antal studerande', showgrid=False, showline=True, linecolor='grey'),
        yaxis=dict(type='category', showgrid=False, showline=True, linecolor='grey'),
        margin=dict(t=40, b=40),
        yaxis_title=''
    )
    return fig

fig = make_figure(selected_year)

def update_figure(state):
    state.fig = make_figure(state.selected_year)

# ---------- Sida
with tgb.Page() as utbildningsomrade:
    with tgb.part(class_name="container card stack-large utbildning-page"):
        tgb.navbar()

        tgb.text(
            "## Studerande i YH – utveckling över tid\n"
            "Linjediagrammet visar trender i antalet studerande per utbildningsområde. "
            "Fyra största visas direkt; övriga kan aktiveras i legenden.",
            mode="md"
        )

        with tgb.part(class_name="card"):
            tgb.chart(figure="{student_area_graph}")

        with tgb.part(class_name="card"):
            tgb.text(
                "## Antalet studerande per utbildningsområde (valbart år)\n"
                "Välj år för att se fördelningen som stapeldiagram.",
                mode="md"
            )
            tgb.selector(
                label="Välj år",
                value="{selected_year}",
                lov=years,
                dropdown=True,
                on_change=update_figure
            )
            tgb.chart(figure="{fig}")

        with tgb.part(class_name="card"):
            tgb.image("assets/images/storytelling_Data_It.png", width="1000px")
