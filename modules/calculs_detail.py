import streamlit as st


def afficher(r, p):
    st.header("② Calculs détaillés")

    # Bilan de liaison
    st.subheader("Étape 1 — Bilan de liaison (Link Budget)")
    st.code(f"""
EIRP = P_tx + G_ant − L_câble
     = {p['tx_power']} + {p['ant_gain']} − {p['cable_loss']}
     = {r['eirp']} dBm

MAPL = EIRP − Sensibilité_UE − M_fading + G_PC + G_SHO
     = {r['eirp']} − ({p['sensitivity']}) − {p['fading_margin']} + {p['pc_gain']} + {p['sho_gain']}
     = {r['mapl']} dB
""", language="text")

    col1, col2 = st.columns(2)
    col1.metric("EIRP", f"{r['eirp']} dBm")
    col2.metric("MAPL", f"{r['mapl']} dB")

    st.divider()

    # COST-Hata
    st.subheader("Étape 2 — Rayon cellulaire (Modèle COST-Hata)")
    st.code(f"""
Facteur correction hauteur mobile a(hM) :
  a(hM) = 3.2 × (log(11.75 × hM))² − 4.97   [f > 1 GHz]
        = {r.get('a_hm', '—')} dB

Modèle COST-Hata :
  Lu(d) = 69.55 + 26.16·log(f) − 13.82·log(hB) − a(hM)
          + (44.9 − 6.55·log(hB)) × log(d)

Résolution numérique (dichotomie) : Lu(R) = MAPL
  → R              = {r['rayon_km']} km
  → Perte au rayon = {r['perte_rayon']} dB
  → Aire cellule   = 2.6 × R² = {r['aire_cellule']} km²
""", language="text")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rayon R", f"{r['rayon_km']} km")
    col2.metric("Perte au rayon", f"{r['perte_rayon']} dB")
    col3.metric("Aire cellule", f"{r['aire_cellule']} km²")

    st.divider()

    # Capacité
    st.subheader("Étape 3 — Dimensionnement capacitaire")
    st.code(f"""
Trafic total = Surface × Densité × Pénétration × Activité × Débit_cible
             = {p['surface']} × {p['densite_pop']} × {p['penetration']/100} × {p['activite']/100} × {p['debit_cible']} Mbps
             = {r['trafic_mbps']} Mbps

Débit_cellule = BW × Efficacité_spectrale × Nb_antennes_MIMO
              = {p['bw']} × {p['spec_eff']} × {p['mimo']}
              = {r['debit_cellule']} Mbps

Sites_capacité = ⌈ {r['trafic_mbps']} / ({r['debit_cellule']} × {p['secteurs']}) ⌉
               = {r['sites_cap']}
""", language="text")

    col1, col2, col3 = st.columns(3)
    col1.metric("Trafic total", f"{r['trafic_mbps']} Mbps")
    col2.metric("Débit/cellule", f"{r['debit_cellule']} Mbps")
    col3.metric("Sites (capacité)", r['sites_cap'])