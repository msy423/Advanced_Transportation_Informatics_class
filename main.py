import pandas as pd
import folium
import time


#緯度経度が度分秒表記かつ整数化のために1000かけてるので、10進法緯度経度に直すための関数
def dms2dec(latlong_raw):
    var_degree = int(latlong_raw/1e7)
    var_minutes = int(latlong_raw/1e5 - var_degree*100) 
    var_seconds = (latlong_raw/1e3 - var_degree*1e4 - var_minutes*100)
    decimal_latlong = var_degree + var_minutes/60 + var_seconds/3600
    
    return decimal_latlong

#foliumに描画するデータを作成
def addLatLong2map(df_in, color_in, folium_map, legend_name):
    lgd_txt = '<span style="color: {col};">{txt}</span>'
    FeatureGroup_in = folium.FeatureGroup(name= lgd_txt.format( txt= legend_name, col= color_in))
    for index_df in range(len(df_in)):
        folium.CircleMarker([dms2dec(df_in["地点　緯度（北緯）"][index_df]), 
                             dms2dec(df_in["地点　経度（東経）"][index_df])],
                             radius=2,color=color_in,
                             fill=True,fill_opacity=0.9).add_to(FeatureGroup_in)
    folium_map.add_child(FeatureGroup_in)




accidents_data = pd.read_csv("./accidents_statistics2021/honhyo_2021.csv", encoding='cp932')

df_tokyo = accidents_data[accidents_data['都道府県コード']==30]

# create map
folium_map = folium.Map(location=[35.415377, 139.595271], zoom_start=11)

# 人対車両事故の抽出
df_person = df_tokyo[df_tokyo["事故類型"]==1].reset_index()
df_nodeath = df_person[df_person['死者数'] == 0].reset_index()
df_death = df_person[df_person['死者数'] > 0].reset_index()

#車対車
df_carVScar = df_tokyo[df_tokyo["事故類型"]==21].reset_index()
df_carVScar_nodeath = df_carVScar[df_carVScar['死者数'] == 0].reset_index()
df_carVScar_death = df_carVScar[df_carVScar['死者数'] > 0].reset_index()

#車両単独
df_caronly = df_tokyo[df_tokyo["事故類型"]==41].reset_index()
df_caronly_nodeath = df_caronly[df_caronly['死者数'] == 0].reset_index()
df_caronly_death = df_caronly[df_caronly['死者数'] > 0].reset_index()


start_time = time.time()

addLatLong2map(df_nodeath,'#f0a500',folium_map, 'pedestrian accident')
addLatLong2map(df_carVScar_nodeath,'#000080',folium_map, 'car vs car accident')
addLatLong2map(df_caronly_nodeath,'#32cd32',folium_map, 'car only accident')
print("--- %s seconds for accident loop ---" % (time.time() - start_time))

addLatLong2map(df_death,'#ff0000',folium_map, 'pedestrian death')
addLatLong2map(df_carVScar_death,'#00ffff',folium_map, 'car vs car death')
addLatLong2map(df_caronly_death,'#000000',folium_map, 'car only death')

# turn on layer control
folium_map.add_child(folium.map.LayerControl())

print("--- %s seconds for all loop ---" % (time.time() - start_time))

folium_map

# save map
folium_map.save('./JapanTrafficAccidents_statistics.html')
