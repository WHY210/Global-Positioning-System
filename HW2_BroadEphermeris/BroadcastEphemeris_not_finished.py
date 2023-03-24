####全球定位系統概論HW2第4.5題
####by:WHY/2022.4.3

##從CDDIS下載廣播星曆壓縮檔
import requests
from bs4 import BeautifulSoup

Time = str(input("請輸入要求的時刻(以空格隔開，例如作業為2022 2 5 0 15 0.0) : "))
weekday = int(input("請輸入星期幾，例如星期六則輸入6 : "))
def time(time):
    date = Time.split(" ")
    ##判斷閏年(1:閏年)
    if int(date[0]) % 4 == 0: 
        leap = 1
        if int(date[0]) % 100 == 0:
            if int(date[0]) % 400 == 0: leap = 1
            else: leap = 0
    else: leap = 0
    ##計算GPSday
    month      = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    GPSday = 0
    ##平年
    if leap == 0:
        for i in range(int(date[1])-1):
            GPSday += month[i] 
        GPSday += int(date[2])
    ##閏年
    if leap == 1:
        for i in range(int(date[1])-1):
            GPSday += month_leap[i] 
        GPSday += date[2]
    GPSday = str("0" + str(GPSday))
    return GPSday
    

##更改檔案絕對路徑
import os
path = str(input("欲存放的資料夾位置 : "))
path = path.replace("\\","/")
os.chdir(path)


"""
url = "https://cddis.nasa.gov/archive/gnss/data/daily/" + Time[0:4] + "/" + time(Time) + "/22n/"
headers = {'content-type': 'text/html; charset=UTF-8',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
html = requests.get(url=url,headers=headers,timeout=30)
soup = BeautifulSoup(html.content,'html.parser')
"""
file = "brdc" + time(Time) + "0.22n.gz"
"""
r = requests.get(soup[file], headers=headers, stream=True, verify=False, auth=('why24', 'tatsumi24'))
with open("./"+file, "wb") as brdc:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            brdc.write(chunk)
            brdc.close()
"""




##解壓縮gz檔
import gzip
def un_gz(file_name):
    f_name = file_name.replace("gz", "")
    g_file = gzip.GzipFile(file_name)
    open(f_name, "wb+").write(g_file.read())
    g_file.close()
un_gz(path + "/" + file)

##生成CSV檔
file = file[0:-3]
if not os.path.exists(file + ".csv"): 
    os.rename(file, file + ".csv")

##讀取CSV檔
import pandas as pd
file = "brdc" + time(Time) + "0.22n.csv"
df = pd.read_csv(file, delimiter="\t")

##整理資料
df = df.loc[7:12]
df.columns = ["prn1"]
df.index = [i for i in range(0,6)]
a = df["prn1"].tolist()
for i in range(len(a)):
    a[i] = a[i][3:]
    a[i] = str(a[i]).replace("D", "E")
 
##資料對應參數
"""
VariableList = dict.fromkeys(["DateTime"], str(a[0][19*0:19*1]))
VariableList.update(dict.fromkeys(["a0", "a1", "a2"], (float(a[0][19*c:19*c]) for c in range(1,4))))
VariableList.update(dict.fromkeys(["AgeOfEphemeris", "Crs", "delta_n", "M0"], (float(a[1][19*c:19*c]) for c in range(4))))
VariableList.update(dict.fromkeys(["toe", "Cic", "BigOmega0", "Cis"], (float(a[3][19*c:19*c]) for c in range(4))))
VariableList.update(dict.fromkeys(["i0", "Crc", "omega", "BigOmega1"], (float(a[4][19*c:19*c]) for c in range(4))))
VariableList.update(dict.fromkeys(["i1", None, None, None], (float(a[5][19*c:19*c]) for c in range(4))))
"""
r=0
DateTime =       str(a[0][19*0:19*1])
a0 =             float(a[r][19*1:19*2])
a1 =             float(a[r][19*2:19*3])
a2 =             float(a[r][19*3:19*4])
r=1
AgeOfEphemeris = float(a[r][19*0:19*1])
Crs =            float(a[r][19*1:19*2])
delta_n =        float(a[r][19*2:19*3])
M0 =             float(a[r][19*3:19*4])
r=2
Cuc =            float(a[r][19*0:19*1])
e =              float(a[r][19*1:19*2])
Cus =            float(a[r][19*2:19*3])
sqrt_a =         float(a[r][19*3:19*4])
r=3
toe =            float(a[r][19*0:19*1])
Cic =            float(a[r][19*1:19*2])
BigOmega0 =      float(a[r][19*2:19*3])
Cis =            float(a[r][19*3:19*4])
r=4
i0 =             float(a[r][19*0:19*1])
Crc =            float(a[r][19*1:19*2])
omega =          float(a[r][19*2:19*3])
BigOmega1 =      float(a[r][19*3:19*4])
r=5
i1 =             float(a[r][19*0:19*1])



