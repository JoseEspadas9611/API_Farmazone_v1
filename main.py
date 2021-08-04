from fastapi import FastAPI, Request
import json
from pydantic import BaseModel
import xmlrpc.client
import json

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
    price: float
    is_offer: bool = None


def traerProductos(db,uid,password):
    someProducts = models.execute_kw(db,uid,password,'product.template', 'search_read',
                [],{'fields': ['name','lst_price','default_code','qty_available']})
    return someProducts

datos = traerProductos(db,uid,password)

def traerPrecioCorner(db,uid,password,id):
    id2 = int(id)
    someProducts = models.execute_kw(db,uid,password,'product.pricelist.item', 'search_read',
                [])
    return someProducts

def traerImpuestos(db,uid,password):
    someProducts = models.execute_kw(db,uid,password,'account.tax', 'search_read',[])
    return someProducts

@app.get("/")
def raiz():
    #sin_codificar = json.dumps(datos)
    mensaje = "Estamos trabajando en obtener los datos"
    return mensaje

@app.get("/GetImpuestos")
def getImpuestos():
    impuestos = traerImpuestos(db,uid,password)
    return impuestos

@app.get("/GetIntegracionFarmazone")
def getIntegracionFarmazone():
    productos = []
    for i in range(len(datos)):
        precios = traerPrecioCorner(db,uid,password,datos[i]['id'])
        for j in range(len(precios)):
            if precios[j]['pricelist_id'][0] == 3:
                precio = precios[j]['price'].replace('$ ','')
                productos.append({
                    "SKU":datos[i]['default_code'],
                    "BRANCH_ID":0,
                    "STOCK":datos[i]['qty_available'],
                    "PRICE":float(precio)
                })
                break
    sin_codificar = json.dumps(datos)
    return productos

@app.put("/agregar/{item_id}")
def update_item(item_id:int, item:Item):
    return {"item_name": item.name, "item_id": item_id}

@app.delete("/eliminar")
def eliminar(request:Request):
    print('prueba')

