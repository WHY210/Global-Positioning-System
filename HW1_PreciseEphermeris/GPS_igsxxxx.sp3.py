# coding=utf-8
####2022全球定位系統概論HW1第8題:精密星曆之衛星速度加速度-時間圖
####by:WHY/2022.3.18


###前置作業:我不會爬蟲之類的一直失敗所以只能手動:)
import webbrowser
print("是針對精密星曆的，作業igsxxxxx.sp3的那題！但只要資料格式相同應該也是可以用，但後面程式碼有標住#*#的五處要改檔名。")
if int(input("\n\n###STEP1 查詢GPS week\n直接前往網站按1，不要就隨便按:")) == 1:
    webbrowser.open("https://geodesy.noaa.gov/CORS/Gpscal.shtml" )
gpsweek = input("GPS week : ")
dayoftheweek = input("星期幾（打數字）: ")
print("\n###STEP2 於CDDIS網站下載精密星曆")
print("登入CDDIS網站，點選Data and Produsts -> GNSS -> Product holdings -> Precise orbits")
print("ctrl+F尋找所求的GPS week的資料夾，點選以打開資料夾")
print("ctrl+F尋找所求的檔案 igs%s%s.sp3.Z，點選以下載" %(gpsweek, dayoftheweek))                #*#
if int(input("直接前往網站中Precise orbits頁面按1，不要就隨便按:")) == 1:
    webbrowser.open("https://cddis.nasa.gov/archive/gnss/products" )
print("\n###STEP3 資料前處理")
print("以7-zip或WinRAR解壓縮，成為igs%s%s.sp3" %(gpsweek, dayoftheweek))                       #*#
print("以EXCEL開啟sp3檔，並刪除前面22列 (從日期以下保留)")
print("選取第一欄全部，以資料剖析(資料 -> 資料剖析)讓資料以空格分配至每一格")
print("轉存成csv檔:igs%s%s.csv \n\n" %(gpsweek, dayoftheweek))                                #*#
path = input("存放檔案的路徑:").replace("\\", "\\\\")
import os
if not os.path.exists(path): os.mkdir(path)
os.chdir(path)


###資料讀取與初步處理

##讀取CSV檔 
import pandas as pd
file = "igs" + gpsweek + dayoftheweek                                                        #*#
igs = pd.read_csv(file + ".csv")

##詢問要幾顆衛星
amount = int(input("要取前幾筆衛星: "))
SatelliteAmount = int(input("當天共幾顆衛星(打開檔案來看！目前應該都是32): "))

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
igs.to_csv("igs%s_new.csv" %(file), index=False)                                              #*#


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
        os.chdir("../")
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
print("\n\n圖好了可以交作業了讚")