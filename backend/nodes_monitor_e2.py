'''
Author: Gerry Meixiong
Made July 2015
Markov States of Hepatitis B
'''
import math 

pVar = -1.0
dVar = -2.0

cCHB = 693
cCirr = 2035
cDecompCirr = 7068
cEntecavir = 5987
cHCC = 15600
cLT = 125000
cMonitor = 120
discountC = 0.03
discountU = 0.03
uCHB = 0.85
uCHBinactive = 0.95
uCHBseroclearance = 0.99
uResolution = 1
uSVR = 1
uSeroclearance = 1

tested_rate = 0.58
followup_rate = 0.587
treatment_rate = 0.33

p_adherence = 1
p_monitor = 1

# Touch this part
cohortPop = 100

def getUCirr(age):
    if age <= 24:
        return 0.68
    elif age <= 34:
        return 0.7
    elif age <= 44:
        return 0.68
    elif age <= 54:
        return 0.7
    else:
        return 0.66

def getUDecompCirr(age):
    if age <= 24:
        return 0.3
    elif age <= 34:
        return 0.31
    elif age <= 44:
        return 0.38
    elif age <= 54:
        return 0.35
    else:
        return 0.37

def getUHCC(age):
    if age <= 24:
        return 0.32
    elif age <= 34:
        return 0.37
    elif age <= 44:
        return 0.41
    elif age <= 54:
        return 0.39
    else:
        return 0.41

def getULT(age):
    if age <= 24:
        return 0.62
    elif age <= 34:
        return 0.68
    elif age <= 44:
        return 0.69
    elif age <= 54:
        return 0.68
    else:
        return 0.66

class BasicNode(object):

    def __init__(self, OV):
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = None
        self.destStates = []
        self.probValUT =  None
        self.probValATF = None
        self.probValUTF = None
        self.probValLET = None
        self.probValAT =  None
        self.probValAFR = None
        self.probValAFF = None
        self.isCirrhosis = False
        self.guac = 0

    def __str__(self):
        return str(self.originValue)

    def getID(self):
        return self.ID

    def getOriginValue(self):
        return self.originValue

    def getVarName(self):
        return self.varName

    def getDestStates(self):
        return self.destStates

    def getProbValUTF(self):
        try:
            return self.probValUTF
        except:
            return None

    def getProbValATF(self):
        return self.probValATF

    def getProbValUT(self):
        return self.probValUT

    def getProbValLET(self):
        return self.probValLET

    def getProbValAT(self):
        return self.probValAT

    def getProbValAFR(self):
        return self.probValAFR

    def getProbValAFF(self):
        return self.probValAFF

    def getGuac(self):
        return self.guac

    def nextStage(self,destStates, originVal, probList, cirrIgn, currNode = None):
        temp = []
        for i in range(0, len(destStates)):
            tempNode = destStates[i](originVal * probList[i]) 
            temp.append(tempNode)
            if tempNode.getID() == currNode.getID():
                tempNode.guac += tempNode.getOriginValue()
            if tempNode.isCirrhosis and not currNode.isCirrhosis:
                cirrIgn += tempNode.getOriginValue()

        return temp, cirrIgn


def getMort(age):
    if age == 0:
        return 0.001947564
    elif age <= 4:
        return 0.000347779
    elif age <= 9:
        return 0.000167785
    elif age <= 14:
        return 0.000140057
    elif age <= 19:
        return 0.000229494
    elif age <= 24:
        return 0.000290839
    elif age <= 29:
        return 0.00034194
    elif age <= 34:
        return 0.000404525
    elif age <= 39:
        return 0.000592417
    elif age <= 44:
        return 0.000987346
    elif age <= 49:
        return 0.001698871
    elif age <= 54:
        return 0.002997754
    elif age <= 59:
        return 0.004753559
    elif age <= 64:
        return 0.007465249
    elif age <= 69:
        return 0.012523989
    elif age <= 74:
        return 0.01965294
    elif age <= 79:
        return 0.075699955
    elif age <= 84:
        return 0.139918705
    elif age <= 89:
        return 0.444573737
    elif age <= 110:
        return 0.830838984
    else:
        return 1

