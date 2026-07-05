import math
from calculs.bilan_liaison import calc_eirp, calc_mapl
from calculs.propagation import calc_rayon_cellulaire, hata_path_loss


def calc_trafic(surface_km2, densite_pop, penetration_pct, activite_pct, debit_cible_mbps):
    """Estimation de la demande trafic agrégée"""
    population   = surface_km2 * densite_pop
    users_5g     = population * (penetration_pct / 100)
    users_actifs = users_5g   * (activite_pct   / 100)
    trafic_mbps  = users_actifs * debit_cible_mbps
    return {
        "population":   round(population),
        "users_5g":     round(users_5g),
        "users_actifs": round(users_actifs),
        "trafic_mbps":  round(trafic_mbps, 2),
    }


def calc_sites_couverture(surface_km2, rayon_km, nb_secteurs):
    """
    Nombre de sites par contrainte couverture
    Aire hexagonale = 2.6 × R²
    """
    aire_cellule = 2.6 * rayon_km ** 2
    sites = math.ceil(surface_km2 / (aire_cellule * nb_secteurs))
    return {
        "aire_cellule_km2": round(aire_cellule, 4),
        "sites_couverture": max(1, sites),
    }


def calc_capacite_cellule(bw_mhz, spec_eff, mimo):
    """Débit cellulaire (Mbps) = BW × Efficacité_spectrale × Nb_antennes_MIMO"""
    return round(bw_mhz * spec_eff * mimo, 2)


def calc_sites_capacite(trafic_mbps, debit_cellule_mbps, nb_secteurs):
    """Nombre de sites par contrainte capacité"""
    return max(1, math.ceil(trafic_mbps / (debit_cellule_mbps * nb_secteurs)))


def dimensionner(p):
    """
    Processus complet de dimensionnement NG-RAN 5G.
    p : dictionnaire de paramètres d'entrée
    Retourne tous les résultats intermédiaires et finaux.
    """
    # Étape 1 : Bilan de liaison
    eirp = calc_eirp(p["tx_power"], p["ant_gain"], p["cable_loss"])
    mapl = calc_mapl(eirp, p["sensitivity"], p["fading_margin"], p["pc_gain"], p["sho_gain"])

    # Étape 2 : Rayon cellulaire
    rayon = calc_rayon_cellulaire(mapl, p["freq"], p["h_base"], env=p["env"])
    perte_rayon = hata_path_loss(rayon, p["freq"], p["h_base"], env=p["env"])

    # Étape 3 : Couverture
    cov = calc_sites_couverture(p["surface"], rayon, p["secteurs"])

    # Étape 4 : Capacité
    traf = calc_trafic(
        p["surface"], p["densite_pop"],
        p["penetration"], p["activite"], p["debit_cible"]
    )
    debit_cellule = calc_capacite_cellule(p["bw"], p["spec_eff"], p["mimo"])
    sites_cap = calc_sites_capacite(traf["trafic_mbps"], debit_cellule, p["secteurs"])

    # Étape 5 : Dimensionnant
    n_sites = max(cov["sites_couverture"], sites_cap)
    facteur = "Couverture" if cov["sites_couverture"] >= sites_cap else "Capacité"

    # Étape 6 : Couverture réelle
    couverture_reelle = n_sites * cov["aire_cellule_km2"] * p["secteurs"]
    couverture_pct    = min(100.0, (couverture_reelle / p["surface"]) * 100)

    return {
        "eirp":          round(eirp, 2),
        "mapl":          round(mapl, 2),
        "perte_rayon":   round(perte_rayon, 2),
        "rayon_km":      round(rayon, 4),
        "aire_cellule":  cov["aire_cellule_km2"],
        "sites_cov":     cov["sites_couverture"],
        **traf,
        "debit_cellule": debit_cellule,
        "sites_cap":     sites_cap,
        "n_sites":       n_sites,
        "facteur":       facteur,
        "couverture_pct": round(couverture_pct, 1),
    }