# wilayah.py

class Wilayah:
    """
    Representasi satu wilayah (Desa atau Kecamatan) beserta atribut terkait harga.
    """

    def __init__(self, nama, kecamatan=None, harga=None):
        self.nama = nama
        self.kecamatan = kecamatan
        self.harga = harga

    def get_kategori(self):
        """
        Menentukan kategori harga berdasarkan nilai harga.
        """
        if self.harga is None:
            return "Tidak diketahui"
        elif self.harga >= 2_500_000:
            return "Sangat Tinggi"
        elif self.harga >= 1_750_000:
            return "Tinggi"
        elif self.harga >= 1_000_000:
            return "Sedang"
        else:
            return "Rendah"

    def get_warna(self):
        """
        Menentukan warna wilayah berdasarkan kategori harga.
        """
        if self.harga is None:
            return "#bdbdbd"  # Abu-abu
        elif self.harga >= 2_500_000:
            return "#e41a1c"  # Merah
        elif self.harga >= 1_750_000:
            return "#ff7f00"  # Oranye
        elif self.harga >= 1_000_000:
            return "#4daf4a"  # Hijau
        else:
            return "#377eb8"  # Biru

    def get_opacity(self):
        """
        Menentukan transparansi layer peta berdasarkan nilai harga.
        """
        if self.harga is None:
            return 0.6
        elif self.harga >= 2_500_000:
            return 0.8
        elif self.harga >= 1_750_000:
            return 0.7
        elif self.harga >= 1_000_000:
            return 0.6
        else:
            return 0.5

    def to_dict(self):
        """
        Untuk debug atau representasi data dalam format dictionary.
        """
        return {
            "nama": self.nama,
            "kecamatan": self.kecamatan,
            "harga": self.harga,
            "kategori": self.get_kategori(),
            "warna": self.get_warna(),
            "opacity": self.get_opacity(),
        }