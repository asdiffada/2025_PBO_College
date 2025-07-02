import folium
import json
import pandas as pd
from shapely.geometry import shape
from wilayah import Wilayah
from utils import warna_kecamatan, warna_desa, opacity_harga

class GeoPeta:
    """
    Kelas untuk membuat layer GeoJSON ke dalam folium.Map dengan logika pewarnaan berdasarkan harga tanah.
    """

    def __init__(self, path_geojson, df_data, tipe='desa'):
        self.tipe = tipe 
        self.df = df_data.copy()
        self.geojson = self._load_geojson(path_geojson)

    def _load_geojson(self, path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)

    def get_layer(self, highlight_nama=None, search_mode=None):
        """
        Menghasilkan layer GeoJson untuk dimasukkan ke peta folium.
        """
        return folium.GeoJson(
            self.geojson,
            name=self.tipe.capitalize(),
            style_function=lambda feature: self._style_function(feature, highlight_nama, search_mode),
            highlight_function=lambda feature: self._highlight_function(feature, highlight_nama, search_mode),
            tooltip=self._get_tooltip()
        )

    def _style_function(self, feature, highlight_nama, search_mode):
        props = feature['properties']
        nama = props['Desa'] if self.tipe == 'desa' else props['Kecamatan']
        kecamatan = props.get('Kecamatan', None)

        harga = self._ambil_harga(nama)
        wilayah = Wilayah(nama, kecamatan, harga)

        tampilkan = False
        if search_mode == 'Kecamatan' and self.tipe == 'desa' and highlight_nama:
            tampilkan = kecamatan == highlight_nama
        elif search_mode == 'Desa' and self.tipe == 'desa' and highlight_nama:
            tampilkan = nama == highlight_nama
        elif self.tipe == 'kecamatan':
            tampilkan = True

        if tampilkan:
            return {
                'fillColor': wilayah.get_warna(),
                'color': "#00000000",
                'weight': 0,
                'fillOpacity': wilayah.get_opacity(),
            }
        else:
            return {
                'fillColor': "#ffffff00",
                'color': "#00000000",
                'weight': 0,
                'fillOpacity': 0,
            }

    def _highlight_function(self, feature, highlight_nama, search_mode):
        props = feature['properties']
        nama = props['Desa'] if self.tipe == 'desa' else props['Kecamatan']
        kecamatan = props.get('Kecamatan', None)

        harga = self._ambil_harga(nama)
        wilayah = Wilayah(nama, kecamatan, harga)

        fill = warna_desa(harga) if self.tipe == 'desa' else warna_kecamatan(nama, self.df['Kecamatan'].unique().tolist())

        return {
            "fillColor": fill,
            "color": "#000000", 
            "weight": 2,
            "fillOpacity": 0.7,
        }
        cocok = False
        if self.tipe == 'desa' and search_mode == 'Desa' and highlight_nama == nama:
            cocok = True
        elif self.tipe == 'desa' and search_mode == 'Kecamatan' and kecamatan == highlight_nama:
            cocok = True
        elif self.tipe == 'kecamatan' and search_mode == 'Kecamatan' and highlight_nama == nama:
            cocok = True

        if cocok:
            return {
                'fillColor': wilayah.get_warna(),
                'color': "#00000000",
                'weight': 1,
                'fillOpacity': min(wilayah.get_opacity() + 0.2, 1),
            }
        else:
            return {
                'fillColor': "#ffffff00",
                'color': "#00000000",
                'weight': 0,
                'fillOpacity': 0,
            }

    def _ambil_harga(self, nama):
        kolom = 'Desa' if self.tipe == 'desa' else 'Kecamatan'
        row = self.df[self.df[kolom] == nama]
        return row.iloc[0]['Harga'] if not row.empty and 'Harga' in row.columns else None

    def _get_tooltip(self):
        if self.tipe == 'desa':
            return folium.GeoJsonTooltip(fields=["Desa", "Kecamatan"], sticky=True)
        else:
            return folium.GeoJsonTooltip(fields=["Kecamatan"], sticky=True)