### Step1：已知WGS84之橢球參數
##地球引力常數（m^3/sec^2）
μ = float(398600800000000)
##地球自轉速率（rad/sec）
omegae = float(0.00007292115147)

### Step2：計算平運動量
##軌道長半徑
a_ = (sqrt_a)**2
##平運動量
n0 = float((μ/(a_**3))**(0.5))

### Step3：計算觀測時刻與參考時刻之時間差tk
Time = Time[2:]
Time = Time.split(" ")
t = (24*60*60)*weekday + (60*60)*float(Time[3]) + (60)*float(Time[4]) + float(Time[5])
tk = t - toe

### Step4：計算改正後之平運動量
n = n0 + delta_n

### Step5：利用克卜勒方程漸進解算偏心偏近點角E
from cmath import pi
import math
M = M0 + n * tk
##迭代解
E = M

for m in range(1000):
    E = E - ((E - e*(math.sin(E)) - M) / (1 - e*(math.cos(E))))
    

### Step6：計算真近點角fk
import numpy as np
cos_fk = (math.cos(E) - e)/(1 - e*math.cos(E))
sin_fk = (1 - e**2)**(0.5) * math.sin(E) / (1 - e * math.cos(E))
fk = math.atan((sin_fk/cos_fk)) #* (180 / np.pi)

"""
#     090
#   -+ | ++
#180---+---000
#   -- | +-
#     270
if cos_fk > 0:
    if sin_fk > 0: fk = fk
    else: fk = 360-fk
else:
    if sin_fk > 0: fk = 180-fk
    else: fk = 180+fk
"""
###Step7：計算緯度變角uk、軌道半徑rk、軌道傾角ik
uk = omega + fk + Cus*(math.sin(2*(omega+fk)))+ Cuc*(math.cos(2*(omega+fk)))
rk = a_*(1-e*math.cos(E)) + Crc*math.sin(2*(omega+fk)) +Crc*math.cos(2*(omega+fk))
ik = i0 + i1*tk + Cis*math.sin(2*(omega+fk)) +Cic*math.cos(2*(omega+fk))

###Step8：計算lk
lk = BigOmega0 + (BigOmega1-omegae)*tk-omegae*toe

### Step9：計算軌道平面上之衛星坐標
x = rk*math.cos(uk)
y = rk*math.sin(uk)

### Step 10：計算WGS84坐標系之衛星坐標(X, Y, Z)
X = x*math.cos(lk)-y*math.cos(ik)*math.sin(lk)
Y = x*math.sin(lk)+y*math.cos(ik)*math.cos(lk)
Z = y*math.sin(ik)

X = X / 1000
Y = Y / 1000
Z = Z / 1000

print("坐標為(", X, Y, Z, ")(km)")

###誤差
X_IGS = 14581.408067
Y_IGS = -1494.739422
Z_IGS = 21889.107258
error_X = X-X_IGS
error_Y = Y-Y_IGS
error_Z = Z-Z_IGS
P_error_X = error_X / X_IGS *100
P_error_Y = error_Y / Y_IGS *100
P_error_Z = error_Z / Z_IGS *100
print("誤差為(", error_X, error_Y, error_Z, ")(km)")
print("百分誤差為(", P_error_X, P_error_Y, P_error_Z, ")(%)")

"""
class BroadcastEphemeris:
    ### 建構式
    def __init__(self, CoordinateName):
        self.CoordinateName = CoordinateName ##坐標屬性
    ###方法
    def Error_brdc_igs(self, CoordinateName, coordinate_igs):
        Error= CoordinateName - coordinate_igs
        PercentError = (CoordinateName - coordinate_igs) / coordinate_igs * 100 
        print(f"{self.CoordinateName}坐標的誤差 = ", Error, "(m), 大約是", PercentError, "(%)") 

BroadcastEphemeris(X)
"""
