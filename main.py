import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geo_peta import GeoPeta

st.set_page_config("Geo Harga Tanah", layout="wide")
st.title("🗺️ Geo Harga Tanah Wilayah Kabupaten Semarang")

df_wilayah = pd.read_csv("data/data_wilayah_semarang.csv")
all_kec = sorted(df_wilayah['Kecamatan'].unique())
all_desa = sorted(df_wilayah['Desa'].unique())

geo_desa_path = "data/batas_desa_semarang.geojson"
geo_kec_path = "data/batas_kecamatan_semarang.geojson"

if "selected_kec" not in st.session_state:
    st.session_state.selected_kec = "(Pilih Area)"
if "selected_desa" not in st.session_state:
    st.session_state.selected_desa = "(Pilih Area)"

search_mode = st.radio("Cari berdasarkan:", ["Kecamatan", "Desa"], horizontal=True)
if search_mode == "Kecamatan":
    wilayah = st.selectbox("Pilih Kecamatan", ["(Pilih Area)"] + all_kec,
                           index=(["(Pilih Area)"] + all_kec).index(st.session_state.selected_kec))
else:
    wilayah = st.selectbox("Pilih Desa", ["(Pilih Area)"] + all_desa,
                           index=(["(Pilih Area)"] + all_desa).index(st.session_state.selected_desa))

highlight_kec = wilayah if search_mode == "Kecamatan" and wilayah != "(Pilih Area)" else None
highlight_desa = wilayah if search_mode == "Desa" and wilayah != "(Pilih Area)" else None

CENTER = [-7.2, 110.4]
ZOOM = 11
m = folium.Map(location=CENTER, zoom_start=ZOOM, control_scale=True)

peta_kec = GeoPeta(geo_kec_path, df_wilayah, tipe="kecamatan")
peta_desa = GeoPeta(geo_desa_path, df_wilayah, tipe="desa")

m.add_child(peta_kec.get_layer(highlight_kec, search_mode))
m.add_child(peta_desa.get_layer(highlight_desa, search_mode))

legend_html = """<div style="position: fixed; bottom: 40px; left: 40px; width: 270px; z-index:9999; font-size:14px; background:white; border:1px solid #888; padding:8px; color:#222;">
  <b>Kategori Harga Tanah</b><br>
  <div><i style="background:#e41a1c;width:18px;height:15px;display:inline-block;margin-right:8px;"></i> ≥ Rp 2.500.000 Sangat Tinggi</div>
  <div><i style="background:#ff7f00;width:18px;height:15px;display:inline-block;margin-right:8px;"></i> Rp 1.750.000 - 2.499.999 Tinggi</div>
  <div><i style="background:#4daf4a;width:18px;height:15px;display:inline-block;margin-right:8px;"></i> Rp 1.000.000 - 1.749.999 Sedang</div>
  <div><i style="background:#377eb8;width:18px;height:15px;display:inline-block;margin-right:8px;"></i> &lt; Rp 1.000.000 Rendah</div>
  <div><i style="background:#bdbdbd;width:18px;height:15px;display:inline-block;margin-right:8px;"></i> Tidak Ada Data</div>
</div>"""
m.get_root().html.add_child(folium.Element(legend_html))

map_data = st_folium(m, width=950, height=600, returned_objects=["last_active_drawing"])

info = None
wilayah_show = None
is_kecamatan = False

if map_data and map_data.get("last_active_drawing"):
    props = map_data["last_active_drawing"]["properties"]
    if search_mode == "Desa" and "Desa" in props:
        st.session_state.selected_desa = props["Desa"]
        wilayah_show = props["Desa"]
        info = df_wilayah[df_wilayah["Desa"] == wilayah_show]
        st.rerun()
    elif search_mode == "Kecamatan" and "Kecamatan" in props:
        st.session_state.selected_kec = props["Kecamatan"]
        wilayah_show = props["Kecamatan"]
        info = df_wilayah[df_wilayah["Kecamatan"] == wilayah_show]
        st.rerun()
elif wilayah != "(Pilih Area)":
    wilayah_show = wilayah
    if search_mode == "Kecamatan":
        info = df_wilayah[df_wilayah["Kecamatan"] == wilayah]
    else:
        info = df_wilayah[df_wilayah["Desa"] == wilayah]

if wilayah_show:
    st.subheader(f"ℹ️ Info {search_mode}: {wilayah_show}")
    st.write(info.T if info is not None and not info.empty else "Tidak ada data tersedia.")

st.markdown("---")
