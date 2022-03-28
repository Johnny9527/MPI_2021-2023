import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_UP
import os
from datetime import datetime

# Passing the path of the xml document to enable the parsing process
tree = ET.parse('C:\\MyStuffs\Test\Results_20210311135707.xml')  # 20210311 FE01.xps
# tree = ET.parse('C:\\MyStuffs\Test\Results_20210311135929.xml')  # 20210311 FE10.xps
# tree = ET.parse('C:\\MyStuffs\Test\Results_20210312095743.xml')  # 20210312 Al-01.xps
# tree = ET.parse('C:\\MyStuffs\Test\Results_20210312100001.xml')  # 20210312 Al-30.xps
# tree = ET.parse('C:\\MyStuffs\Test\Results_20210312122437.xml')  # 20210312 NI-01.xps

# getting the parent tag of the xml document
root = tree.getroot()

# print out the root content, XMLVersion and XMLCreationDateTime
print(root.attrib)

print('**********************************')

# analysis count
count = 1

# get the last analysed element in the XML file
ReferenceLineName = root.find('.//MeasurementReplicate/Measurement/Lines/Line').attrib['ReferenceLineName']
print(ReferenceLineName)
lastElement = ReferenceLineName[0] + ReferenceLineName[1]
print('The last analysed element is ' + lastElement)

print('**********************************')

# write Python results line by line to 'outputResult.txt' after extracting data from the XML
# but need to open the file first, otherwise results will be overwritten in a loop
with open('C:\\MyStuffs\Test\outputResult.txt', 'w') as f:

    # find all three 'MeasurementReplicate' tags
    for findAllMeasurementReplicate in root.findall('.//MeasurementReplicates'):

        # print out the attribute of MeasurementReplicate
        print(findAllMeasurementReplicate.attrib)

        # find all 'Element' tags under 'MeasurementReplicate'
        for element in root.findall('.//MeasurementReplicate/Measurement/Elements/Element'):

            print(element.attrib)

            # print out the element name and its analysis number
            print(element.attrib['ElementName'] + '(' + str(count) + ')')

            # use tempElement to record each element name and write it into 'outputResult.txt'
            tempElement = element.attrib['ElementName'] + '_' + str(count)

            # combine strings and values into MQTT broker format
            f.write("cmd" + " /c " + '"' + "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t " + tempElement)
            f.write(" ")

            # get ElementResult tag in which StatType="Reported"
            for elementResult in element.iter('ElementResult'):

                # get StatType="Reported"
                if elementResult.attrib['StatType'] == 'Reported':

                    # get the first resultValue under 'ElementResult' when StatType="Reported" in text
                    for resultValue in elementResult.iter('ResultValue'):
                        print(resultValue.text)

                        # use tempResult to record each resultValue and write it into 'outputResult.txt'
                        tempResult = resultValue.text

                        # round up the analysis result value
                        round_Value = Decimal(tempResult).quantize(Decimal(".00000"), ROUND_HALF_UP)

                        # combine strings and values into MQTT broker format
                        # I purposely add an '@' here because I need to get rid of the '\n' in a later step
                        # otherwise an error will occur during the CMD process
                        f.write("-m " + str(round_Value) + " -u mqttuser2 -P Mqtt123456" + '"' + '@')
                        f.write('\n')

                        # after each round of analysis, count is incremented by one
                        if element.attrib['ElementName'] == lastElement:
                            count = count + 1
                            break
                        else:
                            break

                    print('#################################')

        print('//////////////////////////////////')

    # find all 'MeasurementStatistics' tags
    for findAllMeasurementStatistics in root.findall('.//MeasurementStatistics'):

        # find all 'Element' tags under 'MeasurementStatistics'
        for element in root.findall('.//MeasurementStatistics/Measurement/Elements/Element'):

            print(element.attrib)

            # print out the element name and its Rep
            print(element.attrib['ElementName'] + '(Rep)')

            # use tempElement to record each element name and write it into 'outputResult.txt'
            tempElement = element.attrib['ElementName'] + '_Rep'

            # combine strings and values into MQTT broker format
            f.write("cmd" + " /c " + '"' + "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t " + tempElement)
            f.write(" ")

            # get ElementResult tag in which StatType="Reported"
            for elementResult in element.iter('ElementResult'):

                # get StatType="Reported"
                if elementResult.attrib['StatType'] == 'Reported':

                    # get the first resultValue under 'ElementResult' when StatType="Reported" in text
                    for resultValue in elementResult.iter('ResultValue'):
                        print(resultValue.text)

                        # use tempResult to record each resultValue and write it into 'outputResult.txt'
                        tempResult = resultValue.text

                        # round up the analysis result value
                        round_Value = Decimal(tempResult).quantize(Decimal(".00000"), ROUND_HALF_UP)

                        # combine strings and values into MQTT broker format
                        f.write("-m " + str(round_Value) + " -u mqttuser2 -P Mqtt123456" + '"' + '@')
                        f.write('\n')

                        break

                    print('#################################')

        print('//////////////////////////////////')

    print('---read & write XML script end---')

f.close()

# set the default value of each element to zero
print('---start data cleaning, please wait---')

os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t UTC_timestamp -m NA -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t AnalysisFileName -m NA -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t C_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Si_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mn_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t P_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t S_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cr_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mo_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ni_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Al_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Co_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cu_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Nb_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ti_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t V_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t W_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Pb_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sn_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t As_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Zr_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Bi_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ca_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ce_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sb_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Se_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Te_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ta_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t B_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Zn_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t La_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ag_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t N_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t O_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Fe_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t C_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Si_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mn_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t P_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t S_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cr_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mo_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ni_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Al_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Co_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cu_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Nb_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ti_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t V_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t W_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Pb_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sn_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t As_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Zr_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Bi_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ca_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ce_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sb_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Se_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Te_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ta_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t B_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Zn_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t La_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ag_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t N_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t O_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Fe_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t C_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Si_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mn_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t P_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t S_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cr_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mo_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ni_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Al_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Co_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cu_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Nb_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ti_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t V_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t W_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Pb_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sn_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t As_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Zr_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Bi_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ca_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ce_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sb_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Se_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Te_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ta_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t B_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Zn_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t La_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ag_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t N_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t O_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Fe_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t C_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Si_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mn_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t P_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t S_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cr_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mo_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ni_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Al_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Co_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cu_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Nb_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ti_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t V_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t W_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Pb_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sn_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t As_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Zr_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Bi_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ca_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ce_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sb_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Se_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Te_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ta_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t B_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Zn_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t La_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ag_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t N_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t O_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Fe_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mg_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mg_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mg_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Mg_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ba_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ba_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ba_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ba_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Be_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Be_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Be_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Be_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cd_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cd_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cd_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Cd_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ga_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ga_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ga_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Ga_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Hg_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Hg_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Hg_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Hg_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t In_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t In_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t In_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t In_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Li_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Li_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Li_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Li_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Na_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Na_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Na_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Na_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sr_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sr_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sr_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sr_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sc_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sc_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sc_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Sc_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Hf_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Hf_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Hf_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Hf_Rep -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Re_1 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Re_2 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Re_3 -m 0 -u mqttuser2 -P Mqtt123456"')
os.system('cmd /c "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t Re_Rep -m 0 -u mqttuser2 -P Mqtt123456"')

