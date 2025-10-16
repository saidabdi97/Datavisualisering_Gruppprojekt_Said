import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px


# ---------- Diagram 1: Könsfördelning (Topp 10)
def gender_graph():
    df = pd.read_excel("data/Utbildningsansökning_age.xlsx", sheet_name='Education')

    for col in ['Total', 'Women', 'Men']:
        df[col] = df[col].astype(str).str.replace(' ', '').astype(int)

    df_filtered = df[df['Year'].isin([2023, 2024])].copy()
    df_filtered['TotalApplicants'] = df_filtered['Women'] + df_filtered['Men']

    df_grouped = df_filtered.groupby('Education').agg(
        Women=('Women', 'sum'),
        Men=('Men', 'sum'),
        TotalApplicants=('TotalApplicants', 'sum')
    ).reset_index()

    top_10 = df_grouped.sort_values(by='TotalApplicants', ascending=True).tail(10)

    melted = top_10.melt(
        id_vars=['Education'],
        value_vars=['Women', 'Men'],
        var_name='Gender',
        value_name='Applicants'
    )

    fig = px.bar(
        melted,
        x='Applicants',
        y='Education',
        color='Gender',
        barmode='overlay',
        orientation='h',
        color_discrete_map={'Women': '#60a5fa', 'Men': '#94a3b8'},
        labels={'Applicants': 'Antal sökande', 'Education': 'Utbildningsområde', 'Gender': 'Kön'}
    )

    fig.update_layout(
        height=600,
        xaxis_title='',
        yaxis_title='',
        legend_title='Kön',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showline=True, linewidth=1, linecolor='grey', ticks='outside'),
        yaxis=dict(tickfont=dict(color='#334850', size=13)),
        hoverlabel=dict(font=dict(color='#0b2d39', family="Inter", size=15))
    )
    return fig


# ---------- Diagram 2: Åldersfördelning
def age_graph():
    df = pd.read_excel("data/Utbildningsansökning_age.xlsx", sheet_name="Age")
    df.columns = df.columns.str.strip()

    df_melted = df.melt(
        id_vars=["Age groups"],
        value_vars=["Women", "Men"],
        var_name="Gender",
        value_name="Applications"
    )

    fig = px.bar(
        df_melted,
        x="Age groups",
        y="Applications",
        color="Gender",
        barmode="group",
        labels={"Applications": "Antal ansökningar", "Age groups": "Åldersgrupper"},
        color_discrete_map={"Women": "#60a5fa", "Men": "#94a3b8"}
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(font=dict(color='#0b2d39', family="Inter", size=15)),
        yaxis=dict(showline=True, linecolor='grey', ticks="outside")
    )
    return fig


# ---------- Initiera grafer
gender_chart = gender_graph()
age_chart = age_graph()

# ---------- Sida
with tgb.Page() as gender_age:
    with tgb.part(class_name="container card stack-large overview-page"):
        tgb.navbar()

        tgb.text("# Demografisk översikt", mode="md")
        tgb.text(
            """
Här visas köns- och åldersfördelningen bland de som ansökt till yrkeshögskoleutbildningar.  
Data hämtas från **Utbildningsansökning_age.xlsx** och uppdateras löpande.
""",
            mode="md"
        )

        with tgb.part(class_name="card"):
            tgb.text("### 👩‍💼 Män vs. Kvinnor – Topp 10 utbildningsområden (2023–2024)", mode="md")
            tgb.chart(figure='{gender_chart}')

        with tgb.part(class_name="card"):
            tgb.text("### 👥 Åldersfördelning bland sökande (2022–2024)", mode="md")
            tgb.chart(figure='{age_chart}')

        with tgb.part(class_name="card"):
            tgb.image("assets/images/storytelling_aldergrupp.png", width="1000px")
