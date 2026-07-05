import streamlit as st


def generer_texte(r, p):
    texte = f"""
DIMENSIONNEMENT NG-RAN 5G
Master 1 SRT - ESP/UCAD - Dakar, Senegal
==========================================

RESULTATS DU DIMENSIONNEMENT
------------------------------
Sites gNB requis       : {r['n_sites']}
Facteur dimensionnant  : {r['facteur']}
Rayon cellulaire       : {r['rayon_km']} km
Aire cellule hex.      : {r['aire_cellule']} km2
MAPL                   : {r['mapl']} dB
EIRP                   : {r['eirp']} dBm
Perte au rayon R       : {r['perte_rayon']} dB
Couverture zone        : {r['couverture_pct']} %
Sites (couverture)     : {r['sites_cov']}
Sites (capacite)       : {r['sites_cap']}
Population zone        : {r['population']:,} hab.
Utilisateurs 5G        : {r['users_5g']:,}
Utilisateurs actifs    : {r['users_actifs']:,}
Trafic total           : {r['trafic_mbps']} Mbps
Debit par cellule      : {r['debit_cellule']} Mbps

PARAMETRES D'ENTREE
------------------------------
Surface zone           : {p['surface']} km2
Densite population     : {p['densite_pop']} hab/km2
Taux penetration 5G    : {p['penetration']} %
Facteur activite       : {p['activite']} %
Debit cible/user       : {p['debit_cible']} Mbps
Frequence              : {p['freq']} MHz
Puissance gNB          : {p['tx_power']} dBm
Gain antenne           : {p['ant_gain']} dBi
Pertes cables          : {p['cable_loss']} dB
Sensibilite UE         : {p['sensitivity']} dBm
Marge fading           : {p['fading_margin']} dB
Bande passante NR      : {p['bw']} MHz
Configuration MIMO     : {p['mimo']}x{p['mimo']}
Secteurs par site      : {p['secteurs']}
Eff. spectrale         : {p['spec_eff']} bits/s/Hz
Environnement          : {p['env']}
Hauteur gNB            : {p['h_base']} m

BILAN DE LIAISON
------------------------------
EIRP = {p['tx_power']} + {p['ant_gain']} - {p['cable_loss']} = {r['eirp']} dBm
MAPL = {r['eirp']} - ({p['sensitivity']}) - {p['fading_margin']} + {p['pc_gain']} + {p['sho_gain']} = {r['mapl']} dB
Rayon R (COST-Hata)    : {r['rayon_km']} km
"""
    return texte


def bouton_export(r, p):
    texte = generer_texte(r, p)
    st.download_button(
        label="📄 Exporter les résultats (.txt)",
        data=texte,
        file_name="dimensionnement_ngran_5g.txt",
        mime="text/plain",
        use_container_width=True
    )