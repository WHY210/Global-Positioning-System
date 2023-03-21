####全球定位系統概論HW2第4.5題
####by:WHY/2022.4.3

### 圖形化介面
##import Tkinter
try:
    import Tkinter as tkinter
except ImportError:
    import tkinter as tkinter
##建立主視窗 
win = tkinter.Tk()
win.minsize(width=600, height=60)



##定義按鍵函式
def btnPressed():
    ###輸入參數
    Time = str(entry1.get())
    weekday = int(entry2.get())
    path = str(entry3.get())
    IGS = str(entry4.get())

    ###從CDDIS下載廣播星曆壓縮檔並處理
    import requests
    def time(Time):
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
    path = path.replace("\\","\\\\")
    os.chdir(path)
    ##檔名
    file = "brdc" + time(Time) + "0.%sn.gz" %(Time[2:4])


    ##解壓縮gz檔
    #import gzip
    #def un_gz(file_name):
    #    f_name = file_name.replace("gz", "")
    #    g_file = gzip.GzipFile(file_name)
    #    open(f_name, "wb+").write(g_file.read())
    #    g_file.close()
    #un_gz(path + "/" + file)

    ##生成CSV檔
    file = file[0:-3]
    if not os.path.exists(file + ".csv"): 
        os.rename(file, file + ".csv")

    ##讀取CSV檔
    import pandas as pd
    file = "brdc" + time(Time) + "0.%sn.csv" %(Time[2:4])
    df = pd.read_csv(file, delimiter="\t")

    ##整理資料
    df = df.loc[7:12]
    df.columns = ["prn1"]
    df.index = [i for i in range(0,6)]
    dl = df["prn1"].tolist()
    for i in range(len(dl)):
        dl[i] = dl[i][3:]
        dl[i] = str(dl[i]).replace("D", "E")
 
    ##資料對應參數
    r=0
    #DateTime =       str(dl[0][19*0:19*1])
    #a0 =             float(dl[r][19*1:19*2])
    #a1 =             float(dl[r][19*2:19*3])
    #a2 =             float(dl[r][19*3:19*4])
    r=1
    #AgeOfEphemeris = float(dl[r][19*0:19*1])
    #Crs =            float(dl[r][19*1:19*2])
    delta_n =        float(dl[r][19*2:19*3])
    M0 =             float(dl[r][19*3:19*4])
    r=2
    Cuc =            float(dl[r][19*0:19*1])
    e =              float(dl[r][19*1:19*2])
    Cus =            float(dl[r][19*2:19*3])
    sqrt_a =         float(dl[r][19*3:19*4])
    r=3
    toe =            float(dl[r][19*0:19*1])
    Cic =            float(dl[r][19*1:19*2])
    BigOmega0 =      float(dl[r][19*2:19*3])
    Cis =            float(dl[r][19*3:19*4])
    r=4
    i0 =             float(dl[r][19*0:19*1])
    Crc =            float(dl[r][19*1:19*2])
    omega =          float(dl[r][19*2:19*3])
    BigOmega1 =      float(dl[r][19*3:19*4])
    r=5
    i1 =             float(dl[r][19*0:19*1])


    ### Step1：已知WGS84之橢球參數
    ##地球引力常數（m^3/sec^2）
    μ = float(398600800000000)
    ##地球自轉速率（rad/sec）
    omegae = float(0.00007292115147)

    ### Step2：計算平運動量
    ##軌道長半徑
    a = (sqrt_a)**2
    ##平運動量
    n0 = float((μ/(a**3))**(0.5))

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
   
    ###Step7：計算緯度變角uk、軌道半徑rk、軌道傾角ik
    uk = omega + fk + Cus*(math.sin(2*(omega+fk)))+ Cuc*(math.cos(2*(omega+fk)))
    rk = a*(1-e*math.cos(E)) + Crc*math.sin(2*(omega+fk)) +Crc*math.cos(2*(omega+fk))
    ik = i0 + i1*tk + Cis*math.sin(2*(omega+fk)) +Cic*math.cos(2*(omega+fk))

    ###Step8：計算lk
    lk = BigOmega0 + (BigOmega1-omegae)*tk-omegae*toe

    ### Step9：計算軌道平面上之衛星坐標
    x = rk*math.cos(uk)
    y = rk*math.sin(uk)

    ### Step 10：計算WGS84坐標系之衛星坐標(X, Y, Z)
    X = (x*math.cos(lk)-y*math.cos(ik)*math.sin(lk)) / 1000
    Y = (x*math.sin(lk)+y*math.cos(ik)*math.cos(lk)) / 1000
    Z = (y*math.sin(ik)) / 1000

    ###誤差（第五題）
    ##精密星曆的資料
    IGS = IGS.split(",")
    X_IGS = float(IGS[0] )
    Y_IGS = float(IGS[1] )
    Z_IGS = float(IGS[2] )
    

    ##公里誤差
    error_X = X-X_IGS
    error_Y = Y-Y_IGS
    error_Z = Z-Z_IGS
    ##百分誤差
    P_error_X = error_X / X_IGS *100
    P_error_Y = error_Y / Y_IGS *100
    P_error_Z = error_Z / Z_IGS *100

    ##結果輸出
    path = './output.txt'
    f = open(path, 'w')
    f.write("廣播星曆之衛星編號1號於20%s年%s月%s日%s時%s分%s秒轉換為地球地固坐標系 \n" %(Time[0], Time[1], Time[2], Time[3], Time[4], Time[5]))
    f.write("坐標為(%.6f km, %.6f km, %.6f km) \n" %(X, Y, Z))
    f.write("與精密星曆之誤差為(%.6f km, %.6f km, %.6f km) \n" %(error_X, error_Y, error_Z))
    f.write("百分誤差為(%.6f %%, %.6f %%, %.6f %%)" %(P_error_X, P_error_Y, P_error_Z))
    f.close()

###輸入區
label0 = tkinter.Label(win, text="請先自行下載當天之廣播星曆檔，將其移至你欲存放的資料夾位置，但不須解壓縮")
label0.place(x=20, y=20)
label1 = tkinter.Label(win, text="請輸入要求的時刻，以空格隔開，例如作業為2022 2 5 0 15 0.0 : ")
label1.place(x=20, y=40)
entry1 = tkinter.Entry(win)
entry1.place(x=375, y=40)
label2 = tkinter.Label(win, text="請輸入星期幾，例如作業為星期六則輸入6 : ")
label2.place(x=20, y=60)
entry2 = tkinter.Entry(win)
entry2.place(x=265, y=60)
label3 = tkinter.Label(win, text="欲存放的資料夾位置 : ")
label3.place(x=20, y=80)
entry3 = tkinter.Entry(win)
entry3.place(x=145, y=80)
label4 = tkinter.Label(win, text="請對照當天此時刻之精密星曆輸入X Y Z 坐標,以逗號「,」間隔 : ")
label4.place(x=20, y=100)
label5 =tkinter.Label(win, text="例如作業則為輸入 14581.408067,-1494.739422,21889.107258")
label5. place(x=20, y=120)
entry4 = tkinter.Entry(win)
entry4.place(x=375, y = 120)

###按鍵
btn1 = tkinter.Button(win, text="確認", command=btnPressed)
btn1.place(x = 500, y=160)

win.mainloop()


