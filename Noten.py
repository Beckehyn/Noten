import streamlit as st
import pandas as pd

# -----------------------------
# Seitenkonfiguration
# -----------------------------
st.set_page_config(
    page_title="Notenrechner Unterstufe",
    layout="wide"
)

# -----------------------------
# CSS für dunklere Tabelle
# -----------------------------
st.markdown("""
<style>
    table {
        background-color: #f0f2f6;
    }
    th {
        background-color: #d9dde5;
        font-weight: bold;
        text-align: center;
    }
    td {
        background-color: #f7f8fa;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Konstanten
# -----------------------------
FÄCHER = ["Deutsch", "Mathe", "Latein", "Englisch", "Kunst"]
LEISTUNGEN = ["KA1", "KA2", "KA3", "mündl.", "Referate"]
AUSWAHL = ["-", 1, 2, 3, 4, 5, 6]

GEWICHTE = {
    "KA": 0.4,
    "mündl.": 0.5,
    "Referate": 0.1
}

# -----------------------------
# Session State
# -----------------------------
if "seite" not in st.session_state:
    st.session_state.seite = "eingabe"

if "daten" not in st.session_state:
    st.session_state.daten = pd.DataFrame(
        [["-" for _ in LEISTUNGEN] for _ in FÄCHER],
        columns=LEISTUNGEN,
        index=FÄCHER
    )

# -----------------------------
# Funktionen
# -----------------------------
def berechne_zeugnisnote(zeile):
    ka_noten = [
        int(n) for n in [zeile["KA1"], zeile["KA2"], zeile["KA3"]]
        if n != "-"
    ]

    mündl = zeile["mündl."]
    ref = zeile["Referate"]

    gesamt = 0
    gewicht_summe = 0

    if ka_noten:
        gesamt += (sum(ka_noten) / len(ka_noten)) * GEWICHTE["KA"]
        gewicht_summe += GEWICHTE["KA"]

    if mündl != "-":
        gesamt += int(mündl) * GEWICHTE["mündl."]
        gewicht_summe += GEWICHTE["mündl."]

    if ref != "-":
        gesamt += int(ref) * GEWICHTE["Referate"]
        gewicht_summe += GEWICHTE["Referate"]

    if gewicht_summe == 0:
        return "-"

    return round(gesamt / gewicht_summe, 2)

# -----------------------------
# Seite 1: Eingabe
# -----------------------------
if st.session_state.seite == "eingabe":
    st.title("📘 Notenrechner – Unterstufe")
    st.write("Trage deine bisherigen Noten ein:")

    st.session_state.daten = st.data_editor(
        st.session_state.daten,
        column_config={
            col: st.column_config.SelectboxColumn(
                col,
                options=AUSWAHL
            ) for col in LEISTUNGEN
        },
        use_container_width=True
    )

    st.markdown("---")

    if st.button("📊 Zeugnisnoten anzeigen"):
        st.session_state.seite = "ergebnis"
        st.rerun()

# -----------------------------
# Seite 2: Ergebnisanzeige
# -----------------------------
if st.session_state.seite == "ergebnis":
    col1, col2 = st.columns([10, 1])

    with col2:
        if st.button("↩️"):
            st.session_state.seite = "eingabe"
            st.rerun()

    st.title("📊 Aktuelle Zeugnisnoten")

    ergebnis = {}
    gültige_noten = []

    for fach in FÄCHER:
        note = berechne_zeugnisnote(st.session_state.daten.loc[fach])
        ergebnis[fach] = note
        if note != "-":
            gültige_noten.append(note)

    ergebnis_df = pd.DataFrame.from_dict(
        ergebnis,
        orient="index",
        columns=["Zeugnisnote"]
    )

    st.table(ergebnis_df)

    # -----------------------------
    # Gesamtdurchschnitt
    # -----------------------------
    st.markdown("---")

    if gültige_noten:
        gesamt_durchschnitt = round(
            sum(gültige_noten) / len(gültige_noten), 2
        )
        st.subheader(f"📌 ⌀ Gesamtdurchschnitt: **{gesamt_durchschnitt}**")
    else:
        st.subheader("📌 ⌀ Gesamtdurchschnitt: **-**")
