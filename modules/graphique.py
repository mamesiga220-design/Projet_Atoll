import streamlit as st
import plotly.graph_objects as go
from calculs.propagation import courbe_propagation


def afficher(r, p):
    st.header("④ Courbe de propagation — COST-Hata")
    st.caption(
        f"Fréquence : {p['freq']} MHz  ·  "
        f"Environnement : {p['env']}  ·  "
        f"Hauteur gNB : {p['h_base']} m"
    )

    distances, pertes = courbe_propagation(p["freq"], p["h_base"], p["env"])

    fig = go.Figure()

    # Courbe des pertes
    fig.add_trace(go.Scatter(
        x=distances,
        y=pertes,
        mode="lines",
        name="Pertes COST-Hata (dB)",
        line=dict(color="#0066cc", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(0,102,204,0.07)"
    ))

    # Ligne MAPL
    fig.add_hline(
        y=r["mapl"],
        line_dash="dash",
        line_color="red",
        line_width=2,
        annotation_text=f"MAPL = {r['mapl']} dB",
        annotation_position="top right"
    )

    # Ligne rayon cellulaire
    fig.add_vline(
        x=r["rayon_km"],
        line_dash="dot",
        line_color="green",
        line_width=2,
        annotation_text=f"R = {r['rayon_km']} km",
        annotation_position="top right"
    )

    fig.update_layout(
        xaxis_title="Distance (km)",
        yaxis_title="Perte de trajet (dB)",
        legend=dict(orientation="h", y=-0.15),
        height=450,
        margin=dict(l=40, r=20, t=20, b=40),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "**Lecture du graphique :**\n\n"
        "- La **courbe bleue** représente les pertes de propagation selon COST-Hata.\n"
        "- La **ligne rouge pointillée** est la MAPL (perte maximale tolérée).\n"
        "- La **ligne verte pointillée** est le rayon cellulaire R : "
        "c'est l'intersection entre la courbe et la MAPL."
    )