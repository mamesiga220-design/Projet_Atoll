import math


def facteur_correction_hm(freq_mhz, h_mobile=1.5):
    """Facteur de correction hauteur antenne mobile a(hM)"""
    if freq_mhz <= 1000:
        return 8.29 * (math.log10(1.54 * h_mobile)) ** 2 - 1.1
    else:
        return 3.2 * (math.log10(11.75 * h_mobile)) ** 2 - 4.97


def hata_path_loss(d_km, freq_mhz, h_base=25.0, h_mobile=1.5, env="urbain"):
    """
    Pertes de propagation COST-Hata (dB)
    Extension COST 231 pour f > 2000 MHz
    """
    correction = 0.0
    f = freq_mhz

    if freq_mhz > 2000:
        correction = 26 * math.log10(freq_mhz / 2000)
        f = 2000

    ahm = facteur_correction_hm(f, h_mobile)

    Lu = (
        69.55
        + 26.16 * math.log10(f)
        - 13.82 * math.log10(h_base)
        - ahm
        + (44.9 - 6.55 * math.log10(h_base)) * math.log10(d_km)
    )

    if env == "suburbain":
        Lu -= 2 * (math.log10(f / 28)) ** 2 + 5.4
    elif env == "rural":
        Lu -= (
            4.78 * (math.log10(f)) ** 2
            - 18.33 * math.log10(f)
            + 40.94
        )

    return Lu + correction


def calc_rayon_cellulaire(mapl, freq_mhz, h_base=25.0, h_mobile=1.5, env="urbain"):
    """
    Résolution numérique par dichotomie :
    Trouver R tel que Lu(R) = MAPL
    """
    lo, hi = 0.01, 100.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if hata_path_loss(mid, freq_mhz, h_base, h_mobile, env) < mapl:
            lo = mid
        else:
            hi = mid
    return mid


def courbe_propagation(freq_mhz, h_base, env, d_min=0.1, d_max=15.0, nb_points=150):
    """Retourne (distances, pertes) pour tracé graphique"""
    distances = [
        round(d_min + (d_max - d_min) * i / (nb_points - 1), 3)
        for i in range(nb_points)
    ]
    pertes = [
        hata_path_loss(d, freq_mhz, h_base, env=env)
        for d in distances
    ]
    return distances, pertes