def getInitialNodes(age):
    if (age <= 14):
        totalPopulation = 18788587
        HBsAgPrevalence = .0284
        HBeAgPosRate = .531914893617021
        HBeAgNegRate = .468085106382979
        ActiveCHBePosRate = .346153846153846
        ActiveCHBeNegRate = .19047619047619
        CirrHBePos = .020
        CirrHBeNeg = .050
    if age >= 15 and age <= 24:
        totalPopulation = 12441662
        HBsAgPrevalence = .0394
        HBeAgPosRate = .360
        HBeAgNegRate = .640
        ActiveCHBePosRate = .518518518518518
        ActiveCHBeNegRate = .147368421052632
        CirrHBePos = .020
        CirrHBeNeg = .050
    if age >= 25 and age <= 34:
        totalPopulation = 12328944
        HBsAgPrevalence = .0636
        HBeAgPosRate = .204
        HBeAgNegRate = .796
        ActiveCHBePosRate = .700
        ActiveCHBeNegRate = .213197969543147
        CirrHBePos = .060
        CirrHBeNeg = .070
    if age >= 35 and age <= 44:
        totalPopulation = 10070734
        HBsAgPrevalence = .0620
        HBeAgPosRate = .100
        HBeAgNegRate = .900
        ActiveCHBePosRate = .564102564102564
        ActiveCHBeNegRate = .171919770773639
        CirrHBePos = .070
        CirrHBeNeg = .150
    if age >= 45 and age <= 54:
        totalPopulation = 7927348
        HBsAgPrevalence = .0552
        HBeAgPosRate = .0517711171662125
        HBeAgNegRate = .948228882833787
        ActiveCHBePosRate = .526315789473684
        ActiveCHBeNegRate = .179190751445087
        CirrHBePos = .250
        CirrHBeNeg = .280
    if age >= 55 and age <= 64:
        totalPopulation = 5066402
        HBsAgPrevalence = .0365
        HBeAgPosRate = .0689655172413793
        HBeAgNegRate = .931034482758621
        ActiveCHBePosRate = .583333333333333
        ActiveCHBeNegRate = .236024844720497
        CirrHBePos = .330
        CirrHBeNeg = .510
    if age >= 65:
        totalPopulation = 4893423
        HBsAgPrevalence = .0403
        HBeAgPosRate = .0925925925925926
        HBeAgNegRate = .907407407407407
        ActiveCHBePosRate = .250
        ActiveCHBeNegRate = .208333333333333
        CirrHBePos = .000
        CirrHBeNeg = .560

    population = int(round(totalPopulation * HBsAgPrevalence, 0))

    HBsAg = int(round((totalPopulation * HBsAgPrevalence) - (totalPopulation * HBsAgPrevalence * HBeAgPosRate
    * ActiveCHBePosRate) - (totalPopulation * HBsAgPrevalence * HBeAgNegRate * ActiveCHBeNegRate), 0))

    CHB = int(round((totalPopulation * HBsAgPrevalence * HBeAgPosRate * ActiveCHBePosRate) - (totalPopulation
    * HBsAgPrevalence * HBeAgPosRate * ActiveCHBePosRate * CirrHBePos), 0))

    CHBneg = int(round((totalPopulation * HBsAgPrevalence * HBeAgNegRate * ActiveCHBeNegRate) - (totalPopulation
    * HBsAgPrevalence * HBeAgNegRate * ActiveCHBeNegRate * CirrHBeNeg), 0))

    Cirr = int(round((totalPopulation * HBsAgPrevalence * HBeAgPosRate * ActiveCHBePosRate
    * CirrHBePos) + (totalPopulation * HBsAgPrevalence * HBeAgNegRate * ActiveCHBeNegRate * CirrHBeNeg), 0))

    PCHB = round((CHB * tested_rate * followup_rate * treatment_rate) / population, 3)                      #4
    PCHBNH = round((CHB - CHB * tested_rate * followup_rate * treatment_rate) / population, 3)              #28
    PCHBneg = round((CHBneg * tested_rate * followup_rate * treatment_rate) / population, 3)                #5
    PCHBnegNH = round((CHBneg - CHBneg * tested_rate * followup_rate * treatment_rate) / population, 3)     #29
    Pcirr = round((Cirr * tested_rate * followup_rate * treatment_rate) / population, 3)                    #6
    PcirrNH = round((Cirr - Cirr * tested_rate * followup_rate * treatment_rate) / population, 3)           #30
    PHBsAg = round((HBsAg * tested_rate * followup_rate) / population, 3)
    PHBsAgNH = 1 - PHBsAg - PCHB - PCHBNH - PCHBneg - PCHBnegNH - Pcirr - PcirrNH                         #26

    if p_monitor == 0:
        PHBsAg = 0

    return [Node02(PHBsAg), Node26(PHBsAgNH), Node04(PCHB), Node28(PCHBNH), Node05(PCHBneg), Node29(PCHBnegNH), Node06(Pcirr), Node30(PcirrNH)]

