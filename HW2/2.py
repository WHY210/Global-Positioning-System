####全球定位系統概論HW2第4.5題
####by:WHY/2022.4.3

### Step1：已知WGS84之橢球參數
#地球引力常數（m^3/sec^2）
μ = float(398600800000000)
#地球自轉速率（rad/sec）
e = float(0.00007292115147)

### Step2：計算平運動量
##軌道長半徑
a = float(input("軌道長半徑："))
##平運動量
n = (μ/(a**3))**(-0.5)

### Step3：計算觀測時刻與參考時刻之時間差tk
##參考時刻
date = str(input("參考時刻，以「.」分隔："))
date_lst = date.split(".")
map_date_lst = map(int, date_lst)
date_lst = list(map_date_lst)
#[year, month, day, hour, minute, second]
##判斷閏年(1:閏年)
if date_lst[0] % 4 == 0:
    leap = 1
    if date_lst[0] % 100 == 0:
        if date_lst[0] % 400 == 0:
            leap = 1
        else:
            leap = 0

leap4   = date_lst[0] / 4
leap100 = date_lst[0] / 100
leap400 = date_lst[0] / 400
month      = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
month_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

##非閏年
days = 0
MonthDays = 0
i = 0
while leap == 0:
    for i in range(date_lst[1]-1):
        MonthDays += month[i] 
        MonthDays += date_lst[2]
    days = 365 * (date_lst[0] -1 - leap4 + leap100 -leap400) 
         + 366 *(leap4 - leap100 +leap400)
         + MonthDays

else:
    for i in range(date_lst[1]-1):
        MonthDays += month_leap[i] 
        MonthDays += date_lst[2]

#if (date_lst[0] % 4 == 0 & date_lst[0] % 100 == 0 & date_lst[0] == 400) == False:
    #

#t = 86400 * {* date_lst[0] + * date_lst[1] * date_lst[2]
