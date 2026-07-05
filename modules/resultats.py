import streamlit as st


def afficher(r):
    st.header("③ Résultats du dimensionnement")

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sites gNB requis",  r["n_sites"],           f"Dimensionnant : {r['facteur']}")
    col2.metric("Rayon cellulaire",  f"{r['rayon_km']} km")
    col3.metric("MAPL",              f"{r['mapl']} dB")
    col4.metric("Couverture zone",   f"{r['couverture_pct']}%", "objectif ≥ 95%")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Couverture")
        statut = (
            "✅ Satisfaisant (≥ 95%)" if r["couverture_pct"] >= 95
            else "⚠️ Partiel (80–95%)" if r["couverture_pct"] >= 80
            else "❌ Insuffisant (< 80%)"
        )
        data_cov = {
            "Paramètre": [
                "EIRP", "MAPL", "Perte au rayon R",
                "Rayon cellulaire R", "Aire cellule hex.",
                "Sites (couverture)", "Statut couverture"
            ],
            "Valeur": [
                f"{r['eirp']} dBm",
                f"{r['mapl']} dB",
                f"{r['perte_rayon']} dB",
                f"{r['rayon_km']} km",
                f"{r['aire_cellule']} km²",
                str(r['sites_cov']),
                statut,
            ]
        }
        st.table(data_cov)

    with col2:
        st.subheader("Capacité")
        data_cap = {
            "Paramètre": [
                "Population zone", "Utilisateurs 5G",
                "Utilisateurs actifs", "Trafic total",
                "Débit/cellule", "Sites (capacité)"
            ],
            "Valeur": [
                f"{r['population']:,} hab.",
                f"{r['users_5g']:,}",
                f"{r['users_actifs']:,}",
                f"{r['trafic_mbps']} Mbps",
                f"{r['debit_cellule']} Mbps",
                str(r['sites_cap']),
            ]
        }
        st.table(data_cap)

    st.divider()
    st.subheader("Conclusion")

    col1, col2 = st.columns([1, 2])
    col1.metric("Facteur dimensionnant", r["facteur"])
    col1.metric("Sites retenus (gNB)",   r["n_sites"])

    if r["facteur"] == "Couverture":
        col2.info(
            "**La contrainte géographique domine.**\n\n"
            "Leviers d'optimisation :\n"
            "- Passer à une bande plus basse (700 MHz) pour augmenter le rayon cellulaire\n"
            "- Augmenter la hauteur des antennes gNB\n"
            "- Réduire la marge de fading avec diversité d'antennes"
        )
    else:
        col2.info(
            "**La demande trafic domine.**\n\n"
            "Leviers d'optimisation :\n"
            "- Massive MIMO 64×64 pour multiplier le débit par cellule\n"
            "- Cell splitting pour densifier le réseau\n"
            "- Augmenter la largeur de bande NR (200 MHz)"
        )