def getCost(varName, stage):
    dic = {"HBsAg Seroclearance" : 0,                                                                  #1
    "HBsAg +" : 0,                                                                                     #2
    "HBeAg Seroconversion" : (cCHB + cEntecavir) / math.pow(1 + discountC, stage),                     #3
    "CHBe+" : cCHB / math.pow(1 + discountC, stage),                                                   #4
    "CHBe- disease" : cCHB / math.pow(1 + discountC, stage),                                           #5
    "Cirrhosis" : cCirr / math.pow(1 + discountC, stage),                                              #6
    "DecompCirr" : cDecompCirr / math.pow(1 + discountC, stage),                                       #7
    "HCC" : cHCC / math.pow(1 + discountC, stage),                                                     #8
    "Liver Transplantation" : cLT / math.pow(1 + discountC, stage),                                    #9
    "Sustained Virological Response" : cEntecavir / math.pow(1 + discountC, stage),                    #10
    "CHB initial Rx" : (cCHB + cEntecavir) / math.pow(1 + discountC, stage),                           #11
    "CHB Long Term Rx" : (cCHB + cEntecavir) / math.pow(1 + discountC, stage),                         #12
    "CHB Long Term with Rx with Resistance" : (cCHB + cEntecavir) / math.pow(1 + discountC, stage),    #13
    "Cirrhosis Initial Rx" : (cCirr + cEntecavir) / math.pow(1 + discountC, stage),                    #14
    "Cirrhosis Long Term Rx" : (cCirr + cEntecavir) / math.pow(1 + discountC, stage),                  #15
    "Cirrhosis Long Term Rx with resistance" : (cCirr + cEntecavir) / math.pow(1 + discountC, stage),  #16
    "CHBe- initial Rx" : (cCHB + cEntecavir) / math.pow(1 + discountC, stage),                         #17
    "CHBe- longterm Rx" : (cCHB + cEntecavir) / math.pow(1 + discountC, stage),                        #18
    "CHBe- longterm Rx resistance" : (cCHB + cEntecavir) / math.pow(1 + discountC, stage),             #19
    "Cirrhosis e- initial Rx" : (cCirr + cEntecavir) / math.pow(1 + discountC, stage),                 #20
    "Cirrhosis e- longterm Rx" : (cCirr + cEntecavir) / math.pow(1 + discountC, stage),                #21
    "Cirrhosis e- longterm Rx with resistance" : (cCirr + cEntecavir) / math.pow(1 + discountC, stage),#22
    "Death HBV" : 0,                                                                                   #23
    "Death (Other)" : 0,                                                                               #24
    "HBsAg SeroclearanceNH" : 0,                                                                       #25
    "HBsAg + NH" : 0,                                                                                  #26
    "HBeAg SeroconversionNH" : cCHB / math.pow(1 + discountC, stage),                                  #27
    "CHBe+NH" : cCHB / math.pow(1 + discountC, stage),                                                 #28
    "CHB e- diseaseNH" : cCHB / math.pow(1 + discountC, stage),                                        #29
    "Cirrhosis NH" : cCirr / math.pow(1 + discountC, stage),                                           #30
    "DecompCirr NH" : cDecompCirr / math.pow(1 + discountC, stage),                                    #31
    "HCC NH" : cHCC / math.pow(1 + discountC, stage),                                                  #32
    "Liver Transplantation NH" : cLT / math.pow(1 + discountC, stage),                                 #33
    "Death HBV NH" : 0,                                                                                #34
    "Death Other NH" : 0,                                                                              #35
    "HBsAg + Monitor" : cMonitor / math.pow(1 + discountC, stage)                                      #36
    }

    if p_monitor != 0:
        dic["HBsAg +"] = cMonitor  / math.pow(1 + discountC, stage)
        dic["HBeAg SeroconversionNH"] = 0

    if str(varName) in dic.keys():
        return dic[str(varName)]