print('---data cleaning end---')

# get the "XMLCreationDateTime", make it into a file name, and then upload to ThingWorx
XMLCreationDateTime = root.attrib['XMLCreationDateTime']
fileName = "Results_" + XMLCreationDateTime[0] + XMLCreationDateTime[1] + XMLCreationDateTime[2] + \
           XMLCreationDateTime[3] + XMLCreationDateTime[5] + XMLCreationDateTime[6] + XMLCreationDateTime[8] + \
           XMLCreationDateTime[9] + XMLCreationDateTime[11] + XMLCreationDateTime[12] + XMLCreationDateTime[14] + \
           XMLCreationDateTime[15] + XMLCreationDateTime[17] + XMLCreationDateTime[18]
print('The analysis file is ' + fileName + '.xml')

# constructing the MQTT command line
AnalysisFileName = "cmd" + " /c " + '"' + "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t AnalysisFileName" + \
                   " -m " + str(fileName) + " -u mqttuser2 -P Mqtt123456" + '"'

# upload "AnalysisFileName" to ThingWorx platform
os.system(AnalysisFileName)

# open and read the content of 'outputResult.txt'
with open('C:\\MyStuffs\Test\outputResult.txt', 'r') as f:

    # read all the lines of the file and return them as a list of strings
    contents = f.readlines()

    # lenth of the content list
    lenth = len(contents)

    # use a 'for loop' to go through the list content
    for i in range(0, lenth):

        # extract the chemical element
        temp_Ele = contents[i].split('-t ')[1].split(' -m')[0]

        # if the element is C_1 extract the MQTT command line from the content
        if temp_Ele == 'C_1':
            C_1 = contents[i].split('@')[0]
            print(C_1)
            os.system(C_1)  # execute MQTT command on CMD

        # if the element is Si_1 extract the MQTT command line from the content
        elif temp_Ele == 'Si_1':
            Si_1 = contents[i].split('@')[0]
            print(Si_1)
            os.system(Si_1)  # execute MQTT command on CMD

        # if the element is Mn_1 extract the MQTT command line from the content
        elif temp_Ele == 'Mn_1':
            Mn_1 = contents[i].split('@')[0]
            print(Mn_1)
            os.system(Mn_1)  # execute MQTT command on CMD

        # if the element is P_1 extract the MQTT command line from the content
        elif temp_Ele == 'P_1':
            P_1 = contents[i].split('@')[0]
            print(P_1)
            os.system(P_1)  # execute MQTT command on CMD

        # if the element is S_1 extract the MQTT command line from the content
        elif temp_Ele == 'S_1':
            S_1 = contents[i].split('@')[0]
            print(S_1)
            os.system(S_1)  # execute MQTT command on CMD

        # if the element is Cr_1 extract the MQTT command line from the content
        elif temp_Ele == 'Cr_1':
            Cr_1 = contents[i].split('@')[0]
            print(Cr_1)
            os.system(Cr_1)  # execute MQTT command on CMD

        # if the element is Mo_1 extract the MQTT command line from the content
        elif temp_Ele == 'Mo_1':
            Mo_1 = contents[i].split('@')[0]
            print(Mo_1)
            os.system(Mo_1)  # execute MQTT command on CMD

        # if the element is Ni_1 extract the MQTT command line from the content
        elif temp_Ele == 'Ni_1':
            Ni_1 = contents[i].split('@')[0]
            print(Ni_1)
            os.system(Ni_1)  # execute MQTT command on CMD

        # if the element is Al_1 extract the MQTT command line from the content
        elif temp_Ele == 'Al_1':
            Al_1 = contents[i].split('@')[0]
            print(Al_1)
            os.system(Al_1)  # execute MQTT command on CMD

        # if the element is Co_1 extract the MQTT command line from the content
        elif temp_Ele == 'Co_1':
            Co_1 = contents[i].split('@')[0]
            print(Co_1)
            os.system(Co_1)  # execute MQTT command on CMD

        # if the element is Cu_1 extract the MQTT command line from the content
        elif temp_Ele == 'Cu_1':
            Cu_1 = contents[i].split('@')[0]
            print(Cu_1)
            os.system(Cu_1)  # execute MQTT command on CMD

        # if the element is Nb_1 extract the MQTT command line from the content
        elif temp_Ele == 'Nb_1':
            Nb_1 = contents[i].split('@')[0]
            print(Nb_1)
            os.system(Nb_1)  # execute MQTT command on CMD

        # if the element is Ti_1 extract the MQTT command line from the content
        elif temp_Ele == 'Ti_1':
            Ti_1 = contents[i].split('@')[0]
            print(Ti_1)
            os.system(Ti_1)  # execute MQTT command on CMD

        # if the element is V_1 extract the MQTT command line from the content
        elif temp_Ele == 'V_1':
            V_1 = contents[i].split('@')[0]
            print(V_1)
            os.system(V_1)  # execute MQTT command on CMD

        # if the element is W_1 extract the MQTT command line from the content
        elif temp_Ele == 'W_1':
            W_1 = contents[i].split('@')[0]
            print(W_1)
            os.system(W_1)  # execute MQTT command on CMD

        # if the element is Pb_1 extract the MQTT command line from the content
        elif temp_Ele == 'Pb_1':
            Pb_1 = contents[i].split('@')[0]
            print(Pb_1)
            os.system(Pb_1)  # execute MQTT command on CMD

        # if the element is Sn_1 extract the MQTT command line from the content
        elif temp_Ele == 'Sn_1':
            Sn_1 = contents[i].split('@')[0]
            print(Sn_1)
            os.system(Sn_1)  # execute MQTT command on CMD

        # if the element is As_1 extract the MQTT command line from the content
        elif temp_Ele == 'As_1':
            As_1 = contents[i].split('@')[0]
            print(As_1)
            os.system(As_1)  # execute MQTT command on CMD

        # if the element is Zr_1 extract the MQTT command line from the content
        elif temp_Ele == 'Zr_1':
            Zr_1 = contents[i].split('@')[0]
            print(Zr_1)
            os.system(Zr_1)  # execute MQTT command on CMD

        # if the element is Bi_1 extract the MQTT command line from the content
        elif temp_Ele == 'Bi_1':
            Bi_1 = contents[i].split('@')[0]
            print(Bi_1)
            os.system(Bi_1)  # execute MQTT command on CMD

        # if the element is Ca_1 extract the MQTT command line from the content
        elif temp_Ele == 'Ca_1':
            Ca_1 = contents[i].split('@')[0]
            print(Ca_1)
            os.system(Ca_1)  # execute MQTT command on CMD

        # if the element is Ce_1 extract the MQTT command line from the content
        elif temp_Ele == 'Ce_1':
            Ce_1 = contents[i].split('@')[0]
            print(Ce_1)
            os.system(Ce_1)  # execute MQTT command on CMD

        # if the element is Sb_1 extract the MQTT command line from the content
        elif temp_Ele == 'Sb_1':
            Sb_1 = contents[i].split('@')[0]
            print(Sb_1)
            os.system(Sb_1)  # execute MQTT command on CMD

        # if the element is Se_1 extract the MQTT command line from the content
        elif temp_Ele == 'Se_1':
            Se_1 = contents[i].split('@')[0]
            print(Se_1)
            os.system(Se_1)  # execute MQTT command on CMD

        # if the element is Te_1 extract the MQTT command line from the content
        elif temp_Ele == 'Te_1':
            Te_1 = contents[i].split('@')[0]
            print(Te_1)
            os.system(Te_1)  # execute MQTT command on CMD

        # if the element is Ta_1 extract the MQTT command line from the content
        elif temp_Ele == 'Ta_1':
            Ta_1 = contents[i].split('@')[0]
            print(Ta_1)
            os.system(Ta_1)  # execute MQTT command on CMD

        # if the element is B_1 extract the MQTT command line from the content
        elif temp_Ele == 'B_1':
            B_1 = contents[i].split('@')[0]
            print(B_1)
            os.system(B_1)  # execute MQTT command on CMD

        # if the element is Zn_1 extract the MQTT command line from the content
        elif temp_Ele == 'Zn_1':
            Zn_1 = contents[i].split('@')[0]
            print(Zn_1)
            os.system(Zn_1)  # execute MQTT command on CMD

        # if the element is La_1 extract the MQTT command line from the content
        elif temp_Ele == 'La_1':
            La_1 = contents[i].split('@')[0]
            print(La_1)
            os.system(La_1)  # execute MQTT command on CMD

        # if the element is Ag_1 extract the MQTT command line from the content
        elif temp_Ele == 'Ag_1':
            Ag_1 = contents[i].split('@')[0]
            print(Ag_1)
            os.system(Ag_1)  # execute MQTT command on CMD

        # if the element is N_1 extract the MQTT command line from the content
        elif temp_Ele == 'N_1':
            N_1 = contents[i].split('@')[0]
            print(N_1)
            os.system(N_1)  # execute MQTT command on CMD

        # if the element is O_1 extract the MQTT command line from the content
        elif temp_Ele == 'O_1':
            O_1 = contents[i].split('@')[0]
            print(O_1)
            os.system(O_1)  # execute MQTT command on CMD

        # if the element is Fe_1 extract the MQTT command line from the content
        elif temp_Ele == 'Fe_1':
            Fe_1 = contents[i].split('@')[0]
            print(Fe_1)
            os.system(Fe_1)  # execute MQTT command on CMD

        # if the element is Mg_1 extract the MQTT command line from the content
        elif temp_Ele == 'Mg_1':
            Mg_1 = contents[i].split('@')[0]
            print(Mg_1)
            os.system(Mg_1)  # execute MQTT command on CMD

        # if the element is Ba_1 extract the MQTT command line from the content
        elif temp_Ele == 'Ba_1':
            Ba_1 = contents[i].split('@')[0]
            print(Ba_1)
            os.system(Ba_1)  # execute MQTT command on CMD

        # if the element is Be_1 extract the MQTT command line from the content
        elif temp_Ele == 'Be_1':
            Be_1 = contents[i].split('@')[0]
            print(Be_1)
            os.system(Be_1)  # execute MQTT command on CMD

        # if the element is Cd_1 extract the MQTT command line from the content
        elif temp_Ele == 'Cd_1':
            Cd_1 = contents[i].split('@')[0]
            print(Cd_1)
            os.system(Cd_1)  # execute MQTT command on CMD

        # if the element is Ga_1 extract the MQTT command line from the content
        elif temp_Ele == 'Ga_1':
            Ga_1 = contents[i].split('@')[0]
            print(Ga_1)
            os.system(Ga_1)  # execute MQTT command on CMD

        # if the element is Hg_1 extract the MQTT command line from the content
        elif temp_Ele == 'Hg_1':
            Hg_1 = contents[i].split('@')[0]
            print(Hg_1)
            os.system(Hg_1)  # execute MQTT command on CMD

        # if the element is In_1 extract the MQTT command line from the content
        elif temp_Ele == 'In_1':
            In_1 = contents[i].split('@')[0]
            print(In_1)
            os.system(In_1)  # execute MQTT command on CMD

        # if the element is Li_1 extract the MQTT command line from the content
        elif temp_Ele == 'Li_1':
            Li_1 = contents[i].split('@')[0]
            print(Li_1)
            os.system(Li_1)  # execute MQTT command on CMD

        # if the element is Na_1 extract the MQTT command line from the content
        elif temp_Ele == 'Na_1':
            Na_1 = contents[i].split('@')[0]
            print(Na_1)
            os.system(Na_1)  # execute MQTT command on CMD

        # if the element is Sr_1 extract the MQTT command line from the content
        elif temp_Ele == 'Sr_1':
            Sr_1 = contents[i].split('@')[0]
            print(Sr_1)
            os.system(Sr_1)  # execute MQTT command on CMD

        # if the element is Sc_1 extract the MQTT command line from the content
        elif temp_Ele == 'Sc_1':
            Sc_1 = contents[i].split('@')[0]
            print(Sc_1)
            os.system(Sc_1)  # execute MQTT command on CMD

        # if the element is Hf_1 extract the MQTT command line from the content
        elif temp_Ele == 'Hf_1':
            Hf_1 = contents[i].split('@')[0]
            print(Hf_1)
            os.system(Hf_1)  # execute MQTT command on CMD

        # if the element is Re_1 extract the MQTT command line from the content
        elif temp_Ele == 'Re_1':
            Re_1 = contents[i].split('@')[0]
            print(Re_1)
            os.system(Re_1)  # execute MQTT command on CMD

        # if the element is C_2 extract the MQTT command line from the content
        elif temp_Ele == 'C_2':
            C_2 = contents[i].split('@')[0]
            print(C_2)
            os.system(C_2)  # execute MQTT command on CMD

        # if the element is Si_2 extract the MQTT command line from the content
        elif temp_Ele == 'Si_2':
            Si_2 = contents[i].split('@')[0]
            print(Si_2)
            os.system(Si_2)  # execute MQTT command on CMD

        # if the element is Mn_2 extract the MQTT command line from the content
        elif temp_Ele == 'Mn_2':
            Mn_2 = contents[i].split('@')[0]
            print(Mn_2)
            os.system(Mn_2)  # execute MQTT command on CMD

        # if the element is P_2 extract the MQTT command line from the content
        elif temp_Ele == 'P_2':
            P_2 = contents[i].split('@')[0]
            print(P_2)
            os.system(P_2)  # execute MQTT command on CMD

        # if the element is S_2 extract the MQTT command line from the content
        elif temp_Ele == 'S_2':
            S_2 = contents[i].split('@')[0]
            print(S_2)
            os.system(S_2)  # execute MQTT command on CMD

        # if the element is Cr_2 extract the MQTT command line from the content
        elif temp_Ele == 'Cr_2':
            Cr_2 = contents[i].split('@')[0]
            print(Cr_2)
            os.system(Cr_2)  # execute MQTT command on CMD

        # if the element is Mo_2 extract the MQTT command line from the content
        elif temp_Ele == 'Mo_2':
            Mo_2 = contents[i].split('@')[0]
            print(Mo_2)
            os.system(Mo_2)  # execute MQTT command on CMD

        # if the element is Ni_2 extract the MQTT command line from the content
        elif temp_Ele == 'Ni_2':
            Ni_2 = contents[i].split('@')[0]
            print(Ni_2)
            os.system(Ni_2)  # execute MQTT command on CMD

        # if the element is Al_2 extract the MQTT command line from the content
        elif temp_Ele == 'Al_2':
            Al_2 = contents[i].split('@')[0]
            print(Al_2)
            os.system(Al_2)  # execute MQTT command on CMD

        # if the element is Co_2 extract the MQTT command line from the content
        elif temp_Ele == 'Co_2':
            Co_2 = contents[i].split('@')[0]
            print(Co_2)
            os.system(Co_2)  # execute MQTT command on CMD

        # if the element is Cu_2 extract the MQTT command line from the content
        elif temp_Ele == 'Cu_2':
            Cu_2 = contents[i].split('@')[0]
            print(Cu_2)
            os.system(Cu_2)  # execute MQTT command on CMD

        # if the element is Nb_2 extract the MQTT command line from the content
        elif temp_Ele == 'Nb_2':
            Nb_2 = contents[i].split('@')[0]
            print(Nb_2)
            os.system(Nb_2)  # execute MQTT command on CMD

        # if the element is Ti_2 extract the MQTT command line from the content
        elif temp_Ele == 'Ti_2':
            Ti_2 = contents[i].split('@')[0]
            print(Ti_2)
            os.system(Ti_2)  # execute MQTT command on CMD

        # if the element is V_2 extract the MQTT command line from the content
        elif temp_Ele == 'V_2':
            V_2 = contents[i].split('@')[0]
            print(V_2)
            os.system(V_2)  # execute MQTT command on CMD

        # if the element is W_2 extract the MQTT command line from the content
        elif temp_Ele == 'W_2':
            W_2 = contents[i].split('@')[0]
            print(W_2)
            os.system(W_2)  # execute MQTT command on CMD

        # if the element is Pb_2 extract the MQTT command line from the content
        elif temp_Ele == 'Pb_2':
            Pb_2 = contents[i].split('@')[0]
            print(Pb_2)
            os.system(Pb_2)  # execute MQTT command on CMD

        # if the element is Sn_2 extract the MQTT command line from the content
        elif temp_Ele == 'Sn_2':
            Sn_2 = contents[i].split('@')[0]
            print(Sn_2)
            os.system(Sn_2)  # execute MQTT command on CMD

        # if the element is As_2 extract the MQTT command line from the content
        elif temp_Ele == 'As_2':
            As_2 = contents[i].split('@')[0]
            print(As_2)
            os.system(As_2)  # execute MQTT command on CMD

        # if the element is Zr_2 extract the MQTT command line from the content
        elif temp_Ele == 'Zr_2':
            Zr_2 = contents[i].split('@')[0]
            print(Zr_2)
            os.system(Zr_2)  # execute MQTT command on CMD

        # if the element is Bi_2 extract the MQTT command line from the content
        elif temp_Ele == 'Bi_2':
            Bi_2 = contents[i].split('@')[0]
            print(Bi_2)
            os.system(Bi_2)  # execute MQTT command on CMD

        # if the element is Ca_2 extract the MQTT command line from the content
        elif temp_Ele == 'Ca_2':
            Ca_2 = contents[i].split('@')[0]
            print(Ca_2)
            os.system(Ca_2)  # execute MQTT command on CMD

        # if the element is Ce_2 extract the MQTT command line from the content
        elif temp_Ele == 'Ce_2':
            Ce_2 = contents[i].split('@')[0]
            print(Ce_2)
            os.system(Ce_2)  # execute MQTT command on CMD

        # if the element is Sb_2 extract the MQTT command line from the content
        elif temp_Ele == 'Sb_2':
            Sb_2 = contents[i].split('@')[0]
            print(Sb_2)
            os.system(Sb_2)  # execute MQTT command on CMD

        # if the element is Se_2 extract the MQTT command line from the content
        elif temp_Ele == 'Se_2':
            Se_2 = contents[i].split('@')[0]
            print(Se_2)
            os.system(Se_2)  # execute MQTT command on CMD

        # if the element is Te_2 extract the MQTT command line from the content
        elif temp_Ele == 'Te_2':
            Te_2 = contents[i].split('@')[0]
            print(Te_2)
            os.system(Te_2)  # execute MQTT command on CMD

        # if the element is Ta_2 extract the MQTT command line from the content
        elif temp_Ele == 'Ta_2':
            Ta_2 = contents[i].split('@')[0]
            print(Ta_2)
            os.system(Ta_2)  # execute MQTT command on CMD

        # if the element is B_2 extract the MQTT command line from the content
        elif temp_Ele == 'B_2':
            B_2 = contents[i].split('@')[0]
            print(B_2)
            os.system(B_2)  # execute MQTT command on CMD

        # if the element is Zn_2 extract the MQTT command line from the content
        elif temp_Ele == 'Zn_2':
            Zn_2 = contents[i].split('@')[0]
            print(Zn_2)
            os.system(Zn_2)  # execute MQTT command on CMD

        # if the element is La_2 extract the MQTT command line from the content
        elif temp_Ele == 'La_2':
            La_2 = contents[i].split('@')[0]
            print(La_2)
            os.system(La_2)  # execute MQTT command on CMD

        # if the element is Ag_2 extract the MQTT command line from the content
        elif temp_Ele == 'Ag_2':
            Ag_2 = contents[i].split('@')[0]
            print(Ag_2)
            os.system(Ag_2)  # execute MQTT command on CMD

        # if the element is N_2 extract the MQTT command line from the content
        elif temp_Ele == 'N_2':
            N_2 = contents[i].split('@')[0]
            print(N_2)
            os.system(N_2)  # execute MQTT command on CMD

        # if the element is O_2 extract the MQTT command line from the content
        elif temp_Ele == 'O_2':
            O_2 = contents[i].split('@')[0]
            print(O_2)
            os.system(O_2)  # execute MQTT command on CMD

        # if the element is Fe_2 extract the MQTT command line from the content
        elif temp_Ele == 'Fe_2':
            Fe_2 = contents[i].split('@')[0]
            print(Fe_2)
            os.system(Fe_2)  # execute MQTT command on CMD

        # if the element is Mg_2 extract the MQTT command line from the content
        elif temp_Ele == 'Mg_2':
            Mg_2 = contents[i].split('@')[0]
            print(Mg_2)
            os.system(Mg_2)  # execute MQTT command on CMD

        # if the element is Ba_2 extract the MQTT command line from the content
        elif temp_Ele == 'Ba_2':
            Ba_2 = contents[i].split('@')[0]
            print(Ba_2)
            os.system(Ba_2)  # execute MQTT command on CMD

        # if the element is Be_2 extract the MQTT command line from the content
        elif temp_Ele == 'Be_2':
            Be_2 = contents[i].split('@')[0]
            print(Be_2)
            os.system(Be_2)  # execute MQTT command on CMD

        # if the element is Cd_2 extract the MQTT command line from the content
        elif temp_Ele == 'Cd_2':
            Cd_2 = contents[i].split('@')[0]
            print(Cd_2)
            os.system(Cd_2)  # execute MQTT command on CMD

        # if the element is Ga_2 extract the MQTT command line from the content
        elif temp_Ele == 'Ga_2':
            Ga_2 = contents[i].split('@')[0]
            print(Ga_2)
            os.system(Ga_2)  # execute MQTT command on CMD

        # if the element is Hg_2 extract the MQTT command line from the content
        elif temp_Ele == 'Hg_2':
            Hg_2 = contents[i].split('@')[0]
            print(Hg_2)
            os.system(Hg_2)  # execute MQTT command on CMD

        # if the element is In_2 extract the MQTT command line from the content
        elif temp_Ele == 'In_2':
            In_2 = contents[i].split('@')[0]
            print(In_2)
            os.system(In_2)  # execute MQTT command on CMD

        # if the element is Li_2 extract the MQTT command line from the content
        elif temp_Ele == 'Li_2':
            Li_2 = contents[i].split('@')[0]
            print(Li_2)
            os.system(Li_2)  # execute MQTT command on CMD

        # if the element is Na_2 extract the MQTT command line from the content
        elif temp_Ele == 'Na_2':
            Na_2 = contents[i].split('@')[0]
            print(Na_2)
            os.system(Na_2)  # execute MQTT command on CMD

        # if the element is Sr_2 extract the MQTT command line from the content
        elif temp_Ele == 'Sr_2':
            Sr_2 = contents[i].split('@')[0]
            print(Sr_2)
            os.system(Sr_2)  # execute MQTT command on CMD

        # if the element is Sc_2 extract the MQTT command line from the content
        elif temp_Ele == 'Sc_2':
            Sc_2 = contents[i].split('@')[0]
            print(Sc_2)
            os.system(Sc_2)  # execute MQTT command on CMD

        # if the element is Hf_2 extract the MQTT command line from the content
        elif temp_Ele == 'Hf_2':
            Hf_2 = contents[i].split('@')[0]
            print(Hf_2)
            os.system(Hf_2)  # execute MQTT command on CMD

        # if the element is Re_2 extract the MQTT command line from the content
        elif temp_Ele == 'Re_2':
            Re_2 = contents[i].split('@')[0]
            print(Re_2)
            os.system(Re_2)  # execute MQTT command on CMD

        # if the element is C_3 extract the MQTT command line from the content
        elif temp_Ele == 'C_3':
            C_3 = contents[i].split('@')[0]
            print(C_3)
            os.system(C_3)  # execute MQTT command on CMD

        # if the element is Si_3 extract the MQTT command line from the content
        elif temp_Ele == 'Si_3':
            Si_3 = contents[i].split('@')[0]
            print(Si_3)
            os.system(Si_3)  # execute MQTT command on CMD

        # if the element is Mn_3 extract the MQTT command line from the content
        elif temp_Ele == 'Mn_3':
            Mn_3 = contents[i].split('@')[0]
            print(Mn_3)
            os.system(Mn_3)  # execute MQTT command on CMD

        # if the element is P_3 extract the MQTT command line from the content
        elif temp_Ele == 'P_3':
            P_3 = contents[i].split('@')[0]
            print(P_3)
            os.system(P_3)  # execute MQTT command on CMD

        # if the element is S_3 extract the MQTT command line from the content
        elif temp_Ele == 'S_3':
            S_3 = contents[i].split('@')[0]
            print(S_3)
            os.system(S_3)  # execute MQTT command on CMD

        # if the element is Cr_3 extract the MQTT command line from the content
        elif temp_Ele == 'Cr_3':
            Cr_3 = contents[i].split('@')[0]
            print(Cr_3)
            os.system(Cr_3)  # execute MQTT command on CMD

        # if the element is Mo_3 extract the MQTT command line from the content
        elif temp_Ele == 'Mo_3':
            Mo_3 = contents[i].split('@')[0]
            print(Mo_3)
            os.system(Mo_3)  # execute MQTT command on CMD

        # if the element is Ni_3 extract the MQTT command line from the content
        elif temp_Ele == 'Ni_3':
            Ni_3 = contents[i].split('@')[0]
            print(Ni_3)
            os.system(Ni_3)  # execute MQTT command on CMD

        # if the element is Al_3 extract the MQTT command line from the content
        elif temp_Ele == 'Al_3':
            Al_3 = contents[i].split('@')[0]
            print(Al_3)
            os.system(Al_3)  # execute MQTT command on CMD

        # if the element is Co_3 extract the MQTT command line from the content
        elif temp_Ele == 'Co_3':
            Co_3 = contents[i].split('@')[0]
            print(Co_3)
            os.system(Co_3)  # execute MQTT command on CMD

        # if the element is Cu_3 extract the MQTT command line from the content
        elif temp_Ele == 'Cu_3':
            Cu_3 = contents[i].split('@')[0]
            print(Cu_3)
            os.system(Cu_3)  # execute MQTT command on CMD

        # if the element is Nb_3 extract the MQTT command line from the content
        elif temp_Ele == 'Nb_3':
            Nb_3 = contents[i].split('@')[0]
            print(Nb_3)
            os.system(Nb_3)  # execute MQTT command on CMD

        # if the element is Ti_3 extract the MQTT command line from the content
        elif temp_Ele == 'Ti_3':
            Ti_3 = contents[i].split('@')[0]
            print(Ti_3)
            os.system(Ti_3)  # execute MQTT command on CMD

        # if the element is V_3 extract the MQTT command line from the content
        elif temp_Ele == 'V_3':
            V_3 = contents[i].split('@')[0]
            print(V_3)
            os.system(V_3)  # execute MQTT command on CMD

        # if the element is W_3 extract the MQTT command line from the content
        elif temp_Ele == 'W_3':
            W_3 = contents[i].split('@')[0]
            print(W_3)
            os.system(W_3)  # execute MQTT command on CMD

        # if the element is Pb_3 extract the MQTT command line from the content
        elif temp_Ele == 'Pb_3':
            Pb_3 = contents[i].split('@')[0]
            print(Pb_3)
            os.system(Pb_3)  # execute MQTT command on CMD

        # if the element is Sn_3 extract the MQTT command line from the content
        elif temp_Ele == 'Sn_3':
            Sn_3 = contents[i].split('@')[0]
            print(Sn_3)
            os.system(Sn_3)  # execute MQTT command on CMD

        # if the element is As_3 extract the MQTT command line from the content
        elif temp_Ele == 'As_3':
            As_3 = contents[i].split('@')[0]
            print(As_3)
            os.system(As_3)  # execute MQTT command on CMD

        # if the element is Zr_3 extract the MQTT command line from the content
        elif temp_Ele == 'Zr_3':
            Zr_3 = contents[i].split('@')[0]
            print(Zr_3)
            os.system(Zr_3)  # execute MQTT command on CMD

        # if the element is Bi_3 extract the MQTT command line from the content
        elif temp_Ele == 'Bi_3':
            Bi_3 = contents[i].split('@')[0]
            print(Bi_3)
            os.system(Bi_3)  # execute MQTT command on CMD

        # if the element is Ca_3 extract the MQTT command line from the content
        elif temp_Ele == 'Ca_3':
            Ca_3 = contents[i].split('@')[0]
            print(Ca_3)
            os.system(Ca_3)  # execute MQTT command on CMD

        # if the element is Ce_3 extract the MQTT command line from the content
        elif temp_Ele == 'Ce_3':
            Ce_3 = contents[i].split('@')[0]
            print(Ce_3)
            os.system(Ce_3)  # execute MQTT command on CMD

        # if the element is Sb_3 extract the MQTT command line from the content
        elif temp_Ele == 'Sb_3':
            Sb_3 = contents[i].split('@')[0]
            print(Sb_3)
            os.system(Sb_3)  # execute MQTT command on CMD

        # if the element is Se_3 extract the MQTT command line from the content
        elif temp_Ele == 'Se_3':
            Se_3 = contents[i].split('@')[0]
            print(Se_3)
            os.system(Se_3)  # execute MQTT command on CMD

        # if the element is Te_3 extract the MQTT command line from the content
        elif temp_Ele == 'Te_3':
            Te_3 = contents[i].split('@')[0]
            print(Te_3)
            os.system(Te_3)  # execute MQTT command on CMD

        # if the element is Ta_3 extract the MQTT command line from the content
        elif temp_Ele == 'Ta_3':
            Ta_3 = contents[i].split('@')[0]
            print(Ta_3)
            os.system(Ta_3)  # execute MQTT command on CMD

        # if the element is B_3 extract the MQTT command line from the content
        elif temp_Ele == 'B_3':
            B_3 = contents[i].split('@')[0]
            print(B_3)
            os.system(B_3)  # execute MQTT command on CMD

        # if the element is Zn_3 extract the MQTT command line from the content
        elif temp_Ele == 'Zn_3':
            Zn_3 = contents[i].split('@')[0]
            print(Zn_3)
            os.system(Zn_3)  # execute MQTT command on CMD

        # if the element is La_3 extract the MQTT command line from the content
        elif temp_Ele == 'La_3':
            La_3 = contents[i].split('@')[0]
            print(La_3)
            os.system(La_3)  # execute MQTT command on CMD

        # if the element is Ag_3 extract the MQTT command line from the content
        elif temp_Ele == 'Ag_3':
            Ag_3 = contents[i].split('@')[0]
            print(Ag_3)
            os.system(Ag_3)  # execute MQTT command on CMD

        # if the element is N_3 extract the MQTT command line from the content
        elif temp_Ele == 'N_3':
            N_3 = contents[i].split('@')[0]
            print(N_3)
            os.system(N_3)  # execute MQTT command on CMD

        # if the element is O_3 extract the MQTT command line from the content
        elif temp_Ele == 'O_3':
            O_3 = contents[i].split('@')[0]
            print(O_3)
            os.system(O_3)  # execute MQTT command on CMD

        # if the element is Fe_3 extract the MQTT command line from the content
        elif temp_Ele == 'Fe_3':
            Fe_3 = contents[i].split('@')[0]
            print(Fe_3)
            os.system(Fe_3)  # execute MQTT command on CMD

        # if the element is Mg_3 extract the MQTT command line from the content
        elif temp_Ele == 'Mg_3':
            Mg_3 = contents[i].split('@')[0]
            print(Mg_3)
            os.system(Mg_3)  # execute MQTT command on CMD

        # if the element is Ba_3 extract the MQTT command line from the content
        elif temp_Ele == 'Ba_3':
            Ba_3 = contents[i].split('@')[0]
            print(Ba_3)
            os.system(Ba_3)  # execute MQTT command on CMD

        # if the element is Be_3 extract the MQTT command line from the content
        elif temp_Ele == 'Be_3':
            Be_3 = contents[i].split('@')[0]
            print(Be_3)
            os.system(Be_3)  # execute MQTT command on CMD

        # if the element is Cd_3 extract the MQTT command line from the content
        elif temp_Ele == 'Cd_3':
            Cd_3 = contents[i].split('@')[0]
            print(Cd_3)
            os.system(Cd_3)  # execute MQTT command on CMD

        # if the element is Ga_3 extract the MQTT command line from the content
        elif temp_Ele == 'Ga_3':
            Ga_3 = contents[i].split('@')[0]
            print(Ga_3)
            os.system(Ga_3)  # execute MQTT command on CMD

        # if the element is Hg_3 extract the MQTT command line from the content
        elif temp_Ele == 'Hg_3':
            Hg_3 = contents[i].split('@')[0]
            print(Hg_3)
            os.system(Hg_3)  # execute MQTT command on CMD

        # if the element is In_3 extract the MQTT command line from the content
        elif temp_Ele == 'In_3':
            In_3 = contents[i].split('@')[0]
            print(In_3)
            os.system(In_3)  # execute MQTT command on CMD

        # if the element is Li_3 extract the MQTT command line from the content
        elif temp_Ele == 'Li_3':
            Li_3 = contents[i].split('@')[0]
            print(Li_3)
            os.system(Li_3)  # execute MQTT command on CMD

        # if the element is Na_3 extract the MQTT command line from the content
        elif temp_Ele == 'Na_3':
            Na_3 = contents[i].split('@')[0]
            print(Na_3)
            os.system(Na_3)  # execute MQTT command on CMD

        # if the element is Sr_3 extract the MQTT command line from the content
        elif temp_Ele == 'Sr_3':
            Sr_3 = contents[i].split('@')[0]
            print(Sr_3)
            os.system(Sr_3)  # execute MQTT command on CMD

        # if the element is Sc_3 extract the MQTT command line from the content
        elif temp_Ele == 'Sc_3':
            Sc_3 = contents[i].split('@')[0]
            print(Sc_3)
            os.system(Sc_3)  # execute MQTT command on CMD

        # if the element is Hf_3 extract the MQTT command line from the content
        elif temp_Ele == 'Hf_3':
            Hf_3 = contents[i].split('@')[0]
            print(Hf_3)
            os.system(Hf_3)  # execute MQTT command on CMD

        # if the element is Re_3 extract the MQTT command line from the content
        elif temp_Ele == 'Re_3':
            Re_3 = contents[i].split('@')[0]
            print(Re_3)
            os.system(Re_3)  # execute MQTT command on CMD

        # if the element is C_Rep extract the MQTT command line from the content
        elif temp_Ele == 'C_Rep':
            C_Rep = contents[i].split('@')[0]
            print(C_Rep)
            os.system(C_Rep)  # execute MQTT command on CMD

        # if the element is Si_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Si_Rep':
            Si_Rep = contents[i].split('@')[0]
            print(Si_Rep)
            os.system(Si_Rep)  # execute MQTT command on CMD

        # if the element is Mn_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Mn_Rep':
            Mn_Rep = contents[i].split('@')[0]
            print(Mn_Rep)
            os.system(Mn_Rep)  # execute MQTT command on CMD

        # if the element is P_Rep extract the MQTT command line from the content
        elif temp_Ele == 'P_Rep':
            P_Rep = contents[i].split('@')[0]
            print(P_Rep)
            os.system(P_Rep)  # execute MQTT command on CMD

        # if the element is S_Rep extract the MQTT command line from the content
        elif temp_Ele == 'S_Rep':
            S_Rep = contents[i].split('@')[0]
            print(S_Rep)
            os.system(S_Rep)  # execute MQTT command on CMD

        # if the element is Cr_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Cr_Rep':
            Cr_Rep = contents[i].split('@')[0]
            print(Cr_Rep)
            os.system(Cr_Rep)  # execute MQTT command on CMD

        # if the element is Mo_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Mo_Rep':
            Mo_Rep = contents[i].split('@')[0]
            print(Mo_Rep)
            os.system(Mo_Rep)  # execute MQTT command on CMD

        # if the element is Ni_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Ni_Rep':
            Ni_Rep = contents[i].split('@')[0]
            print(Ni_Rep)
            os.system(Ni_Rep)  # execute MQTT command on CMD

        # if the element is Al_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Al_Rep':
            Al_Rep = contents[i].split('@')[0]
            print(Al_Rep)
            os.system(Al_Rep)  # execute MQTT command on CMD

        # if the element is Co_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Co_Rep':
            Co_Rep = contents[i].split('@')[0]
            print(Co_Rep)
            os.system(Co_Rep)  # execute MQTT command on CMD

        # if the element is Cu_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Cu_Rep':
            Cu_Rep = contents[i].split('@')[0]
            print(Cu_Rep)
            os.system(Cu_Rep)  # execute MQTT command on CMD

        # if the element is Nb_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Nb_Rep':
            Nb_Rep = contents[i].split('@')[0]
            print(Nb_Rep)
            os.system(Nb_Rep)  # execute MQTT command on CMD

        # if the element is Ti_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Ti_Rep':
            Ti_Rep = contents[i].split('@')[0]
            print(Ti_Rep)
            os.system(Ti_Rep)  # execute MQTT command on CMD

        # if the element is V_Rep extract the MQTT command line from the content
        elif temp_Ele == 'V_Rep':
            V_Rep = contents[i].split('@')[0]
            print(V_Rep)
            os.system(V_Rep)  # execute MQTT command on CMD

        # if the element is W_Rep extract the MQTT command line from the content
        elif temp_Ele == 'W_Rep':
            W_Rep = contents[i].split('@')[0]
            print(W_Rep)
            os.system(W_Rep)  # execute MQTT command on CMD

        # if the element is Pb_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Pb_Rep':
            Pb_Rep = contents[i].split('@')[0]
            print(Pb_Rep)
            os.system(Pb_Rep)  # execute MQTT command on CMD

        # if the element is Sn_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Sn_Rep':
            Sn_Rep = contents[i].split('@')[0]
            print(Sn_Rep)
            os.system(Sn_Rep)  # execute MQTT command on CMD

        # if the element is As_Rep extract the MQTT command line from the content
        elif temp_Ele == 'As_Rep':
            As_Rep = contents[i].split('@')[0]
            print(As_Rep)
            os.system(As_Rep)  # execute MQTT command on CMD

        # if the element is Zr_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Zr_Rep':
            Zr_Rep = contents[i].split('@')[0]
            print(Zr_Rep)
            os.system(Zr_Rep)  # execute MQTT command on CMD

        # if the element is Bi_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Bi_Rep':
            Bi_Rep = contents[i].split('@')[0]
            print(Bi_Rep)
            os.system(Bi_Rep)  # execute MQTT command on CMD

        # if the element is Ca_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Ca_Rep':
            Ca_Rep = contents[i].split('@')[0]
            print(Ca_Rep)
            os.system(Ca_Rep)  # execute MQTT command on CMD

        # if the element is Ce_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Ce_Rep':
            Ce_Rep = contents[i].split('@')[0]
            print(Ce_Rep)
            os.system(Ce_Rep)  # execute MQTT command on CMD

        # if the element is Sb_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Sb_Rep':
            Sb_Rep = contents[i].split('@')[0]
            print(Sb_Rep)
            os.system(Sb_Rep)  # execute MQTT command on CMD

        # if the element is Se_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Se_Rep':
            Se_Rep = contents[i].split('@')[0]
            print(Se_Rep)
            os.system(Se_Rep)  # execute MQTT command on CMD

        # if the element is Te_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Te_Rep':
            Te_Rep = contents[i].split('@')[0]
            print(Te_Rep)
            os.system(Te_Rep)  # execute MQTT command on CMD

        # if the element is Ta_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Ta_Rep':
            Ta_Rep = contents[i].split('@')[0]
            print(Ta_Rep)
            os.system(Ta_Rep)  # execute MQTT command on CMD

        # if the element is B_Rep extract the MQTT command line from the content
        elif temp_Ele == 'B_Rep':
            B_Rep = contents[i].split('@')[0]
            print(B_Rep)
            os.system(B_Rep)  # execute MQTT command on CMD

        # if the element is Zn_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Zn_Rep':
            Zn_Rep = contents[i].split('@')[0]
            print(Zn_Rep)
            os.system(Zn_Rep)  # execute MQTT command on CMD

        # if the element is La_Rep extract the MQTT command line from the content
        elif temp_Ele == 'La_Rep':
            La_Rep = contents[i].split('@')[0]
            print(La_Rep)
            os.system(La_Rep)  # execute MQTT command on CMD

        # if the element is Ag_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Ag_Rep':
            Ag_Rep = contents[i].split('@')[0]
            print(Ag_Rep)
            os.system(Ag_Rep)  # execute MQTT command on CMD

        # if the element is N_Rep extract the MQTT command line from the content
        elif temp_Ele == 'N_Rep':
            N_Rep = contents[i].split('@')[0]
            print(N_Rep)
            os.system(N_Rep)  # execute MQTT command on CMD

        # if the element is O_Rep extract the MQTT command line from the content
        elif temp_Ele == 'O_Rep':
            O_Rep = contents[i].split('@')[0]
            print(O_Rep)
            os.system(O_Rep)  # execute MQTT command on CMD

        # if the element is Fe_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Fe_Rep':
            Fe_Rep = contents[i].split('@')[0]
            print(Fe_Rep)
            os.system(Fe_Rep)  # execute MQTT command on CMD

        # if the element is Mg_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Mg_Rep':
            Mg_Rep = contents[i].split('@')[0]
            print(Mg_Rep)
            os.system(Mg_Rep)  # execute MQTT command on CMD

        # if the element is Ba_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Ba_Rep':
            Ba_Rep = contents[i].split('@')[0]
            print(Ba_Rep)
            os.system(Ba_Rep)  # execute MQTT command on CMD

        # if the element is Be_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Be_Rep':
            Be_Rep = contents[i].split('@')[0]
            print(Be_Rep)
            os.system(Be_Rep)  # execute MQTT command on CMD

        # if the element is Cd_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Cd_Rep':
            Cd_Rep = contents[i].split('@')[0]
            print(Cd_Rep)
            os.system(Cd_Rep)  # execute MQTT command on CMD

        # if the element is Ga_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Ga_Rep':
            Ga_Rep = contents[i].split('@')[0]
            print(Ga_Rep)
            os.system(Ga_Rep)  # execute MQTT command on CMD

        # if the element is Hg_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Hg_Rep':
            Hg_Rep = contents[i].split('@')[0]
            print(Hg_Rep)
            os.system(Hg_Rep)  # execute MQTT command on CMD

        # if the element is In_Rep extract the MQTT command line from the content
        elif temp_Ele == 'In_Rep':
            In_Rep = contents[i].split('@')[0]
            print(In_Rep)
            os.system(In_Rep)  # execute MQTT command on CMD

        # if the element is Li_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Li_Rep':
            Li_Rep = contents[i].split('@')[0]
            print(Li_Rep)
            os.system(Li_Rep)  # execute MQTT command on CMD

        # if the element is Na_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Na_Rep':
            Na_Rep = contents[i].split('@')[0]
            print(Na_Rep)
            os.system(Na_Rep)  # execute MQTT command on CMD

        # if the element is Sr_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Sr_Rep':
            Sr_Rep = contents[i].split('@')[0]
            print(Sr_Rep)
            os.system(Sr_Rep)  # execute MQTT command on CMD

        # if the element is Sc_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Sc_Rep':
            Sc_Rep = contents[i].split('@')[0]
            print(Sc_Rep)
            os.system(Sc_Rep)  # execute MQTT command on CMD

        # if the element is Hf_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Hf_Rep':
            Hf_Rep = contents[i].split('@')[0]
            print(Hf_Rep)
            os.system(Hf_Rep)  # execute MQTT command on CMD

        # if the element is Re_Rep extract the MQTT command line from the content
        elif temp_Ele == 'Re_Rep':
            Re_Rep = contents[i].split('@')[0]
            print(Re_Rep)
            os.system(Re_Rep)  # execute MQTT command on CMD

        else:
            continue

