import streamlit as st
import pandas as pd


def afficher():
    st.header("⑤ Processus de dimensionnement NG-RAN 5G")

    etapes = [
        (
            "1", "Définition des exigences de service",
            "Identification des cas d'usage 5G : **eMBB** (Enhanced Mobile Broadband), "
            "**URLLC** (Ultra-Reliable Low Latency Communications), "
            "**mMTC** (Massive Machine Type Communications). "
            "Chaque cas impose des contraintes différentes sur le débit, la latence et la fiabilité."
        ),
        (
            "2", "Estimation de la demande trafic",
            "Trafic agrégé = Population × Taux de pénétration × Facteur d'activité × Débit cible. "
            "Le facteur d'activité (busy hour ratio) représente le pourcentage d'utilisateurs "
            "simultanément actifs en heure chargée."
        ),
        (
            "3", "Bilan de liaison (Link Budget)",
            "**EIRP = P_tx + G_ant − L_câble**\n\n"
            "**MAPL = EIRP − Sensibilité_UE − M_fading + G_PC + G_SHO**\n\n"
            "La MAPL (Maximum Allowable Path Loss) est la perte maximale tolérée "
            "sur le trajet radio. Elle détermine la portée maximale de la cellule."
        ),
        (
            "4", "Modèle de propagation & rayon cellulaire",
            "Le modèle **COST-Hata** est utilisé pour les environnements macro-cellulaires "
            "(urbain, suburbain, rural). Pour 3.5 GHz (5G NR), une correction logarithmique "
            "est appliquée (COST 231 Hata). Le rayon R est obtenu par **résolution numérique "
            "(dichotomie)** de : Lu(R) = MAPL."
        ),
        (
            "5", "Nombre de sites par couverture",
            "Aire cellule hexagonale = **2.6 × R²**\n\n"
            "Nb_sites = ⌈ Surface / (Aire_cellule × Nb_secteurs) ⌉\n\n"
            "La géométrie hexagonale minimise les zones non couvertes entre cellules adjacentes."
        ),
        (
            "6", "Capacité cellulaire & nombre de sites",
            "Débit_cellule = BW × Efficacité_spectrale × Nb_antennes_MIMO\n\n"
            "Nb_sites_capacité = ⌈ Trafic_total / (Débit_cellule × Secteurs) ⌉\n\n"
            "Le Massive MIMO augmente le débit sans augmenter la bande passante "
            "(multiplexage spatial)."
        ),
        (
            "7", "Choix du dimensionnant & optimisation",
            "N_sites_final = max(sites_couverture, sites_capacité)\n\n"
            "Le facteur dimensionnant oriente les leviers d'optimisation : "
            "changement de bande, tilt électrique, beamforming, cell splitting, small cells."
        ),
    ]

    for num, titre, desc in etapes:
        with st.expander(f"Étape {num} — {titre}", expanded=True):
            st.markdown(desc)

    st.divider()
    st.subheader("Justification des paramètres d'entrée")

    df = pd.DataFrame([
        ["Bande n78 — 3.5 GHz",  "3500 MHz",       "Bande pivot 5G NR FR1 — équilibre couverture/capacité, spectre mondial (3GPP TS 38.104)"],
        ["Puissance gNB",         "46 dBm (40 W)",  "Puissance typique gNB macro conforme 3GPP TS 38.104 §6.2.1"],
        ["Gain antenne",          "18 dBi",          "Antenne directionnelle sectorielle 65° — standard macro 5G/LTE"],
        ["Sensibilité UE",        "−105 dBm",        "3GPP TS 38.101-1, UE NR Cat. M, BW 100 MHz, NF = 7 dB"],
        ["Marge de fading",       "10 dB",           "Log-normal shadowing σ = 8 dB → probabilité de couverture ≥ 90% (ITU-R M.2135)"],
        ["Massive MIMO 8×8",      "8 antennes",      "Gain de beamforming spatial — multiplexage sans augmentation de puissance"],
        ["Efficacité spectrale",  "5.4 bits/s/Hz",   "64-QAM, code rate 3/4 — valeur moyenne eMBB 5G NR urbain (3GPP TR 38.913)"],
        ["Taux pénétration",      "30%",             "Hypothèse réaliste en phase de déploiement initial 5G"],
        ["Facteur d'activité",    "20%",             "Busy hour ratio standard — 20% des abonnés actifs simultanément (UIT-T E.501)"],
    ], columns=["Paramètre", "Valeur par défaut", "Justification"])

    st.dataframe(df, use_container_width=True, hide_index=True)