def getUtility(varName, stage, age):
    uCirr = getUCirr(age)
    uDecompCirr = getUDecompCirr(age)
    uHCC = getUHCC(age)
    uLiverTransplant = getULT(age)

    dic = {"HBsAg Seroclearance" : uSeroclearance / math.pow(1 + discountU, stage),                    #1
    "HBsAg +" : uCHBinactive / math.pow(1 + discountU, stage),                                         #2
    "HBeAg Seroconversion" : uCHBinactive / math.pow(1 + discountU, stage),                            #3
    "CHBe+" : uCHB / math.pow(1 + discountU, stage),                                                   #4
    "CHBe- disease" : uCHB / math.pow(1 + discountU, stage),                                           #5
    "Cirrhosis" : uCirr / math.pow(1 + discountU, stage),                                              #6
    "DecompCirr" : uDecompCirr / math.pow(1 + discountU, stage),                                       #7
    "HCC" : uHCC / math.pow(1 + discountU, stage),                                                     #8
    "Liver Transplantation" : uLiverTransplant / math.pow(1 + discountU, stage),                       #9
    "Sustained Virological Response" : uSVR / math.pow(1 + discountU, stage),                          #10
    "CHB initial Rx" : uCHB / math.pow(1 + discountU, stage),                                          #11
    "CHB Long Term Rx" : uCHB / math.pow(1 + discountU, stage),                                        #12
    "CHB Long Term with Rx with Resistance" : uCHB / math.pow(1 + discountU, stage),                   #13
    "Cirrhosis Initial Rx" : uCirr / math.pow(1 + discountU, stage),                                   #14
    "Cirrhosis Long Term Rx" : uCirr / math.pow(1 + discountU, stage),                                 #15
    "Cirrhosis Long Term Rx with resistance" : uCirr / math.pow(1 + discountU, stage),                 #16
    "CHBe- initial Rx" : uCHB / math.pow(1 + discountU, stage),                                        #17
    "CHBe- longterm Rx" : uCHB / math.pow(1 + discountU, stage),                                       #18
    "CHBe- longterm Rx resistance" : uCHB / math.pow(1 + discountU, stage),                            #19
    "Cirrhosis e- initial Rx" : uCirr / math.pow(1 + discountU, stage),                                #20
    "Cirrhosis e- longterm Rx" : uCirr / math.pow(1 + discountU, stage),                               #21
    "Cirrhosis e- longterm Rx with resistance" : uCirr / math.pow(1 + discountU, stage),               #22
    "Death HBV" : 0,                                                                                   #23
    "Death (Other)" : 0,                                                                               #24
    "HBsAg SeroclearanceNH" : uSeroclearance / math.pow(1 + discountU, stage),                         #25
    "HBsAg + NH" : uCHBinactive / math.pow(1 + discountU, stage),                                      #26
    "HBeAg SeroconversionNH" : uCHBinactive / math.pow(1 + discountU, stage),                          #27
    "CHBe+NH" : uCHB / math.pow(1 + discountU, stage),                                                 #28
    "CHB e- diseaseNH" : uCHB / math.pow(1 + discountU, stage),                                        #29
    "Cirrhosis NH" : uCirr / math.pow(1 + discountU, stage),                                           #30
    "DecompCirr NH" : uDecompCirr / math.pow(1 + discountU, stage),                                    #31
    "HCC NH" : uHCC / math.pow(1 + discountU, stage),                                                  #32
    "Liver Transplantation NH" : uLiverTransplant / math.pow(1 + discountU, stage),                    #33
    "Death HBV NH" : 0,                                                                                #34
    "Death Other NH" : 0,                                                                              #35
    "HBsAg + Monitor" : uCHBinactive / math.pow(1 + discountU, stage)                                  #36
    }
    if str(varName) in dic.keys():
        return dic[str(varName)]

