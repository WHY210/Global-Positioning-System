import math

## 大地坐標系統 (φ,λ,h) 轉 地心地固坐標系統 (X,Y,Z)
# 已知項輸入區 : 大地坐標系統 (φ,λ,h)
lat  = str(input("大地緯度 φ (度 分 秒, N+/S-) = ")).split()
lon  = str(input("大地經度 λ (度 分 秒, E+/W-) = ")).split()
h    = float(input("大地橢球高 h (m)= ") )
lat = ((int(lat[0])*3600+int(lat[1])*60+int(lat[2]))/3600)*math.pi/180
lon = ((int(lon[0])*3600+int(lon[1])*60+int(lon[2]))/3600)*math.pi/180
geodetic = (lat, lon, h) 

# GRS80橢球體 長半徑a(m) / 扁率f / 離心率e
a = 6387137
f = 1/298.257222101
e = (2*f-f**2)**0.5

# 卯酉圈曲率半徑 N
N = a/(1-(e*math.sin(lat))**2)**0.5

# 所求 : 地心地固坐標系統 (X,Y,Z)
X = (N+h)*math.cos(lat)*math.cos(lon)
Y = (N+h)*math.cos(lat)*math.sin(lon)
Z = (N*(1-e**2)+h)*math.sin(lat)

print("ANS: ",X,Y,Z)