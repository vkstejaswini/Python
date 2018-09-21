#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb  #Bibliotheque pour base de donnees
import serial   #Bibliotheque pour la communication serie
import time     #Bibliotheque pour le delai

try:
    ser = serial.Serial('/dev/ttyACM0', 9600,timeout=0.5)
except:
    ser = serial.Serial('/dev/ttyACM1', 9600,timeout=0.5)

time.sleep(4)   #on attend un peu, pour que l'Arduino soit prêt.

Compteur=0

'''Initialisation au demarrage'''
def RAZ():
    db = OuvertureDB()
    curs = db.cursor()

    curs.execute ("UPDATE commandes SET Etat='0',NombreDem='0',Mode='0',ComManu='0' WHERE Equipement='Lampe_infrarouge'")
    curs.execute ("UPDATE commandes SET Etat='0',NombreDem='0',Mode='0',ComManu='0' WHERE Equipement='Pompe'")
    curs.execute ("UPDATE commandes SET Etat='0',NombreDem='0',Mode='0',ComManu='0' WHERE Equipement='Servomoteur'")
    curs.execute ("UPDATE commandes SET Etat='0',NombreDem='0',Mode='0',ComManu='0' WHERE Equipement='Vanne'")
    curs.execute ("UPDATE commandes SET Etat='0',NombreDem='0',Mode='0',ComManu='0' WHERE Equipement='Ventilateur'")

    curs.execute ("UPDATE types SET Consigne='40',DeltaT='1' WHERE Type='Temperature_int'")
    curs.execute ("UPDATE types SET SeuilBas='20',SeuilHaut='60' WHERE Type='Humidite'")

    curs.execute ("TRUNCATE TABLE mesures")
    
    ser.write('CPRESET')
    
    db.commit()
    FermetureDB(db)

'''Analyse de l'arduino'''
def AnalyseArduino():
    
    MajDBMesures('TPEXT','Temperature_ext')
    MajDBMesures('TPINT','Temperature_int')
    MajDBMesures('HUMID','Humidite')
    MajDBMesures('LUMIN','Luminosite')

    ComLampePrec,ComPompePrec,ComServoPrec,ComVannePrec,ComVentiPrec,ModeLampePrec,ModePompePrec,ModeServoPrec,ModeVannePrec,ModeVentiPrec = LectureEquiDB()
    SPPompePrec,DeltaPompePrec,SeuilBasHumPrec,SeuilHautPrec = LectureTypeDB()
    
    MajDBEquip('LAMPEET','Lampe_infrarouge')
    MajDBEquip('POMPEET','Pompe')
    MajDBEquip('SERVOET','Servomoteur')
    MajDBEquip('VANNEET','Vanne')
    MajDBEquip('VENTIET','Ventilateur')

    ComLampePrec,ComPompePrec,ComServoPrec,ComVannePrec,ComVentiPrec,ModeLampePrec,ModePompePrec,ModeServoPrec,ModeVannePrec,ModeVentiPrec = LectureEquiDB()
    SPPompePrec,DeltaPompePrec,SeuilBasHumPrec,SeuilHautPrec = LectureTypeDB()

    MajCompteur('LAMPEET','Lampe_infrarouge')
    MajCompteur('POMPEET','Pompe')
    MajCompteur('SERVOET','Servomoteur')
    MajCompteur('VANNEET','Vanne')
    MajCompteur('VENTIET','Ventilateur')
        
'''Mise a jour des etats et des compteurs de chaque equipement'''
def MajDBEquip(Commande,Equip):
    db = OuvertureDB()
    curs = db.cursor()
   
    while True:
        try:
            ser.write(Commande)
            #time.sleep(0.25)
            RetCom=str(ser.readline())
            
            curs.execute("UPDATE commandes SET Etat=%s WHERE Equipement=%s",(int(RetCom),Equip))
            if Equip == 'Ventilateur' or Equip == 'Servomoteur':
                print 'Mise à jour réussie du {0}'.format(Equip)
            else:
                print 'Mise à jour réussie de {0}'.format(Equip)
            break
        except:
            if Equip == 'Ventilateur' or Equip == 'Servomoteur':
                print 'Mise à jour du {0} : échec'.format(Equip)
            else:
                print 'Mise à jour de {0} : échec'.format(Equip)
                
    db.commit()
    FermetureDB(db)

