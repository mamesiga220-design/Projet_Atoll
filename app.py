import streamlit as st
from calculs.dimensionnement import dimensionner
from calculs.propagation import facteur_correction_hm
from modules.export_pdf import bouton_export

# ── Configuration page
st.set_page_config(
    page_title="Dimensionnement NG-RAN 5G",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS professionnel
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}
.header-band {
    background: linear-gradient(135deg, #1a2744 0%, #0066cc 100%);
    padding: 24px 32px;
    border-radius: 12px;
    margin-bottom: 24px;
    color: white;
}
.header-band h1 {
    font-size: 28px;
    font-weight: 700;
    margin: 0;
}
.header-band p {
    font-size: 14px;
    opacity: 0.8;
    margin: 4px 0 0 0;
}
[data-testid="stMetric"] {
    background: #f0f4ff;
    border: 1px solid #c4d9f5;
    border-radius: 10px;
    padding: 16px;
}
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #0066cc, #004499);
    color: white;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
}
[data-testid="stTabs"] button {
    font-size: 14px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ── Initialisation session
if "p" not in st.session_state:
    st.session_state.p = {
        "surface": 50.0,
        "densite_pop": 12000.0,
        "penetration": 25,
        "activite": 15,
        "debit_cible": 100.0,
        "freq": 3500,
        "tx_power": 46,
        "ant_gain": 18,
        "cable_loss": 2.0,
        "sensitivity": -105,
        "fading_margin": 10.0,
        "pc_gain": 3.0,
        "sho_gain": 0.0,
        "bw": 100,
        "secteurs": 3,
        "mimo": 8,
        "spec_eff": 5.4,
        "env": "urbain",
        "h_base": 25,
    }

if "resultats" not in st.session_state:
    st.session_state.resultats = None

# ── Import modules
from modules import parametres, calculs_detail, resultats, graphique, processus

# ── En-tête
st.markdown("""
<div class="header-band">
    <h1>📡 Dimensionnement NG-RAN 5G</h1>
    <p>Application de planification radio — Master 1 SRT · Département Génie Informatique · ESP/UCAD · Dakar, Sénégal</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Actions")

    if st.button("▶ Lancer le dimensionnement", type="primary", use_container_width=True):
        with st.spinner("Calcul en cours..."):
            try:
                r = dimensionner(st.session_state.p)
                r["a_hm"] = round(facteur_correction_hm(st.session_state.p["freq"]), 4)
                st.session_state.resultats = r
                st.success("✅ Calcul terminé !")
            except Exception as e:
                st.error(f"Erreur : {e}")

    if st.session_state.resultats:
        r = st.session_state.resultats
        st.divider()
        st.markdown("### 📊 Résumé rapide")
        st.metric("Sites gNB",        r["n_sites"])
        st.metric("Rayon cellulaire",  f"{r['rayon_km']} km")
        st.metric("MAPL",              f"{r['mapl']} dB")
        st.metric("Couverture",        f"{r['couverture_pct']}%")
        st.caption(f"Dimensionnant : **{r['facteur']}**")
        st.divider()
        bouton_export(st.session_state.resultats, st.session_state.p)

    st.divider()
    st.markdown("### ℹ️ À propos")
    st.caption("Modèle : COST-Hata\nNorme : 3GPP TS 38.104 / TR 38.913\nVersion : 1.0")

# ── Onglets
tabs = st.tabs([
    "① Paramètres",
    "② Calculs détaillés",
    "③ Résultats",
    "④ Graphique",
    "⑤ Processus"
])

with tabs[0]:
    parametres.afficher()

with tabs[1]:
    if st.session_state.resultats:
        calculs_detail.afficher(st.session_state.resultats, st.session_state.p)
    else:
        st.info("Lancez le dimensionnement depuis la barre latérale pour voir les calculs détaillés.")

with tabs[2]:
    if st.session_state.resultats:
        resultats.afficher(st.session_state.resultats)
    else:
        st.info("Lancez le dimensionnement depuis la barre latérale pour voir les résultats.")

with tabs[3]:
    if st.session_state.resultats:
        graphique.afficher(st.session_state.resultats, st.session_state.p)
    else:
        st.info("Lancez le dimensionnement depuis la barre latérale pour voir le graphique.")

with tabs[4]:
    processus.afficher()