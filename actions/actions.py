import datetime
from datetime import date, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import Restarted
import mysql.connector
import pymysql


class DataBase:
    def __init__(self):
        self.connection=pymysql.connect(host='172.16.1.141',
                             user='cron',
                             password='T3c4dmin1234.',
                             database='asterisk',
                             )
        self.cursor = self.connection.cursor()
        print("Conexion exitosa!")

    def select_user(self, uniqueid):
        sql = "select T0.vendor_lead_code, T0.first_name,T0.address1,T0.lead_id,T0.address2,T0.city,T0.owner,T1.list_name from vicidial_list T0 inner join vicidial_lists T1 on T0.list_id=T1.list_id where T0.lead_id = '{}'".format(uniqueid)
        
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            global monto
            global nombre
            global fechaVencimiento
            global campaña
            monto = user[4]
            nombre = user[2]
            fechaVencimiento = user[5]
            campaña = user[7]
            print("user: ", user)
            print("Rut:" , user[0])
            print("Nombre:" , user[2])
            print("Deuda monto:" , user[4])
            print("fecha Vencimiento: " , user[5])
            print("campaña: " , user[7])
            global mes
            global dia
            global anio
            global nombreMes 
            dia=int(fechaVencimiento[0:2])
            mes=int(fechaVencimiento[3:5])
            anio=int(fechaVencimiento[6:10])
            nombreMes=month_converter(mes-1)
            print("dia: ",dia)
            print("mes: ",nombreMes)
            print("año: ",anio)
              
        except Exception as e:
            raise

    def update_user(self,Razón,uniqueid):
        sql = "UPDATE bot_movatec SET tipo_contacto='4',motivo='{}',compromiso_p='4'  WHERE lead_id='{}'".format(Razón,uniqueid)
       # sql = "UPDATE usuarios SET name='{}' WHERE id = {}".format(name,id)
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise 
    def close(self):
        try:
            self.connection.close()
            print("Sesion cerrada exitosamente!")
            #agi.verbose("Database cerrada exitosamente!")
        except Exception as e:
            raise

database = DataBase()
#database.select_user(94)
#print("nombre .. :",nombre)
#print("monto .. :",monto)

"""
def variables():
     global fechaVencimiento
     global nombre
     global monto
     fechaVencimiento = "14/01/2021"
     nombre = "Ignacio"
     monto="100000"

variables()
""" 

def month_converter(i):
       month = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
       return month[i]


def ConverterDate():
     global mes
     global dia
     global anio
     global nombreMes 
     dia=int(fechaVencimiento[0:2])
     mes=int(fechaVencimiento[3:5])
     anio=int(fechaVencimiento[6:10])
     nombreMes=month_converter(mes-1)
     print("dia: ",dia)
     print("mes: ",nombreMes)
     print("año: ",anio)


#ConverterDate()



class ActionTracker(Action):

    def name(self) -> Text:
        return "action_tracker_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #database = DataBase()
        #database.select_user(94)
            #dispatcher.utter_message(text=f"Razón: {Razón}")
        return []

def llamarDB():
    database.select_user(94)

class ActionHello(Action):
    def name(self):
        return "action_hello"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        print("senderid: ", tracker.sender_id)
        llamarDB()
        t = datetime.datetime.now()
        print("hora :",t)
        if 23 >= int(t.hour) >= 12:
             dispatcher.utter_message(f'Buenas tardes, nos comunicamos por encargo de Cevsa, es usted {nombre}?')
        else:
             dispatcher.utter_message(f'Buenos días, nos comunicamos por encargo de Cevsa, es usted {nombre}?')
        return []


class ActionHello2(Action):
    def name(self):
        return "action_hello2"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(f'Me comunico con {nombre}?')
        return []

class ActionQuestion(Action):
    def name(self):
        return "action_ask_question"

    def run(self, dispatcher, tracker, domain):
       today_date = date.today()
       print("Dia de hoy : ", today_date)
       td = timedelta(3)
       {nombre},
       print(f'Dia a pagar {(today_date + td).day}')
       print(f'Mes a pagar {(today_date + td).month}')
       print(f'Año a pagar {(today_date + td).year}') 
       dispatcher.utter_message(f'Le informamos que tenemos aprobado un descuento especial por credito cedido de {campaña} que se encuentra en mora por un monto adeudado de {monto} pesos ¿Puede realizar el pago dentro de los proximos 3 días?')
       return []

###############################
######## Si paga ##############
###############################

class ActionGetFechaVcto(Action):
    def name(self):
        return "action_si_paga"

    def run(self, dispatcher, tracker, domain):
        
        dispatcher.utter_message(f"La fecha sería el {dia} de {nombreMes} del {anio}, {nombre} ¿Autoriza que uno de nuestros ejecutivos lo contacte para entregarle información de los medios de pago?")
        return []