''' Mise à jour des mesures de l'arduino'''
def MajDBMesures(Commande,Mesure):
    db = OuvertureDB()
    curs = db.cursor()

    ValId=0

    if Mesure == 'Temperature_ext':
        ValId=1
    elif Mesure == 'Temperature_int':
        ValId=2
    elif Mesure == 'Luminosite':
        ValId=3
    elif Mesure == 'Humidite':
        ValId=4
        
    while True:
        try:
            while True: # ''' MODIF VINCENT'''
                ser.write(Commande)
                #time.sleep(0.25)
                RetCom2=str(ser.readline())
                if not RetCom2=="": break
                
            curs.execute ("INSERT INTO mesures(IdType,Date,Valeur) VALUES(%s,%s,%s)",(ValId,time.strftime('%y/%m/%d %H:%M:%S',time.localtime()),RetCom2))
            if ValId==4:
                print 'Enregistrement de l {0}'.format(Mesure)
                print(RetCom2)
            else:
                print 'Enregistrement de la {0}'.format(Mesure)
                print(RetCom2)
            if RetCom2!=0:
                break
        except:
            print('Erreur')

    db.commit()
    FermetureDB(db)

def MajCompteur(Commande,Equip):
    db = OuvertureDB()
    curs = db.cursor()
    
    while True:
        try:
            ser.write(Commande)
            #time.sleep(0.25)
            RetCom=int(ser.readline())
            
            curs.execute("UPDATE commandes SET NombreDem=%s WHERE Equipement=%s",(RetCom,Equip))
            if Equip == 'Ventilateur' or Equip == 'Servomoteur':
                print 'Mise à jour du compteur du {0} réussie'.format(Equip)
            else:
                print 'Mise à jour du compteur de la {0} réussie'.format(Equip)
            break
        except:
            if Equip == 'Ventilateur' or Equip == 'Servomoteur':
                print 'Mise à jour du compteur du {0} : échec'.format(Equip)
            else:
                print 'Mise à jour du compteur de la {0} : échec'.format(Equip)
    db.commit()
    FermetureDB(db)               
            
'''Fonction d'ouverture du lien avec la base de donnees'''
def OuvertureDB():
    db = MySQLdb.connect(host = "localhost",
                        user = "root",
                        passwd = "root",
                        db = "db_basilic")

    return db

'''Fonction de fermeture du lien avec la base de donnees'''
def FermetureDB(db):
    db.close

'''Fonction de lecture des commandes des equipements dans la base de donnees '''
def LectureEquiDB():
    db = OuvertureDB()

    curs = db.cursor()

    curs.execute ("SELECT * FROM commandes")

    Lecture = 0
    
    for reading in curs.fetchall():
        if Lecture == 0:       
            ComLampe = reading[4]
            ModeLampe = reading[3]
        elif Lecture == 1:
            ComPompe = reading[4]
            ModePompe = reading[3]
        elif Lecture == 2:
            ComServo = reading[4]
            ModeServo = reading[3]
        elif Lecture == 3:
            ComVanne = reading[4]
            ModeVanne = reading[3]
        elif Lecture == 4:
            ComVenti = reading[4]
            ModeVenti = reading[3]
        Lecture = Lecture + 1
    
    FermetureDB(db)

    return ComLampe,ComPompe,ComServo,ComVanne,ComVenti,ModeLampe,ModePompe,ModeServo,ModeVanne,ModeVenti

'''Detection changement d'etat d'un equipement'''

def DetectionFrontEquip(ComLampePrec,ComPompePrec,ComServoPrec,ComVannePrec,ComVentiPrec,ModeLampePrec,ModePompePrec,ModeServoPrec,ModeVannePrec,ModeVentiPrec):
    
    ComLampeActu,ComPompeActu,ComServoActu,ComVanneActu,ComVentiActu,ModeLampeActu,ModePompeActu,ModeServoActu,ModeVanneActu,ModeVentiActu = LectureEquiDB()
    ACK=""
    '''Si changement mode equipement'''
    if ModeLampePrec != ModeLampeActu:
        while True:
            try:
                ser.write('LAMPEMANU')
                time.sleep(0.25)
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print('LAMPEMANU')
        ACK=""       
    if ModePompePrec != ModePompeActu:
        while True:
            try:
                ser.write('POMPEMANU')
                time.sleep(0.25)
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print('POMPEMANU')
        ACK=""    
    if ModeServoPrec != ModeServoActu:
        while True:
            try:
                ser.write('SERVOMANU')
                time.sleep(0.25)
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print('SERVOMANU')
        ACK=""    
    if ModeVannePrec != ModeVanneActu:
        while True:
            try:
                ser.write('VANNEMANU')
                time.sleep(0.25)
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print('VANNEMANU')
        ACK=""
    if ModeVentiPrec != ModeVentiActu:
        while True:
            try:
                ser.write('VENTIMANU')
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print('VENTIMANU')
        ACK=""

    '''Si demande commande manu'''
    if ComLampePrec != ComLampeActu:
        while True:
            try:
                ser.write('LAMPEON')
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print('LAMPEON')
        ACK=""
        
    if ComPompePrec != ComPompeActu:
        while True:
            try:
                ser.write('POMPEON')
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print('POMPEON')
        ACK=""
        
    if ComServoPrec != ComServoActu:
        while True:
            try:
                ser.write('SERVOON')
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print('SERVOON')
        ACK=""
        
    if ComVannePrec != ComVanneActu:
        while True:
            try:
                ser.write('VANNEON')
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print('VANNEON')
        ACK=""
    if ComVentiPrec != ComVentiActu:
        while True:
            try:
                ser.write('VENTION')
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print('VENTION')
        ACK=""

    return ComLampeActu,ComPompeActu,ComServoActu,ComVanneActu,ComVentiActu,ModeLampeActu,ModePompeActu,ModeServoActu,ModeVanneActu,ModeVentiActu