#Basic Calculation Functions
def printCummTestValues(list):
    for i in list:
        if i.getVarName() == 'Cirrhosis NH' or i.getVarName() == 'Cirrhosis Initial Rx' or i.getVarName() == 'HCC' or i.getVarName() == 'HCC NH':
            print ("%-40s %10.5f" % (i.getVarName(), round(i.getOriginValue(),5),))
        if i.getVarName() == 'Liver Transplantation NH' or i.getVarName() == 'Death HBV NH' or i.getVarName() == 'Liver Transplantation' or i.getVarName == 'Death HBV':
            print ("%-40s %10.5f" % (i.getVarName(), round(i.getOriginValue(),5),))

def printList(list):
    for i in list:
        print ("%-40s %10.5f" % (i.getVarName(), round(i.getOriginValue()*cohortPop,5),))

def sumList(list):
    sum = 0
    for i in list:
        sum += i.getOriginValue()
    return sum

def printCost(list, stage, total_stages):
    for i in list:
        if stage == 0 or stage == total_stages:
            print ("%-40s %10f" % (i.getVarName(), i.getOriginValue() * getCost(i.getVarName(), stage) * 0.5))
        else:
            print ("%-40s %10f" % (i.getVarName(), i.getOriginValue() * getCost(i.getVarName(), stage)))

def printUtility(list, stage, total_stages, age):
    for i in list:
        if stage == 0 or stage == total_stages:
            print ("%-40s %10f" % (i.getVarName(), i.getOriginValue() * getUtility(i.getVarName(), stage, age) * 0.5))
        else:
            print ("%-40s %10f" % (i.getVarName(), i.getOriginValue() * getUtility(i.getVarName(), stage, age)))

def sumCost(list, stage, total_stages):
    sum = 0
    for i in list:
        if(stage == 0 or stage == total_stages):
            sum += i.getOriginValue() * getCost(i.getVarName(), stage) * 0.5
        else:
            sum += i.getOriginValue() * getCost(i.getVarName(), stage)
    return sum

def sumUtility(list, stage, age, total_stages):
    sum = 0
    for i in list:
        if (stage == 0 or stage == total_stages):
            sum += i.getOriginValue() * getUtility(i.getVarName(), stage, age) * 0.5
        else:
            sum += i.getOriginValue() * getUtility(i.getVarName(), stage, age)
    return sum

def getOrginValSum(list):
    sum = 0
    for node in list:
        sum += node.getOriginValue()
    return sum

#Prob List Manipulation Functions
def pVarReplace(list):
    pVarOcc = 0

    for i in range(0, len(list)):
        if list[i] < 0:
            pVarOcc += 1

    if pVarOcc is not 0:
        total = sum(list)
        for i in range(0, len(list)):
            if  list[i] < 0:
               list[i] *= total

    return list

def dVarReplace(list, age):
    if dVar in list:
        dIndex = list.index(dVar)
        dRate = getMort(age-1)
        if dRate == 1:
            for i in range(0,len(list)):
                list[i] = 0.0
        list[dIndex] = dRate
    return list

def trimList(array):   # sums up all nodes with same name to create a neat array
    resultList = sorted(array, key=lambda array: array.ID)
    i = 0
    while i < len(resultList)-1:
        if resultList[i].getID() == resultList[i+1].getID():
            resultList[i].originValue = (resultList[i].getOriginValue() + resultList[i+1].getOriginValue())
            del resultList[i+1]
        else:
            i += 1
    return resultList

