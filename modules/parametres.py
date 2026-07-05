import streamlit as st


def afficher():
    st.header("① Paramètres d'entrée")
    st.info("Renseignez tous les paramètres puis cliquez sur **Lancer le dimensionnement** dans la barre latérale.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌍 Zone & Demande trafic")
        st.session_state.p["surface"]      = st.number_input("Surface de la zone (km²)", 0.1, 5000.0, float(st.session_state.p["surface"]), 0.5)
        st.session_state.p["densite_pop"]  = st.number_input("Densité de population (hab/km²)", 100.0, 50000.0, float(st.session_state.p["densite_pop"]), 500.0)
        st.session_state.p["penetration"]  = st.slider("Taux de pénétration 5G (%)", 1, 100, int(st.session_state.p["penetration"]))
        st.session_state.p["activite"]     = st.slider("Facteur d'activité simultanée (%)", 1, 100, int(st.session_state.p["activite"]))
        st.session_state.p["debit_cible"]  = st.number_input("Débit cible par utilisateur (Mbps)", 1.0, 10000.0, float(st.session_state.p["debit_cible"]), 10.0)

        st.subheader("🏙️ Environnement")
        env_map   = {"Urbain dense": "urbain", "Suburbain": "suburbain", "Rural": "rural"}
        env_label = st.selectbox("Type d'environnement", list(env_map.keys()))
        st.session_state.p["env"]    = env_map[env_label]
        st.session_state.p["h_base"] = st.number_input("Hauteur antenne gNB (m)", 10, 150, int(st.session_state.p["h_base"]))

    with col2:
        st.subheader("📶 Paramètres radio NR")
        freq_map = {
            "n78 — 3500 MHz (FR1, bande principale 5G)": 3500,
            "n1  — 2100 MHz (FR1, LTE/NR)":              2100,
            "n28 — 700  MHz (FR1, couverture rurale)":    700,
            "n3  — 1800 MHz (FR1)":                       1800,
        }
        freq_label = st.selectbox("Bande de fréquence", list(freq_map.keys()))
        st.session_state.p["freq"]          = freq_map[freq_label]
        st.session_state.p["tx_power"]      = st.number_input("Puissance d'émission gNB (dBm)", 20, 60, int(st.session_state.p["tx_power"]))
        st.session_state.p["ant_gain"]      = st.number_input("Gain antenne gNB (dBi)", 0, 30, int(st.session_state.p["ant_gain"]))
        st.session_state.p["cable_loss"]    = st.number_input("Pertes câbles & connecteurs (dB)", 0.0, 10.0, float(st.session_state.p["cable_loss"]), 0.5)
        st.session_state.p["sensitivity"]   = st.number_input("Sensibilité récepteur UE (dBm)", -130, -50, int(st.session_state.p["sensitivity"]))
        st.session_state.p["fading_margin"] = st.number_input("Marge de fading log-normal (dB)", 0.0, 20.0, float(st.session_state.p["fading_margin"]), 0.5)
        st.session_state.p["pc_gain"]       = st.number_input("Gain contrôle de puissance (dB)", 0.0, 10.0, float(st.session_state.p["pc_gain"]), 0.5)
        st.session_state.p["sho_gain"]      = st.number_input("Gain soft handover (dB)", 0.0, 6.0, float(st.session_state.p["sho_gain"]), 0.5)

        st.subheader("📡 Capacité NR")
        bw_map = {"100 MHz (NR FR1)": 100, "50 MHz": 50, "20 MHz": 20, "200 MHz": 200}
        bw_label = st.selectbox("Largeur de bande NR (MHz)", list(bw_map.keys()))
        st.session_state.p["bw"] = bw_map[bw_label]

        sect_map   = {"3 secteurs (trisectoriel)": 3, "6 secteurs": 6, "1 secteur": 1}
        sect_label = st.selectbox("Secteurs par site", list(sect_map.keys()))
        st.session_state.p["secteurs"] = sect_map[sect_label]

        mimo_map   = {"8×8 Massive MIMO": 8, "4×4 MIMO": 4, "2×2 MIMO": 2, "64×64 mMIMO": 64}
        mimo_label = st.selectbox("Configuration MIMO", list(mimo_map.keys()))
        st.session_state.p["mimo"] = mimo_map[mimo_label]

        st.session_state.p["spec_eff"] = st.number_input("Efficacité spectrale (bits/s/Hz)", 0.5, 15.0, float(st.session_state.p["spec_eff"]), 0.1)