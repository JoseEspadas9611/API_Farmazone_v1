from fastapi import FastAPI, Request
import json
from fastapi.params import Path
from pydantic import BaseModel
import xmlrpc.client
import json
import certifi
import pymongo
import random
from datetime import datetime

url = 'https://admindagsa-odoo-agsa.odoo.com'
db = 'admindagsa-odoo-agsa-prod-2509291'
username = 'joseem@dagsasc.com'
password = 'Gallo196'
common =xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models =xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
version = common.version()
uid = common.authenticate(db,username,password,{})

app = FastAPI()
""" Api para generar el JSON de Corner y Rappi para limentarlos desde Odoo"""

class Item(BaseModel):
    name: str
    message: str = None
    stock: int

class Historial(BaseModel):
    year: int
    month: str
    state: str
class DetalleHistorial(BaseModel):
    folio: str

class Images(BaseModel):
    base64: list = []
    folio: str = None

def someProducts(db,uid,password):
    someProducts = models.execute_kw(db,uid,password,'stock.quant', 'search_read',
                [[['company_id', '=', 2]]],{'fields': ['product_id','available_quantity']})
    return someProducts

def traerProductos(db,uid,password):
    someProducts = models.execute_kw(db,uid,password,'product.template', 'search_read',
                [],{'fields': ['name','lst_price','default_code','qty_available']})
    return someProducts

def traerPrecioCorner(db,uid,password):
    #id2 = int(id)
    someProducts = models.execute_kw(db,uid,password,'product.pricelist.item', 'search_read',
                [[['pricelist_id', '=', 3]]],{'fields': ['pricelist_id','product_tmpl_id','price']})
    return someProducts

def traerImpuestos(db,uid,password):
    someProducts = models.execute_kw(db,uid,password,'account.tax', 'search_read',[])
    return someProducts

def searchHistorial(estate, year, month):
    fecha_inicio = ""
    fecha_fin = ""
    ca = certifi.where()
    client = pymongo.MongoClient(f"mongodb+srv://desarrollo:yatelasa123@cluster0.hziaa.mongodb.net/test?authSource=admin&replicaSet=atlas-8o2ch6-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true",tlsCAFILE=ca)
    db = client.get_database('PREVIVALE')
    if month == 'enero':
        mes = '01'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"31"+" 00:00:00"
    elif month == 'febrero':
        mes = '02'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"28"+" 00:00:00"
    elif month == 'marzo':
        mes = '03'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"31"+" 00:00:00"
    elif month == 'abril':
        mes = '04'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"30"+" 00:00:00"
    elif month == 'mayo':
        mes = '05'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"31"+" 00:00:00"
    elif month == 'junio':
        mes = '06'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"30"+" 00:00:00"
    elif month == 'julio':
        mes = '07'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"31"+" 00:00:00"
    elif month == 'agosto':
        mes = '08'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"31"+" 00:00:00"
    elif month == 'septiembre':
        mes = '09'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"30"+" 00:00:00"
    elif month == 'octubre':
        mes = '10'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"31"+" 00:00:00"
    elif month == 'noviembre':
        mes = '11'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"30"+" 00:00:00"
    elif month == 'diciembre':
        mes = '12'
        fecha_inicio =str(year)+"-"+mes+"-"+"01"+" 00:00:00"
        fecha_fin = str(year)+"-"+mes+"-"+"31"+" 00:00:00"
        
    fecha_dt_inicio = datetime.strptime(fecha_inicio,'%Y-%m-%d %H:%M:%S')
    fecha_dt_fin = datetime.strptime(fecha_fin,'%Y-%m-%d %H:%M:%S')

    if estate == "Todos":
        consulta = {
            "load_date" : {"$gte" : fecha_dt_inicio, "$lte" : fecha_dt_fin}
            }
    else:
        consulta = {
        "state": estate,
        "load_date" : {"$gte" : fecha_dt_inicio, "$lte" : fecha_dt_fin}
        }
    claves = db.historial.find(consulta,{'_id': 0})
    # claves = db.claves.find({})
    return list(claves)

def insertImage(imagen, folio):
    ca = certifi.where()
    client = pymongo.MongoClient(f"mongodb+srv://desarrollo:yatelasa123@cluster0.hziaa.mongodb.net/test?authSource=admin&replicaSet=atlas-8o2ch6-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true",tlsCAFILE=ca)
    db = client.get_database('PREVIVALE')
    claves = db.historial.insert_one({"imagen":imagen,"folio":folio})
    # claves = db.claves.find({})
    return claves

@app.get("-")
def raiz():
    #sin_codificar = json.dumps(datos)
    mensaje = "Estamos trabajando en obtener los datos"
    return mensaje

@app.get("/GetImpuestos")
def getImpuestos():
    impuestos = someProducts(db,uid,password)
    return impuestos

@app.get("/api/pruebaAPI/Mensaje")
def getImpuestos():
    mensaje = "Datos que pudimos Rescatar:..... HOLI CRAYOLI"
    value = {
         "data":mensaje
    }
    return json.dumps(value)

@app.get("/GetIntegracionFarmazone")
def getIntegracionFarmazone():
    productos = []
    datos = someProducts(db,uid,password)
    #print(datos[0])
    preciosCorner = traerPrecioCorner(db,uid,password)
    #print(preciosCorner[0])
    find_sku = lambda Object_response: Object_response['product_id'][1].split(' ')[0][1:-1]
    for i in range(len(datos)):
        field = {'product_id': datos[i]['product_id']}
        sku = find_sku(field)
        for j in range(len(preciosCorner)):
            if datos[i]['product_id'][0] == preciosCorner[j]['product_tmpl_id'][0]:
                precio = preciosCorner[j]['price'].replace('$ ','')
                productos.append({
                     "SKU":sku,
                     "BRANCH_ID":0,
                     "STOCK":datos[i]['available_quantity'],
                     "PRICE":float(precio)
                })
                break
    print(len(productos))
    return productos

@app.put("/agregar/{item_id}")
def update_item(item_id:int, item:Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/api/pruebaAPI/EnviarMensaje")
async def update_item(item:Item):
    value = {"name": item.name, 
            "message": item.message,
            "stock": item.stock}
    return item

@app.post("/api/pruebaAPI/BuscarHistorial")
async def get_historial(historial:Historial):
    print("Datos de Julio",historial)
    result = searchHistorial(historial.state,historial.year,historial.month)
    result_format = {"data":result}
    return result_format

@app.post("/api/pruebaAPI/DetalleHistorial")
async def get_historial(detalle:DetalleHistorial):
    result_format = {"data":[{
        "fecha_solicitud":"04/06/2021",
        "folio":"002510",
        "Estado":"Revisado",
        "tipo_consumo":"Alimentos",
        "fecha_captura":"05/06/21",
        "no_ticket":"542140",
        "fecha_y_hora_emision":"04/06/2021 20:54",
        "fecha_solicitud_factura":"06/06/21",
        "rfc_emisor":"DVI800013ICQ6",
        "emisor":"Operadora Vips S de RL de CV",
        "importe_total":"1256.50",
    }]}
    return result_format

@app.post("/api/pruebaAPI/insertarImagen")
async def get_historial(imagenes:Images):
    imagenes.folio = random.randint(0,999999)
    insert = insertImage(imagenes.base64,imagenes.folio)
    print(insert)
    return "intento insertar Jejetl"


@app.delete("/eliminar")
def eliminar(request:Request):
    print('prueba')