#The Nodes
class Node01(BasicNode):

    def __init__(self, OV):
        super(Node01, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg Seroclearance"
        self.destStates = [Node01, Node32, Node35]
        self.probValUT =  [pVar  , 0     , dVar]
        self.probValAFF = [pVar  , 0.01  , dVar]

class Node02(BasicNode):

    def __init__(self, OV):
        super(Node02, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg +"
        self.destStates = [Node36    ,       Node26]
        self.probValUT =  [p_monitor      ,    1 - p_monitor]

class Node03(BasicNode):

    def __init__(self, OV):
        super(Node03, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBeAg Seroconversion"
        self.destStates = [Node03, Node01, Node18, Node29,  Node35]
        self.probValUT =  [pVar  , 0.008 , 0.029 , 0.029 ,  dVar]
        self.probValAT =  [pVar  , 0.007 , 0.038 , 0.038 ,  dVar]
        self.probValAFR = [pVar  , 0.003 , 0.086 , 0.086 ,  dVar]
        self.secBranch =  [1     , 1     , p_adherence , 1 - p_adherence  ,  1]


class Node04(BasicNode):

    def __init__(self, OV):
        super(Node04, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe+"
        self.destStates = [Node11, Node28 , Node03 , Node08, Node17 , Node29 , Node14 , Node30 , Node35]
        self.probValUTF = [pVar  , pVar   , 0.09   , 0.001,  0.019  , 0.019  , 0.001  , 0.001  ,  dVar ]
        self.probValLET = [pVar  , pVar   , 0.09   , 0.003,  0.019  , 0.019  , 0.038  , 0.038  ,  dVar ]
        self.probValAT =  [pVar  , pVar   , 0.07   , 0.003,  0.019  , 0.019  , 0.038  , 0.038  ,  dVar ]
        self.secBranch =  [p_adherence  , 1 - p_adherence   , 1      , 1, p_adherence   , 1 - p_adherence   , p_adherence   , 1 - p_adherence  ,  1]

class Node05(BasicNode):

    def __init__(self, OV):
        super(Node05, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- disease"
        self.destStates = [Node08, Node17, Node29, Node14, Node30, Node35]
        self.probValUTF = [0.001,  pVar  , pVar  , 0.001 , 0.001 , dVar]
        self.probValATF = [0.003,  pVar  , pVar  , 0.009 , 0.009 , dVar]
        self.secBranch =  [1, p_adherence  , 1 - p_adherence  , p_adherence  ,1 - p_adherence , 1 ]

class Node06(BasicNode):

    def __init__(self, OV):
        super(Node06, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis"
        self.isCirrhosis = True
        self.destStates = [Node14, Node30, Node35]
        self.probValUT =  [pVar  , pVar  , dVar]
        self.secBranch =  [p_adherence  , 1 - p_adherence  , 1 ]

class Node07(BasicNode):

    def __init__(self, OV):
        super(Node07, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "DecompCirr"
        self.destStates = [Node07, Node08, Node09, Node23, Node35]
        self.probValUT =  [pVar  , 0.0710,   0.23, 0.26,   dVar]

class Node08(BasicNode):

    def __init__(self, OV):
        super(Node08, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HCC"
        self.destStates = [Node08,  Node09, Node23, Node35]
        self.probValUT =  [pVar  ,   0.06,  0.35,   dVar]

class Node09(BasicNode):

    def __init__(self, OV):
        super(Node09, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Liver Transplantation"
        self.destStates = [Node09, Node23, Node35]
        self.probValUT =  [pVar  ,  0.066,   dVar]

class Node10(BasicNode):
    def __init__(self, OV):
        super(Node10, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Sustained Virological Response"
        self.destStates = [Node08, Node10, Node14, Node35]
        self.probValUTF  = [0.001 * 0.5, pVar  , 0.001 * 0.5, dVar]
        self.probValATF  = [0.003 * 0.5, pVar  , 0.038 * 0.5, dVar]

class Node11(BasicNode):

    def __init__(self, OV):
        super(Node11, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB initial Rx"
        self.destStates = [Node10, Node12, Node15, Node08, Node35]
        self.probValUT =  [0.22  , pVar  , 0.0029, 0.002 , dVar]

class Node12(BasicNode):

    def __init__(self, OV):
        super(Node12, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB Long Term Rx"
        self.destStates = [Node10, Node12, Node13, Node15 , Node08, Node35]
        self.probValUT =  [0.27  , pVar  , 0.01  , 0.00295, 0.002 , dVar]

class Node13(BasicNode):

    def __init__(self, OV):
        super(Node13, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB Long Term with Rx with Resistance"
        self.destStates = [Node10, Node13, Node16, Node08, Node35]
        self.probValUT =  [0.05  , pVar  , 0.0295, 0.004 , dVar]

class Node14(BasicNode):

    def __init__(self, OV):
        super(Node14, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis Initial Rx"
        self.isCirrhosis = True
        self.destStates = [Node10, Node15, Node08, Node35]
        self.probValUT =  [0.22  , pVar  , 0.009 , dVar]

class Node15(BasicNode):

    def __init__(self, OV):
        super(Node15, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis Long Term Rx"
        self.isCirrhosis = True
        self.destStates = [Node10, Node15, Node16, Node07, Node08, Node23, Node35]
        self.probValUT =  [0.27  , pVar  , 0.01  , 0.0071, 0.0167, 0.0239, dVar]

class Node16(BasicNode):

    def __init__(self, OV):
        super(Node16, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis Long Term Rx with resistance"
        self.isCirrhosis = True
        self.destStates = [Node10, Node16, Node07, Node08, Node23, Node35]
        self.probValUT =  [0.05  , pVar  , 0.079 , 0.018 , 0.0478, dVar]

class Node17(BasicNode):

    def __init__(self, OV):
        super(Node17, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- initial Rx"
        self.destStates = [Node10, Node18, Node20, Node08, Node35]
        self.probValUT =  [0.11  ,   pVar,  0.006, 0.002,   dVar]

class Node18(BasicNode):

    def __init__(self, OV):
        super(Node18, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- longterm Rx"
        self.destStates = [Node10, Node18, Node19,  Node21, Node08, Node35]
        self.probValUT =  [0.11  ,   pVar,   0.01, 0.00295, 0.006,   dVar]

class Node19(BasicNode):

    def __init__(self, OV):
        super(Node19, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- longterm Rx resistance"
        self.destStates = [Node10, Node19, Node21, Node08, Node35]
        self.probValUT =  [0.005 ,   pVar,  0.062, 0.002,   dVar]

class Node20(BasicNode):

    def __init__(self, OV):
        super(Node20, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis e- initial Rx"
        self.isCirrhosis = True
        self.destStates = [Node10, Node21, Node08, Node35]
        self.probValUT =  [0.11  ,   pVar, 0.015,   dVar]

class Node21(BasicNode):

    def __init__(self, OV):
        super(Node21, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis e- longterm Rx"
        self.isCirrhosis = True
        self.destStates = [Node10, Node21, Node22, Node07, Node08, Node23, Node35]
        self.probValUT =  [0.11  ,   pVar,   0.01, 0.0071, 0.0167, 0.0239,   dVar]

class Node22(BasicNode):

    def __init__(self, OV):
        super(Node22, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis e- longterm Rx with resistance"
        self.isCirrhosis = True
        self.destStates = [Node10, Node22, Node07, Node08, Node23, Node35]
        self.probValUT =  [0.005 ,   pVar,  0.079,  0.029, 0.0478,   dVar]

class Node23(BasicNode):

    def __init__(self, OV):
        super(Node23, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death HBV"
        self.destStates = [Node23]
        self.probValUT = [1]

class Node24(BasicNode):

    def __init__(self, OV):
        super(Node24, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death (Other)"
        self.destStates = [Node24]
        self.probValUT =  [1]
        self.probValAT =  [1]

class Node25(BasicNode):

    def __init__(self, OV):
        super(Node25, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg SeroclearanceNH"
        self.destStates = [Node25, Node32, Node35]
        self.probValUT =  [pVar  , 0.0   , dVar]
        self.probValAFF = [pVar  , 0.01  , dVar]

class Node26(BasicNode):

    def __init__(self, OV):
        super(Node26, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg + NH"
        self.destStates = [Node25, Node28, Node30 , Node32  , Node35, Node26]
        self.probValUT =  [0.0077, 0.0087, 0.00038, 0.001677, dVar  ,   pVar]
        self.probValAT =  [0.0107, 0.0143, 0.00049, 0.001677, dVar  ,   pVar]
        self.probValAFR = [0.0165, 0.0278, 0.00068, 0.001677, dVar  ,   pVar]
        self.probValAFF = [0.0183, 0.0202, 0.00150, 0.001677, dVar  ,   pVar]

class Node27(BasicNode):

    def __init__(self, OV):
        super(Node27, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBeAg SeroconversionNH"
        self.destStates = [Node27, Node25, Node29, Node30, Node32, Node35]
        self.probValUT =  [pVar  , 0.008 , 0.029 , 0.002 , 0     , dVar]
        self.probValAT =  [pVar  , 0.007 , 0.038 , 0.01  , 0     , dVar]
        self.probValAFR = [pVar  , 0.003 , 0.086 , 0.042 , 0     , dVar]
        self.probValAFF = [pVar  , 0.003 , 0.086 , 0.042 , 0.01  , dVar]

class Node28(BasicNode):

    def __init__(self, OV):
        super(Node28 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe+NH"
        self.destStates = [Node28, Node27, Node29, Node30, Node32, Node34, Node35]
        self.probValUTF = [pVar  , 0.09  , 0.019 , 0.001 , 0.001 , 0.0064, dVar]
        self.probValLET = [pVar  , 0.09  , 0.019 , 0.038 , 0.003 , 0.0064, dVar]
        self.probValAT =  [pVar  , 0.07  , 0.019 , 0.038 , 0.003 , 0.0064, dVar]

class Node29(BasicNode):

    def __init__(self, OV):
        super(Node29 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB e- diseaseNH"
        self.destStates = [Node29, Node26, Node30, Node32, Node34, Node35]
        self.probValUTF  = [pVar  , 0.016 , 0.001, 0.001, 0.0064, dVar]
        self.probValATF  = [pVar  , 0.016 , 0.009, 0.003, 0.0064, dVar]

class Node30(BasicNode):

    def __init__(self, OV):
        super(Node30 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis NH"
        self.isCirrhosis = True
        self.destStates = [Node30, Node31, Node32, Node34, Node35]
        self.probValUT =  [pVar  , 0.039 , 0.018  , 0.0555, dVar]

class Node31(BasicNode):

    def __init__(self, OV):
        super(Node31 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "DecompCirr NH"
        self.destStates = [Node31, Node32, Node33, Node34, Node35]
        self.probValUT =  [pVar  , 0.0710, 0.23  , 0.26, dVar]

class Node32(BasicNode):

    def __init__(self, OV):
        super(Node32 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HCC NH"
        self.destStates = [Node32, Node33, Node34, Node35]
        self.probValUT =  [pVar  , 0.06 , 0.35 , dVar]

class Node33(BasicNode):

    def __init__(self, OV):
        super(Node33 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Liver Transplantation NH"
        self.destStates = [Node33, Node34, Node35]
        self.probValUT  = [pVar  , 0.066 , dVar]

class Node34(BasicNode):

    def __init__(self, OV):
        super(Node34, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death HBV NH"
        self.destStates = [Node34]
        self.probValUT =  [1]

class Node35(BasicNode):

    def __init__(self, OV):
        super(Node35, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death Other NH"
        self.destStates = [Node35]
        self.probValUT =  [1]

class Node36(BasicNode):

    def __init__(self, OV):
        super(Node36, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg + Monitor"
        self.destStates = [Node01, Node04,   Node14,   Node08, Node35, Node36]
        self.probValUT =  [0.0077, 0.0087 , 0.00038, 0.00167 , dVar  ,  pVar ]
        self.probValAT =  [0.0107, 0.0143 , 0.00049, 0.00167 , dVar  ,  pVar ]
        self.probValAFR = [0.0165, 0.0278 , 0.00068, 0.00167 , dVar  ,  pVar ]
        self.probValAFF = [0.0183, 0.0202 , 0.00150, 0.00167 , dVar  ,  pVar ]