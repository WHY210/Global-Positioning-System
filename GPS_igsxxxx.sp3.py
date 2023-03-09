# coding=utf-8

####2022全球定位系統概論HW1第8題:精密星曆之衛星速度加速度-時間圖
####by:WHY/2022.3.18


###前置作業:我不會寫程式所以只能手動:)

print("\n\n查詢GPS week (上網打GPS week對照)。")
gpsweek = input("GPS week = ")
gpsday = input("week day = ")
import webbrowser
print("\n於CDDIS網站下載精密星曆:登入CDDIS網站，點選Data and Produsts -> GNSS -> Produc holdings -> Precise orbits")
print("ctrl+F尋找所求的GPS week的資料夾，點選以打開資料夾")
print("ctrl+F尋找所求的檔案 : igsxxxxx.sp3.Z (xxxxx = GPS week + 星期幾 例如2022/02/05星期六為igs21956.sp3.Z)，點選以下載")
if int(input("\n直接前往網站按1，不要就隨便按:")) == 1:
    webbrowser.open("https://cddis.nasa.gov/archive/gnss/products" )
print("\n以7-zip或WinRAR解壓縮:igsxxxxx.sp3")
print("以EXCEL開啟sp3檔，並刪除前面22列 (從日期出現開始保留)，選取第一欄全部")
print("以資料剖析(資料 -> 資料剖析)讓資料以空格分配至每一格")
print("轉存成csv檔:igsxxxxx.csv \n\n")
import time
time.sleep(3)


###資料讀取與初步處理

##檔案存放絕對路徑 ("..."內為存放的資料夾位置，把檔案放那！)
import os
Directory = os.getcwd()
path = str(Directory + "\\GPS_PreciseOrbits")
if not os.path.exists(path): os.mkdir(path)
os.chdir(path)

##讀取CSV檔 (不是igsxxxxx.csv就自己改)
import pandas as pd
file = "igs" + gpsweek + gpsday 
igs = pd.read_csv(file + ".csv")

##詢問要幾顆衛星
amount = int(input("要取前幾筆衛星? "))
SatelliteAmount = int(input("當天總共幾顆衛星? "))

##刪除行，只保留各項要取的衛星:PG01/PG02/PG03...
#00/01/02
#33/34/35
#66/67/68
for j in range(0,24*4*(SatelliteAmount+1)):
    if j % (SatelliteAmount+1) > (amount-1):
        igs.drop(index = [j], inplace = True)  

##更改index row
igs.columns = ['ID','x(km)','y(km)','z(km)','clock(ms)','x-sdev(mm)','y-sdev(mm)','z-sdev(mm)','c-sdev(ps)']

##刪除列，只保留XYZ座標
igs.drop(columns= ['clock(ms)','x-sdev(mm)','y-sdev(mm)','z-sdev(mm)','c-sdev(ps)'], inplace = True)
#print(igs)

##輸出整理後的新檔案
igs.to_csv("igs%s_new.csv" %(file), index=False)



###class事前準備
##import
import matplotlib.pyplot as plt
##路徑
if not os.path.exists('v-t'):
    os.mkdir('v-t')
path_vt = (path + '\\v-t')
os.chdir(path)
if not os.path.exists('a-t'): 
    os.mkdir('a-t')
path_at = (path + '\\a-t')
        
###class
class PreciseEphemeris:
    ### 建構式
    def __init__(self, lst, coordinate, satellite):
        self.lst = lst     ##list屬性
        self.coordinate = coordinate    ## 坐標屬性
        self.satellite = satellite      ## 衛星屬性

    ###方法
    def speed(self):    ##計算速度
        lst_v = []
        for i in range(0,24*4-1):
            lst_v.append((float(self.lst[amount*(i+1)+self.satellite-1])-float(self.lst[amount*i+self.satellite-1]))/(15*60)) 
        return lst_v
    def acceleration(self, lst_v): ##計算加速度
        lst_a = []
        for i in range(0,94):
            lst_a.append((float(lst_v[i+1])-float(lst_v[i]))/(15*60))
        return lst_a
    def plot_vt(self, lst_v):   ##畫v-t圖
        ##更改存圖路徑
        os.chdir(path_vt)
        ##v-t圖
        time = [time for time in range (0,86400-900,900)]
        plt.figure(figsize=(10,6))
        plt.plot(time, lst_v)
        plt.title(f'PG0{self.satellite}:V{self.coordinate}-t')
        plt.xlabel('time(sec)')
        plt.ylabel('speed(km/s)')
        plt.savefig(f"PG0{self.satellite}_V{self.coordinate}-t.png")
        #plt.show()
        os.chdir(Directory)
    def plot_at(self, lst_a):   ##畫a-t圖
        ##更改存圖路徑
        os.chdir(path_at)
        ##a-t圖
        time = [time for time in range (0,86400-1800,900)]
        plt.figure(figsize=(10,6))
        plt.plot(time, lst_a)
        plt.title(f'PG0{self.satellite}:A{self.coordinate}-t')
        plt.xlabel('time(sec)')
        plt.ylabel('speed(km/s)')
        plt.savefig(f"PG0{self.satellite}_A{self.coordinate}-t.png")
        #plt.show()        
        os.chdir(Directory)


#將x/y/z之dataframe轉成list
lst_x = igs['x(km)'].tolist() 
lst_y = igs['y(km)'].tolist() 
lst_z = igs['z(km)'].tolist() 

def x(PG):
    X = PreciseEphemeris(lst_x, "x", PG)
    X.speed()
    lst_v = X.speed()
    X.acceleration(lst_v)
    lst_a = X.acceleration(lst_v)
    X.plot_vt(lst_v)
    X.plot_at(lst_a)
    
def y(PG):
    Y = PreciseEphemeris(lst_y, "y", PG)
    Y.speed()
    lst_v = Y.speed()
    Y.acceleration(lst_v)
    lst_a = Y.acceleration(lst_v)
    Y.plot_vt(lst_v)
    Y.plot_at(lst_a)

def z(PG):
    Z = PreciseEphemeris(lst_z, "z", PG)
    Z.speed()
    lst_v = Z.speed()
    Z.acceleration(lst_v)
    lst_a = Z.acceleration(lst_v)
    Z.plot_vt(lst_v)
    Z.plot_at(lst_a)


for j in range(amount):
    x(j+1)
    y(j+1)
    z(j+1)
print("\n\n好了可以交作業了讚")
