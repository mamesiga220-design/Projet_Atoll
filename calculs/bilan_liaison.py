def calc_eirp(tx_power_dbm, ant_gain_dbi, cable_loss_db):
    """EIRP = P_tx + G_ant - L_câble (dBm)"""
    return tx_power_dbm + ant_gain_dbi - cable_loss_db


def calc_mapl(eirp, sensitivity_dbm, fading_margin_db, pc_gain_db, sho_gain_db):
    """MAPL = EIRP - Sensibilité_UE - M_fading + G_PC + G_SHO (dB)"""
    return eirp - sensitivity_dbm - fading_margin_db + pc_gain_db + sho_gain_db