####全球定位系統概論HW1第8題
####:by:WHY/2022.3.18

###前置作業
##STEP1:查詢GPS week (上網打GPS week對照)
##STEP2:於CDDIS網站下載精密星曆 
    # 點選"Data and Produsts" -> "GNSS" -> "Produc holdings" -> "Precise orbits"
    # https://cddis.nasa.gov/archive/gnss/products
    # 善用ctrl+F尋找所求的GPS week的資料夾
    # 善用ctrl+F尋找所求的檔案 : igsxxxxx.sp3.Z (xxxxx = GPS week + 星期幾 例如2022/02/05星期六為igs21956.sp3.Z)
##STEP3:以7-zip或WinRAR解壓縮 : igsxxxxx.sp3
##STEP4:把sp3檔轉存成csv檔 (更蓋副檔名) : igsxxxxx.csv
##STEP5:以EXCEL開啟並刪除前面22列 (從日期出現開始保留)
##STEP6:選取第一欄全部，以資料剖析("資料" -> "資料剖析")讓資料以空格分配至每一格


###檔案存放位置 ("..."內更改為你存放的資料夾位置，\改成/)
##更改檔案絕對路徑
import os
os.chdir("C:/Users/dulci/OneDrive - 國立陽明交通大學/大二/下/GPS/HW1/過程用的檔案")


###資料讀取與初步處理

##讀取CSV檔
import pandas as pd
igs = pd.read_csv("igs21956.csv")

##刪除行，只保留各項PG01/PG02/PG03
#00/01/02
#33/34/35
#66/67/68
for j in range(0,24*4*33):
    if j % 33 > 2:
        igs.drop(index = [j], inplace = True)  

##更改index row
igs.columns = ['ID','x(km)','y(km)','z(km)','clock(ms)','x-sdev(mm)','y-sdev(mm)','z-sdev(mm)','c-sdev(ps)']

##刪除列，只保留XYZ座標
igs.drop(columns= ['clock(ms)','x-sdev(mm)','y-sdev(mm)','z-sdev(mm)','c-sdev(ps)'], inplace = True)
#print(igs)

##輸出整理後的新檔案
igs.to_csv("igs21956_new.csv", index=False)


###計算X、Y、Z三分量速度及加速度

##將x/y/z之dataframe轉成list
lst_x = igs['x(km)'].tolist()
lst_y = igs['y(km)'].tolist()
lst_z = igs['z(km)'].tolist()

##PG01
lst_Vx_PG01 = []
for i in range(0,24*4-1):
    lst_Vx_PG01.append((float(lst_x[3*i+3])-float(lst_x[3*i]))/(15*60))
#print(lst_Vx_PG01)
lst_Vy_PG01 = []
for i in range(0,24*4-1):
    lst_Vy_PG01.append((float(lst_y[3*i+3])-float(lst_y[3*i])/(15*60)))
#print(lst_Vy_PG01)
lst_Vz_PG01 = []
for i in range(0,24*4-1):
    lst_Vz_PG01.append((float(lst_z[3*i+3])-float(lst_z[3*i]))/(15*60))
#print(lst_Vz_PG01)
lst_Ax_PG01 = []
for i in range(0,94):
    lst_Ax_PG01.append((float(lst_Vx_PG01[i+1])-float(lst_Vx_PG01[i]))/(15*60))
#print(lst_Ax_PG01)
lst_Ay_PG01 = []
for i in range(0,94):
    lst_Ay_PG01.append((float(lst_Vy_PG01[i+1])-float(lst_Vy_PG01[i]))/(15*60))
#print(lst_Ay_PG01)
lst_Az_PG01 = []
for i in range(0,94):
    lst_Az_PG01.append((float(lst_Vz_PG01[i+1])-float(lst_Vz_PG01[i]))/(15*60))
#print(lst_Az_PG01)

##PG02
lst_Vx_PG02 = []
for i in range(0,24*4-1):
    lst_Vx_PG02.append((float(lst_x[3*i+3+1])-float(lst_x[3*i+1]))/(15*60))
