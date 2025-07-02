import pandas as pd

PALET_KCM = [
    "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4",
    "#46f0f0", "#f032e6", "#bcf60c", "#fabebe", "#008080", "#e6beff",
    "#9a6324", "#fffac8", "#800000", "#aaffc3", "#808000", "#ffd8b1",
    "#000075", "#808080", "#a9a9a9"
]

def warna_kecamatan(nama_kec, all_kecamatan=None):
    """
    Menghasilkan warna tetap berdasarkan nama kecamatan.
    """
    if all_kecamatan is None:
        return "#cccccc"
    try:
        idx = all_kecamatan.index(nama_kec)
    except ValueError:
        idx = 0
    return PALET_KCM[idx % len(PALET_KCM)]

def warna_desa(harga):
    """
    Pewarnaan berdasarkan harga tanah.
    """
    if pd.isna(harga):
        return "#bdbdbd"
    elif harga >= 2_500_000:
        return "#e41a1c"
    elif harga >= 1_750_000:
        return "#ff7f00"
    elif harga >= 1_000_000:
        return "#4daf4a"
    else:
        return "#377eb8"

def opacity_harga(harga):
    """
    Transparansi wilayah berdasarkan harga tanah.
    """
    if pd.isna(harga):
        return 0.6
    elif harga >= 2_500_000:
        return 0.8
    elif harga >= 1_750_000:
        return 0.7
    elif harga >= 1_000_000:
        return 0.6
    else:
        return 0.5
