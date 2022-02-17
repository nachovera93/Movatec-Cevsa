import datetime
from datetime import date, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.events import Restarted
import mysql.connector
import pymysql
global SiPaga
global NoPaga
global razon
global tipo_contacto
global compromiso_p
global derivacion
global fecha_com
global entrega_info
SiPaga=None
NoPaga=None
razon=None
tipo_contacto=None
compromiso_p=None
derivacion=None
fecha_com=None
entrega_info=None
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
        sql = "select T0.vendor_lead_code, T0.first_name,T0.address1,T0.lead_id,T0.address2,T0.city,T0.owner,T1.list_name,T0.email,T2.campaign_name from vicidial_list T0 inner join vicidial_lists T1 on T0.list_id=T1.list_id inner join vicidial_campaigns T2 on T1.campaign_id=T2.campaign_id where T0.lead_id = '{}'".format(uniqueid)
        
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            global monto
            global nombre
            global fechaVencimiento
            global Campania
            global oferta
            global primernombre
            primernombre = user[1]
            monto = user[4]
            nombre = user[2]
            fechaVencimiento = "01/01/2022"
            Campania = user[9]
            oferta = user[8]
            print("user: ", user)
            print("Nombre:" , nombre)
            print("Deuda monto:" , monto)
            print("Campaña: " , Campania)
            print("oferta: " , oferta)
            """
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
            """
              
        except Exception as e:
            raise
    def tipo_contacto(self,uniqueid):
        sql = "SELECT tipo_contacto, max(fecha_llamada) from bot_movatec where lead_id='{}'".format(uniqueid)
       # sql = "UPDATE usuarios SET name='{}' WHERE id = {}".format(name,id)
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            global tipo_contact
            tipo_contact = user[0]
          
        except Exception as e:
            raise 
    def update_user(self,tipo_contacto,razon,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid):
        sql = "UPDATE bot_movatec SET tipo_contacto='{}',motivo='{}',compromiso_p='{}',derivacion='{}',fecha_com='{}',entrega_info='{}' WHERE lead_id='{}'".format(tipo_contacto,razon,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid)
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
       return month[i-1]


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



def llamarDB(uniqueid):
    database.select_user(uniqueid)

def progreso(tipo_contacto,razon,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid):
    database.update_user(tipo_contacto,razon,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid)

def TipoContacto(uniqueid):
    database.tipo_contacto(uniqueid)

class ActionHello(Action):
    def name(self):
        return "action_hello"

    def run(self, dispatcher, tracker, domain):
        
        global uniqueid
        uniqueid = tracker.sender_id
        TipoContacto(uniqueid)
        dispatcher.utter_message(f'tipo de contacto 1: {tipo_contact}')
        #uniqueid = 565408        
        llamarDB(uniqueid)
        t = datetime.datetime.now()
        print("hora :",t)
        if 23 >= int(t.hour) >= 12:
             dispatcher.utter_message(f'Buenas tardes, nos comunicamos por encargo de Cevsa, es usted {nombre}?')
        else:
             dispatcher.utter_message(f'Buenos días, nos comunicamos por encargo de Cevsa, es usted {nombre}?') 
        progreso(7,razon,compromiso_p,derivacion,fecha_com,"No",uniqueid)
        TipoContacto(uniqueid)
        dispatcher.utter_message(f'tipo de contacto 2: {tipo_contact}')
        return []
        
           


class ActionHello2(Action):
    def name(self):
        return "action_hello2"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        #uniqueid = 565408
        print("uniqueid: ", tracker.sender_id)
        llamarDB(uniqueid)
        progreso(7,razon,compromiso_p,derivacion,fecha_com,"No",uniqueid)
        dispatcher.utter_message(f'Me comunico con {primernombre}?')
        return []


###########################################################
################### Pregunta Principal ####################
###########################################################

class ActionQuestion(Action):
    def name(self):
        return "action_ask_question"

    def run(self, dispatcher, tracker, domain):
     
        global uniqueid
        uniqueid = tracker.sender_id
        TipoContacto(uniqueid)
        progreso(1,razon,compromiso_p,derivacion,fecha_com,"No",uniqueid)
        llamarDB(uniqueid)
        dispatcher.utter_message(f'Le informamos que tenemos aprobado un descuento especial por credito cedido de {Campania} que se encuentra en mora por un monto adeudado de {monto} pesos, quedando a pagar tan solo {oferta} pesos. ¿Puede realizar el pago dentro de los proximos 3 días?') 
        progreso(2,razon,compromiso_p,derivacion,fecha_com,"Si",uniqueid)
           
        return []
       
################################################
################### Si paga ####################
################################################

class ActionSiPaga(Action):
    def name(self):
        return "action_si_paga"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        llamarDB(uniqueid)
        today_date = date.today()
        print("Dia de hoy : ", today_date)
        td = timedelta(3)
        global fechaPago
        fechaPago=(today_date + td)
        print("Fecha de Pago: ",fechaPago)
        dia = (today_date + td).day
        mes = (today_date + td).month
        anio = (today_date + td).year
        nombreMes=month_converter(mes)
        print(f'Dia a pagar {(today_date + td).day}')
        print(f'Mes a pagar {(today_date + td).month}')
        print(f'Año a pagar {(today_date + td).year}') 
        dispatcher.utter_message(f"La fecha sería el {dia} de {nombreMes} del {anio}. {primernombre}, ¿Autoriza que uno de nuestros ejecutivos lo contacte para entregarle información de los medios de pago?")
        progreso(3,razon,3,derivacion,fechaPago,"Si",uniqueid) 
        return []


