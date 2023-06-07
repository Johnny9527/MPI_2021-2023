# -*- coding: utf-8 -*-
"""
@author: chris.paterson & johnny.lee
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import csv
import re
import requests
import numpy as np
import json

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(event.event_type, event.src_path)

    def on_created(self, event):
        print("on_created", event.src_path)

    def on_deleted(self, event):
        print("on_deleted", event.src_path)

    def on_modified(self, event):
        print("on_modified", event.src_path)
        runimportoffline = ImportOffline()  # If on_modified is triggered, run class ImportOffline

    def on_moved(self, event):
        print("on_moved", event.src_path)

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path="O:\\OESAnalysis", recursive=False)
# observer.schedule(event_handler, path="C:\\Johnny\TestingArea", recursive=False)
observer.start()

class ImportOffline():
    # Code from ImportOffline and ReadFile
    def __init__(self):

        print("Read new Analysis")
        with open("O:\\OESAnalysis\ANALYSEN.DAT", "r") as file:
        # with open("C:\\Johnny\TestingArea\ANALYSEN_6488.DAT", "r") as file:
            first_line = file.readline()
            for last_line in file:
                pass
        file.close()

        temp = last_line.split("  ")
        temp1 = temp[0].split()
        temp[0] = temp1[0]
        temp[1] = temp1[1]
        EMPTYfilter = filter(lambda x: x != "", temp)
        temp2 = list(EMPTYfilter)
        l2 = len(temp2)
        for i in range(l2):
            temp2[i] = temp2[i].strip()

        Header_Start = ['ID Number', 'Year', 'Standard', 'Description']
        Data_Start = [temp2[0], temp2[1], temp2[2], temp[3]]

        l3 = l2 - 4
        temp3 = [None] * (l3)
        tempH = [None] * (l3)
        tempD = [None] * (l3)
        tempHD = list()  # create an empty new list

        temp3 = temp2[4:l2]
        for i in range(l3):
            tempH[i] = re.findall('[A-Za-z]+', temp3[i])
            tempD[i] = re.findall('\d+\.\d+', temp3[i])
            if i >= 1:
                tempHD.append(tempH[i - 1] + tempD[i])  # store both header_main and data_main
            else:
                pass

        lm = l3 - 1
        Data_Main = [None] * (lm)
        Header_Main = [None] * (lm)
        Header_Data_Main = [None] * (lm)  # combination list
        Data_Main = tempD[1:l3]
        Header_Main = tempH[0:lm]
        Header_Data_Main = tempHD[0:l3]  # combination list

        Header = Header_Start + Header_Main
        Data = Data_Start + Data_Main
        HDRow = Data_Start + Header_Data_Main  # create a new row

        output_file = open("C:\\Johnny\OES_Output.csv", "w")
        writer = csv.writer(output_file)
        writer.writerow(Header)
        writer.writerow(Data)
        writer.writerow(HDRow)  # write the new row into file
        output_file.close()

        # ReadFile code
        path = "C:\\Johnny\OES_Output.csv"
        with open(path, newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            data = np.array(list(rows))
            row_2 = data[4]  # last-row data of the file (change according to file needs)
            lr2 = len(row_2)

            #  set all corresponding string to zero at first
            temp_C = "0"
            temp_Si = "0"
            temp_Mn = "0"
            temp_P = "0"
            temp_S = "0"
            temp_Cr = "0"
            temp_Ni = "0"
            temp_Mo = "0"
            temp_Al = "0"
            temp_Cu = "0"
            temp_Co = "0"
            temp_Ti = "0"
            temp_Nb = "0"
            temp_V = "0"
            temp_W = "0"
            temp_Pb = "0"
            temp_Mg = "0"
            temp_B = "0"
            temp_Sb = "0"
            temp_Sn = "0"
            temp_Zn = "0"
            temp_As = "0"
            temp_Bi = "0"
            temp_Ta = "0"
            temp_Ca = "0"
            temp_Ce = "0"
            temp_Zr = "0"
            temp_La = "0"
            temp_Se = "0"
            temp_N = "0"
            temp_Fe = "0"

            for j in range(4, lr2):
                temp_s1 = row_2[j].split('[')[1].split(',')[0]  # fetch the element symbol
                if temp_s1 == "'C'":
                    temp_C = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_C = temp_C.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Si'":
                    temp_Si = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Si = temp_Si.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Mn'":
                    temp_Mn = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Mn = temp_Mn.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'P'":
                    temp_P = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_P = temp_P.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'S'":
                    temp_S = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_S = temp_S.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Cr'":
                    temp_Cr = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Cr = temp_Cr.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Ni'":
                    temp_Ni = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Ni = temp_Ni.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Mo'":
                    temp_Mo = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Mo = temp_Mo.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Al'":
                    temp_Al = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Al = temp_Al.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Cu'":
                    temp_Cu = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Cu = temp_Cu.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Co'":
                    temp_Co = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Co = temp_Co.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Ti'":
                    temp_Ti = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Ti = temp_Ti.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Nb'":
                    temp_Nb = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Nb = temp_Nb.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'V'":
                    temp_V = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_V = temp_V.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'W'":
                    temp_W = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_W = temp_W.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Pb'":
                    temp_Pb = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Pb = temp_Pb.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Mg'":
                    temp_Mg = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Mg = temp_Mg.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'B'":
                    temp_B = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_B = temp_B.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Sb'":
                    temp_Sb = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Sb = temp_Sb.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Sn'":
                    temp_Sn = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Sn = temp_Sn.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Zn'":
                    temp_Zn = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Zn = temp_Zn.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'As'":
                    temp_As = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_As = temp_As.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Bi'":
                    temp_Bi = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Bi = temp_Bi.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Ta'":
                    temp_Ta = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Ta = temp_Ta.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Ca'":
                    temp_Ca = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Ca = temp_Ca.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Ce'":
                    temp_Ce = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Ce = temp_Ce.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Zr'":
                    temp_Zr = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Zr = temp_Zr.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'La'":
                    temp_La = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_La = temp_La.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Se'":
                    temp_Se = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Se = temp_Se.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'N'":
                    temp_N = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_N = temp_N.split("'")[1].split("'")[0]  # clear unnecessary symbols
                if temp_s1 == "'Fe'":
                    temp_Fe = row_2[j].split(',')[1].split(']')[0]  # split data from specific string
                    temp_Fe = temp_Fe.split("'")[1].split("'")[0]  # clear unnecessary symbols

            # parse analysis time
            temp_time = row_2[0].split("0702")[1].split("1NJL")[0]  # clear unnecessary symbols
            temp_time = "20" + temp_time[4] + temp_time[5] + "-" + temp_time[2] + temp_time[3] + "-" + \
                        temp_time[0] + temp_time[1] + "T" + temp_time[6] + temp_time[7] + ":" + \
                        temp_time[8] + temp_time[9] + ":" + temp_time[10] + temp_time[11]  # reformat time

        csvfile.close()

        # url = "https://mpiuktw01.mpiuk.com:8443/Thingworx"
        # url = "https://83.143.243.83:8443/Thingworx"  # for internal connection only
        # url = "https://10.27.99.90:8443/Thingworx"  # 07/09/2022 update: after Aspire change the domain.
        url = "https://10.72.55.30:8443/Thingworx"  # 12/09/2022 update: after Aspire change the domain.

        header = {'Content-Type': 'application/json', 'appKey': 'f680a2c3-6cef-43d2-96ef-2a9294603f0e'}

        # use main as a Python dictionary to create a JSON package
        main = {'ID_Number': row_2[0], 'Year': row_2[1], 'Standard': row_2[2], 'Description': row_2[3],
                'C': temp_C, 'Si': temp_Si, 'Mn': temp_Mn, 'P': temp_P, 'S': temp_S, 'Cr': temp_Cr,
                'Ni': temp_Ni, 'Mo': temp_Mo, 'Al': temp_Al, 'Cu': temp_Cu, 'Co': temp_Co, 'Ti': temp_Ti,
                'Nb': temp_Nb, 'V': temp_V, 'W': temp_W, 'Pb': temp_Pb, 'Mg': temp_Mg, 'B': temp_B, 'Sb': temp_Sb,
                'Sn': temp_Sn, 'Zn': temp_Zn, 'As': temp_As, 'Bi': temp_Bi, 'Ta': temp_Ta, 'Ca': temp_Ca,
                'Ce': temp_Ce, 'Zr': temp_Zr, 'La': temp_La, 'Se': temp_Se, 'N': temp_N, 'Fe': temp_Fe,
                'MachineType': 'SPECTROLAB (old)', 'AnalysisTime': temp_time}

        # serializing JSON from main
        json_output = json.dumps(main, indent=4)

        # write data into OldOES.json to check
        with open("C:\\Johnny\OldOES.json", "w") as jsonfile:
            jsonfile.write(json_output)

        # create main_1 to store Old OES data and JSON package for OESThing (Old OES)
        main_1 = {'ID_Number': row_2[0], 'Year': row_2[1], 'Standard': row_2[2], 'Description': row_2[3],
                  'C': temp_C, 'Si': temp_Si, 'Mn': temp_Mn, 'P': temp_P, 'S': temp_S, 'Cr': temp_Cr,
                  'Ni': temp_Ni, 'Mo': temp_Mo, 'Al': temp_Al, 'Cu': temp_Cu, 'Co': temp_Co, 'Ti': temp_Ti,
                  'Nb': temp_Nb, 'V': temp_V, 'W': temp_W, 'Pb': temp_Pb, 'Mg': temp_Mg, 'B': temp_B, 'Sb': temp_Sb,
                  'Sn': temp_Sn, 'Zn': temp_Zn, 'As': temp_As, 'Bi': temp_Bi, 'Ta': temp_Ta, 'Ca': temp_Ca,
                  'Ce': temp_Ce, 'Zr': temp_Zr, 'La': temp_La, 'Se': temp_Se, 'N': temp_N, 'Fe': temp_Fe,
                  'MachineType': 'SPECTROLAB (old)', 'AnalysisTime': temp_time, 'OldOES-JSON': json_output}

        # send main_1 to OESThing (Old OES) properties
        response_1 = requests.put(url + '/Things/OESThing/Properties/*', headers=header, json=main_1,
                                verify=False)
        print(response_1.status_code)
        print(response_1.text)

        # create main_2 to store Old OES data and JSON package for mqttTest1 (New OES)
        # main_2 = {'HeatNumber': '0', 'ProjectNumber': '0', 'SampleName': row_2[3], 'C': temp_C, 'Si': temp_Si,
        #           'Mn': temp_Mn, 'P': temp_P, 'S': temp_S, 'Cr': temp_Cr, 'Ni': temp_Ni, 'Mo': temp_Mo,
        #           'Al': temp_Al, 'Cu': temp_Cu, 'Co': temp_Co, 'Ti': temp_Ti, 'Nb': temp_Nb, 'V': temp_V,
        #           'W': temp_W, 'Pb': temp_Pb, 'Mg': temp_Mg, 'B': temp_B, 'Sb': temp_Sb, 'Sn': temp_Sn, 'Zn': temp_Zn,
        #           'As': temp_As, 'Bi': temp_Bi, 'Ta': temp_Ta, 'Ca': temp_Ca, 'Ce': temp_Ce, 'Zr': temp_Zr,
        #           'La': temp_La, 'Se': temp_Se, 'N': temp_N, 'Fe': temp_Fe, 'MachineType': 'SPECTROLAB (old)',
        #           'UTC_timestamp': temp_time, 'OldOES-JSON': json_output, 'Li': '0', 'Be': '0', 'Na': '0', 'Sc': '0',
        #           'Ga': '0', 'Sr': '0', 'Ag': '0', 'Cd': '0', 'In': '0', 'Ba': '0', 'Hg': '0', 'Hf': '0', 'O': '0',
        #           'Re': '0', 'Te': '0'}

        # send main_2 to mqttTest1 (New OES) properties
        # 07/09/2022 update: Not sending Old OES data and JSON file to mqttTest1 anymore.

        # response_2 = requests.put(url + '/Things/mqttTest1/Properties/*', headers=header, json=main_2,
        #                         verify=False)
        # print(response_2.status_code)
        # print(response_2.text)

while True:
    try:
        pass
    except KeyboardInterrupt:
        observer.stop()