###############################
##### Action Contactar ########
###############################

class ActionGetGoodBye(Action):
    def name(self):
        return "action_contactar"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(f'Muchas gracias, lo estará contactando uno de nuestros Ejecutivos')
        return []








#####################################
############ Action Si Conoce ##########
#####################################
 
class ActionConoce(Action):
    def name(self):
        return "action_conoce"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(f'Disculpe, usted conoce a {nombre}?')
        return []


class ActionSiConoce(Action):
    def name(self):
        return "action_si_conoce"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(f'Por encargo de Cevsa, le agradecemos que {nombre} se contacte con nosotros al Whatsapp 941111972, repito 941111972. Gracias')
        return []

######################################
###### Action Guardar Slots ##########
######################################

global conoce_o_no
class ActionGuardarConoce(Action):

    def name(self) -> Text:
        return "action_guardar_conoce_o_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conoce_o_no = tracker.get_slot("conoce_o_no")
        if tracker.get_slot("conoce_o_no") is None:
            print("Es None ..")
        print("conoce_o_no: ", conoce_o_no)
            #dispatcher.utter_message(text=f"Razón: {Razón}")
        return []


global es_o_no
class ActionRecibirEsoNo(Action):

    def name(self) -> Text:
        return "action_recibir_es_o_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        es_o_no = tracker.get_slot("es_o_no")
        print("es_o_no: ", es_o_no)
            #dispatcher.utter_message(text=f"Razón: {Razón}")
        return []

global pagará_o_no
class ActionRecibirEsoNo(Action):

    def name(self) -> Text:
        return "action_recibir_paga_o_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        pagará_o_no = tracker.get_slot("pagará_o_no")
        print("pagará_o_no: ", pagará_o_no)
            #dispatcher.utter_message(text=f"Razón: {Razón}")
        return []

global autoriza_o_no
class ActionRecibirEsoNo(Action):

    def name(self) -> Text:
        return "action_autoriza_o_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        autoriza_o_no = tracker.get_slot("autoriza_o_no")
        print("autoriza_o_no: ", autoriza_o_no)
            #dispatcher.utter_message(text=f"Razón: {Razón}")
        return []

####################
###### Restart #####
####################

class ActionRestart2(Action):
    """Resets the tracker to its initial state.
    Utters the restart template if available."""

    def name(self) -> Text:
        return "action_restart2"

    async def run(self, dispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [Restarted()]

####################
###### Final #######
####################
class Final(Action):
    def name(self):   
        return "action_final"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #database.close()
        print("|")
        dispatcher.utter_message(f'|')
        return []


###############################
####### Preguntas Usuario #####
###############################

class ActionConoce(Action):
    def name(self):
        return "action_quien"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(f'hablo con {nombre}?')
        return []

class ActionDonde(Action):
    def name(self):
        return "action_donde"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(f'Nos estamos comunicando por encargo de Cevsa')
        return []

class ActionDonde2(Action):
    def name(self):
        return "action_donde2"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(f'Estamos llamando por encargo de Cevsa, podrá pagar dentro de los 3 proximos días?')
        return []

class ActionMonto(Action):
    def name(self):
        return "action_monto"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(f'El monto adeudado es de {monto} pesos, podrá pagar dentro de los 3 proximos días?')
        return []

class FechaVencimiento(Action):
    def name(self):
        return "action_fecha"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(f'la fecha es el {dia} de {nombreMes} del {anio}, podrá pagar dentro de los 3 proximos días?')
        return []

####################
##### Dar Hora #####
####################
class ActionDarHora(Action):
    def name(self):   
        return "action_dar_hora"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"Son las {dt.datetime.now()}")

        return []
###########################
#### Questions 2 y 3 ######
###########################
class ActionQuestion2(Action):
    def name(self):
        return "action_ask_question2"

    def run(self, dispatcher, tracker, domain):
     
       dispatcher.utter_message(f'Disculpe le haré la pregunta nuevamente')
       return []

class ActionQuestion3(Action):
    def name(self):
        return "action_ask_question3"

    def run(self, dispatcher, tracker, domain):
       dispatcher.utter_message(f'Disculpe comencemos desde el principio')
       return []

###########################
######## Sin uso ##########
###########################
class ActionReceivePersona(Action):

    def name(self) -> Text:
        return "action_unique_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message['text']
        print(f'uniqueid en action: {text}')
        #dispatcher.utter_message(text=f"Es o no es {text}!")
        
        return []  #devolvemos a slot un string con valor