################################################
################### No paga ####################
################################################

class ActionNoPaga(Action):
    def name(self):
        return "action_no_paga"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        progreso(4,razon,4,derivacion,fecha_com,"Si",uniqueid)
        llamarDB(uniqueid)
        dispatcher.utter_message(f"¿Desea que uno de nuestros ejecutivos se contacte con usted para poder entregarle otras alternativas?")
        return []


################################################
################# Action Contactar #############
################################################

class ActionContact(Action):
    def name(self):
        return "action_contactar"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        llamarDB(uniqueid)
        dispatcher.utter_message(f'Muchas gracias, lo estará contactando uno de nuestros Ejecutivos | EXIT')
        if(SiPaga==1):
            progreso(3,razon,3,"Si",fechaPago,"Si",uniqueid)
        elif(SiPaga==0):
            progreso(4,razon,None,"Si",fecha_com,"Si",uniqueid)
        else:
            print("Nada")
        return []


################################################
################# Action Despedida #############
################################################

class ActionGetGoodBye(Action):
    def name(self):
        return "action_despedida"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        llamarDB(uniqueid)
        dispatcher.utter_message(f'Muchas gracias por su tiempo, que tenga un buen día | EXIT')
        if (SiPaga==1):
            progreso(3,razon,3,"No",fechaPago,"Si",uniqueid)
        elif (SiPaga==0):
            progreso(4,razon,4,"No",fecha_com,"Si",uniqueid)
        else:
            print("Nada")
        return []




#####################################
############ Action Si Conoce ##########
#####################################
 
class ActionConoce0(Action):
    def name(self):
        return "action_conoce"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        llamarDB(uniqueid)
        dispatcher.utter_message(f'Disculpe, usted conoce a {nombre}?')
        progreso(5,razon,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid)
        return []


class ActionSiConoce(Action):
    def name(self):
        return "action_si_conoce"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        llamarDB(uniqueid)
        dispatcher.utter_message(f'Por encargo de Cevsa, le agradecemos que {primernombre} se contacte con nosotros al Whatsapp 941111972, repito 941111972. Gracias | EXIT')
        progreso(6,razon,compromiso_p,derivacion,fecha_com,"Si",uniqueid)
        return []


###############################################
################### Restart ###################
###############################################

class ActionRestart2(Action):
    """Resets the tracker to its initial state.
    Utters the restart template if available."""

    def name(self) -> Text:
        return "action_restart2"

    async def run(self, dispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [Restarted()]

##########################
########## Final #########
##########################
class Final(Action):
    def name(self):   
        return "action_final"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Exit")
        return []


###############################
####### Preguntas Usuario #####
###############################

class ActionConoce(Action):
    def name(self):
        return "action_quien"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        llamarDB(uniqueid)
        dispatcher.utter_message(f'{nombre}?')
        return []

class ActionDonde(Action):
    def name(self):
        return "action_donde"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        llamarDB(uniqueid)
        dispatcher.utter_message(f'Nos estamos comunicando por encargo de Cevsa')
        return []

class ActionDonde2(Action):
    def name(self):
        return "action_donde2"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        llamarDB(uniqueid)
        dispatcher.utter_message(f'Estamos llamando por encargo de Cevsa, podrá pagar dentro de los 3 proximos días?')
        return []

class ActionMonto(Action):
    def name(self):
        return "action_monto"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        #progreso(2,razon,compromiso_p,derivacion,fecha_com,"Si",uniqueid)
        llamarDB(uniqueid)
        dispatcher.utter_message(f'El monto adeudado es de {monto} pesos, con oferta de {oferta} podrá pagar dentro de los 3 proximos días?')
        return []

class FechaVencimiento(Action):
    def name(self):
        return "action_fecha"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        llamarDB(uniqueid)
        dispatcher.utter_message(f'Sería dentro de los 3 proximos días, podría cancelar?')
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
class ActionRecibirPagaoNo(Action):

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
class ActionRecibirAutorizaoNo(Action):

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




class ResetSlotss(Action):

    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        print("uniqueid: ", tracker.sender_id)
        llamarDB(uniqueid)
        t = datetime.datetime.now()
        print("hora :",t)
        if 23 >= int(t.hour) >= 12:
             dispatcher.utter_message(f'Buenas tardes, nos comunicamos por encargo de Cevsa, es usted {nombre}?')
        else:
             dispatcher.utter_message(f'Buenos días, nos comunicamos por encargo de Cevsa, es usted {nombre}?')
        progreso(7,razon,compromiso_p,derivacion,fecha_com,"No",uniqueid)
        print("es_o_no: ", None)
        print("conoce_o_no: ", None)
        print("pagará_o_no: ", None)
        print("Razón: ", None)
        return [SlotSet("es_o_no", None),SlotSet("conoce_o_no", None),SlotSet("pagará_o_no", None),SlotSet("Razón", None)]

