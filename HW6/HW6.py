import math

## 大地坐標系統 (φ,λ,h) 轉 地心地固坐標系統 (X,Y,Z)
# 已知項輸入區 : 大地坐標系統 (φ,λ,h)
lat  = str(input("大地緯度 φ (度 分 秒, N+/S-) = ")).split()
lon  = str(input("大地經度 λ (度 分 秒, E+/W-) = ")).split()
h    = float(input("大地橢球高 h (m)= ") )
lat = ((int(lat[0])*3600+int(lat[1])*60+int(lat[2]))/3600)*math.pi/180
lon = ((int(lon[0])*3600+int(lon[1])*60+int(lon[2]))/3600)*math.pi/180
geodetic = [lat, lon, h]
print("大地坐標 = ", geodetic)

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
geocentric = [X,Y,Z]
print("ANS: 地心地固坐標 = ", geocentric)




## 地心地固坐標系統 (X,Y,Z) 疊代反算 大地坐標系統 (φ,λ,h) 

D = (X**2+Y**2)**0.5
lon = math.atan2(Y,X)

#疊代
h = 0
for i in range(1000):
    lat = math.atan(Z/(D*(1-e**2)))
    N = a/(1-(e*math.sin(lat))**2)**0.5
    h = D/math.cos(lat)-N
    lat = math.atan(Z*(N+h)/(D*((1-e**2)*N+h)))
    N = a/(1-(e*math.sin(lat))**2)**0.5
    h = D/math.cos(lat)-N

#所求 : 大地坐標系統 (φ,λ,h) -弧度 
geodetic = [lat, lon, h]
print("ANS: 大地坐標 (弧度) = ", geodetic)

#所求 : 大地坐標系統 (φ,λ,h) -度分秒 
lat = (lat*180/math.pi)%3600
lat_degree = int(lat)
lat_minute = int((lat-int(lat))*60)
lat_second = int(((lat-int(lat))*60-int((lat-int(lat))*60))*60)
lat = "%s°%s\'%s\"" %(lat_degree, lat_minute, lat_second)
lon = (lon*180/math.pi)%3600
lon_degree = int(lon)
lon_minute = int((lon-int(lon))*60)
lon_second = int(((lon-int(lon))*60-int((lon-int(lon))*60))*60)
lon = "%s°%s\'%s\"" %(lon_degree, lon_minute, lon_second)
print("             (度分秒) = [%s, %s, %s]" %(lat, lon, h))