#print(lst_Vx_PG02)
lst_Vy_PG02 = []
for i in range(0,24*4-1):
    lst_Vy_PG02.append((float(lst_y[3*i+3+1])-float(lst_y[3*i+1]))/(15*60))
#print(lst_Vy_PG02)
lst_Vz_PG02 = []
for i in range(0,24*4-1):
    lst_Vz_PG02.append((float(lst_z[3*i+3+1])-float(lst_z[3*i+1]))/(15*60))
#print(lst_Vz_PG02)
lst_Ax_PG02 = []
for i in range(0,94):
    lst_Ax_PG02.append((float(lst_Vx_PG02[i+1])-float(lst_Vx_PG02[i]))/(15*60))
#print(lst_Ax_PG02)
lst_Ay_PG02 = []
for i in range(0,94):
    lst_Ay_PG02.append((float(lst_Vy_PG02[i+1])-float(lst_Vy_PG02[i]))/(15*60))
#print(lst_Ay_PG02)
lst_Az_PG02 = []
for i in range(0,94):
    lst_Az_PG02.append((float(lst_Vz_PG02[i+1])-float(lst_Vz_PG02[i]))/(15*60))
#print(lst_Az_PG02)

##PG03
lst_Vx_PG03 = []
for i in range(0,24*4-1):
    lst_Vx_PG03.append((float(lst_x[3*i+3+2])-float(lst_x[3*i+2]))/(15*60))
#print(lst_Vx_PG03)
lst_Vy_PG03 = []
for i in range(0,24*4-1):
    lst_Vy_PG03.append((float(lst_y[3*i+3+2])-float(lst_y[3*i+2]))/(15*60))
#print(lst_Vy_PG03)
lst_Vz_PG03 = []
for i in range(0,24*4-1):
    lst_Vz_PG03.append((float(lst_z[3*i+3+2])-float(lst_z[3*i+2]))/(15*60))
#print(lst_Vz_PG03)
lst_Ax_PG03 = []
for i in range(0,94):
    lst_Ax_PG03.append((float(lst_Vx_PG03[i+1])-float(lst_Vx_PG03[i]))/(15*60))
#print(lst_Ax_PG03)
lst_Ay_PG03 = []
for i in range(0,94):
    lst_Ay_PG03.append((float(lst_Vy_PG03[i+1])-float(lst_Vy_PG03[i]))/(15*60))
#print(lst_Ay_PG03)
lst_Az_PG03 = []
for i in range(0,94):
    lst_Az_PG03.append((float(lst_Vz_PG03[i+1])-float(lst_Vz_PG03[i]))/(15*60))
#print(lst_Az_PG03)


###額外輸出速度/加速度的CSV檔

##轉回dataframe，插入時間列
data_PG01_Vx = {"Vx_PG01":lst_Vx_PG01}
df_PG01_Vx = pd.DataFrame(data_PG01_Vx, index= [t for t in range(0,86400-900,900)])
data_V= {"Vx_PG01":lst_Vx_PG01,"Vx_PG02":lst_Vx_PG02,"Vx_PG03":lst_Vx_PG03,"Vy_PG01":lst_Vy_PG01,"Vy_PG02":lst_Vy_PG02,"Vy_PG03":lst_Vy_PG03,"Vz_PG01":lst_Vz_PG01,"Vz_PG02":lst_Vz_PG02,"Vz_PG03":lst_Vz_PG03}
df_V = pd.DataFrame(data_V,index = [t for t in range(0,86400-900,900)])
df_V.to_csv("21956_v.csv", index=False)
data_A = {"Ax_PG01":lst_Ax_PG01,"Ax_PG02":lst_Ax_PG02,"Ax_PG03":lst_Ax_PG03,"Ay_PG01":lst_Ay_PG01,"Ay_PG02":lst_Ay_PG02,"Ay_PG03":lst_Ay_PG03,"Az_PG01":lst_Ax_PG01,"Az_PG02":lst_Ax_PG02,"Az_PG03":lst_Ax_PG03}
df_A = pd.DataFrame(data_A,index = [t for t in range(0,86400-1800,900)])
df_A.to_csv("21956_a.csv", index=False)


