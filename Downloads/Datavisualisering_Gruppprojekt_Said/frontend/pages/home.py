import taipy.gui.builder as tgb

with tgb.Page() as home_page:
    with tgb.part(class_name="container card stack-large home-page"):
        tgb.navbar()

        # KPI-kort (enkelt och stabilt)
        with tgb.part(class_name="card"):
            tgb.text("**Totala ansökningar:** {total_applications}", mode="md")
        with tgb.part(class_name="card"):
            tgb.text("**Antal kurser:** {num_courses}", mode="md")
        with tgb.part(class_name="card"):
            tgb.text("**Senast uppdaterad:** {last_update}", mode="md")

        # Huvudbeskrivning
        with tgb.part(class_name="max-text-width"):
            tgb.text("# YH-kollen – The Skool Dashboard", mode="md")
            tgb.text(
                """
YH-kollen är ett datadrivet beslutsstöd utvecklat av **The Skool**.  
Plattformen ger en tydlig, interaktiv överblick över yrkeshögskoleutbildningar i Sverige – baserat på data från **Myndigheten för yrkeshögskolan (MYH)** och **Statistiska centralbyrån (SCB)**.

### Med YH-kollen kan du:
- Följa ansökningsflöden och trender över tid  
- Utforska utbildningsområden, anordnare och demografiska mönster  
- Analysera utbildningar utifrån geografisk spridning och bidragsnivåer  

Välj en sektion i menyn för att börja din analys.
""",
                mode="md"
            )

    # Footer
    with tgb.part(class_name="footer"):
        tgb.text("© The Skool – YH-kollen", mode="md")