f.close()

print('---cmd for MQTT broker end---')

# get current datetime in UTC format
utc_time_temp = datetime.utcnow()
print("Current UTC Time is :", utc_time_temp)

# change UTC time into MQTT acceptable format
utc_time_temp = str(utc_time_temp)
utc_time = utc_time_temp[0] + utc_time_temp[1] + utc_time_temp[2] + utc_time_temp[3] + utc_time_temp[4] + \
           utc_time_temp[5] + utc_time_temp[6] + utc_time_temp[7] + utc_time_temp[8] + utc_time_temp[9] + "_" + \
           utc_time_temp[11] + utc_time_temp[12] + utc_time_temp[13] + utc_time_temp[14] + utc_time_temp[15] + \
           utc_time_temp[16] + utc_time_temp[17] + utc_time_temp[18]
print("New UTC Time format : " + utc_time)

# upload the UTC_timestamp as a flag to distinguish each update of MQTT
UTC_timestamp = "cmd" + " /c " + '"' + "cd C:\Mosquitto & mosquitto_pub -h 10.72.55.30 -t UTC_timestamp" + \
                " -m " + str(utc_time) + " -u mqttuser2 -P Mqtt123456" + '"'
print(UTC_timestamp)

# upload UTC time to ThingWorx platform
os.system(UTC_timestamp)

print('---Python script end---')