###畫圖!!!
import matplotlib.pyplot as plt

##更改存圖路徑
if not os.path.exists('v-t'):
    os.mkdir('v-t')
path_vt = os.path.join(os.getcwd(), 'v-t')
os.chdir(path_vt)

##PG01:Vx-t圖
time = [time for time in range (0,86400-900,900)]
plt.figure(figsize=(10,6))
plt.plot(time, lst_Vx_PG01)
plt.title('PG01:Vx-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
plt.savefig("PG01_Vx-t.png")
#plt.show()
##PG01:Vy-t圖
time = [time for time in range (0,86400-900,900)]
plt.figure(figsize=(10,6))
plt.plot(time, lst_Vy_PG01)
plt.title('PG01:Vy-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
plt.savefig("PG01_Vy-t.png")
#plt.show()
##PG01:Vz-t圖
time = [time for time in range (0,86400-900,900)]
plt.figure(figsize=(10,6))
plt.plot(time, lst_Vz_PG01)
plt.title('PG01:Vz-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
plt.savefig("PG01_Vz-t.png")

#plt.show()
##PG02:Vx-t圖
time = [time for time in range (0,86400-900,900)]
plt.plot(time, lst_Vx_PG02)
plt.title('PG02:Vx-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG02:Vy-t圖
time = [time for time in range (0,86400-900,900)]
plt.plot(time, lst_Vy_PG02)
plt.title('PG02:Vy-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG02:Vz-t圖
time = [time for time in range (0,86400-900,900)]
plt.plot(time, lst_Vz_PG02)
plt.title('PG02:Vz-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG03:Vx-t圖
time = [time for time in range (0,86400-900,900)]
plt.plot(time, lst_Vx_PG03)
plt.title('PG03:Vx-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG03:Vy-t圖
time = [time for time in range (0,86400-900,900)]
plt.plot(time, lst_Vy_PG03)
plt.title('PG03:Vy-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG03:Vz-t圖
time = [time for time in range (0,86400-900,900)]
plt.plot(time, lst_Vz_PG03)
plt.title('PG03:Vz-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()

##更改存圖路徑
FileDirectory = os.getcwd()
ParentDirectory = os.path.dirname(FileDirectory)
os.chdir(ParentDirectory)
if not os.path.exists('a-t'): 
    os.mkdir('a-t')
path_at = os.path.join(ParentDirectory, 'a-t')
os.chdir(path_at)

##PG01:Ax-t圖
time = [time for time in range (0,86400-1800,900)]
plt.figure(figsize=(10,6))
plt.plot(time, lst_Ax_PG01)
plt.title('PG01:Ax-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
plt.savefig("PG01_Ax-t.png")
#plt.show()
##PG01:Ay-t圖
time = [time for time in range (0,86400-1800,900)]
plt.plot(time, lst_Ay_PG01)
plt.title('PG01:Ay-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG01:Az-t圖
time = [time for time in range (0,86400-1800,900)]
plt.plot(time, lst_Az_PG01)
plt.title('PG01:Az-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG02:Ax-t圖
time = [time for time in range (0,86400-1800,900)]
plt.plot(time, lst_Ax_PG02)
plt.title('PG02:Ax-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG02:Ay-t圖
time = [time for time in range (0,86400-1800,900)]
plt.plot(time, lst_Ay_PG02)
plt.title('PG02:Ay-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG02:Az-t圖
time = [time for time in range (0,86400-1800,900)]
plt.plot(time, lst_Az_PG02)
plt.title('PG02:Az-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG03:Ax-t圖
time = [time for time in range (0,86400-1800,900)]
plt.plot(time, lst_Ax_PG03)
plt.title('PG03:Ax-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG03:Ay-t圖
time = [time for time in range (0,86400-1800,900)]
plt.plot(time, lst_Ay_PG03)
plt.title('PG03:Ay-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
##PG03:Az-t圖
time = [time for time in range (0,86400-1800,900)]
plt.plot(time, lst_Az_PG03)
plt.title('PG03:Az-t')
plt.xlabel('time(sec)')
plt.ylabel('speed(km/s)')
#plt.show()