'''Fonction de lecture des types dans la base de donnees '''
    
def LectureTypeDB():
    db = OuvertureDB()

    curs = db.cursor()

    curs.execute ("SELECT * FROM types")

    Lecture = 0
    
    for reading in curs.fetchall():
        if Lecture == 1:
            SPPompe = reading[3]
            DeltaPompe = reading[4]
        elif Lecture == 3:
            SeuilBasHum = reading[5]
            SeuilHautHum = reading[6]

        Lecture = Lecture + 1        

    FermetureDB(db)

    return SPPompe,DeltaPompe,SeuilBasHum,SeuilHautHum

'''Detection changement d'etat d'une donnee de type'''

def DetectionFrontType(SPTempPrec,DeltaTempPrec,SeuilBasHumPrec,SeuilHautPrec):

    ACK=""
    
    SPTempActu,DeltaTempActu,SeuilBasHumActu,SeuilHautActu = LectureTypeDB()

    '''Si changement donnee type'''
    
    if SPTempPrec != SPTempActu:
        while True: # ''' MODIF VINCENT'''
            try:
                ser.write("TEMMO%s#"%SPTempActu)
                time.sleep(0.25)
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print "TEMMO%s#"%SPTempActu
        ACK=""
    if DeltaTempPrec != DeltaTempActu:
        while True: # ''' MODIF VINCENT'''
            try:
                ser.write("DELTAT%s#"%DeltaTempActu)
                time.sleep(0.25)
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print "DELTAT%s#"%DeltaTempActu
        ACK=""
    if SeuilBasHumPrec != SeuilBasHumActu:
        while True: # ''' MODIF VINCENT'''
            try:
                ser.write("HUMBS%s#"%SeuilBasHumActu)
                time.sleep(0.25)
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print "HUMBS%s#"%SeuilBasHumActu
        ACK=""
    if SeuilHautPrec != SeuilHautActu:
        while True: # ''' MODIF VINCENT'''
            try:
                ser.write("HUMHT%s#"%SeuilHautActu)
                time.sleep(0.25)
                ACK=str(ser.readline())
                if not ACK=="OK": break
            except:
                ''''''
        print "HUMHT%s#"%SeuilHautActu
        ACK=""
        
    return SPTempActu,DeltaTempActu,SeuilBasHumActu,SeuilHautActu

'''Initialisation'''
print('Initialisation equipement')

RAZ()
AnalyseArduino()

ComLampePrec,ComPompePrec,ComServoPrec,ComVannePrec,ComVentiPrec,ModeLampePrec,ModePompePrec,ModeServoPrec,ModeVannePrec,ModeVentiPrec = LectureEquiDB()
SPPompePrec,DeltaPompePrec,SeuilBasHumPrec,SeuilHautPrec = LectureTypeDB()
reset=0

while True:
    if Compteur == 5:
        AnalyseArduino()
        Compteur = 0
    if time.strftime('%H:%M',time.localtime()) == "00:00" and reset==0: #modif Vincent
        ser.write('CPRESET')
        reset=1
    if  time.strftime('%H:%M',time.localtime()) == "00:01" and reset==1:   
        reset=0
        

        
    ComLampePrec,ComPompePrec,ComServoPrec,ComVannePrec,ComVentiPrec,ModeLampePrec,ModePompePrec,ModeServoPrec,ModeVannePrec,ModeVentiPrec = DetectionFrontEquip(ComLampePrec,ComPompePrec,ComServoPrec,ComVannePrec,ComVentiPrec,ModeLampePrec,ModePompePrec,ModeServoPrec,ModeVannePrec,ModeVentiPrec)
    SPPompePrec,DeltaPompePrec,SeuilBasHumPrec,SeuilHautPrec = DetectionFrontType(SPPompePrec,DeltaPompePrec,SeuilBasHumPrec,SeuilHautPrec)
    Compteur = Compteur +1
    time.sleep(1)
