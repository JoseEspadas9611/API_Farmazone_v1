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

@app.get("/")
def raiz():
    #sin_codificar = json.dumps(datos)
    mensaje = "Estamos trabajando en obtener los datos"
    return mensaje

@app.get("/GetImpuestos")
def getImpuestos():
    impuestos = someProducts(db,uid,password)
    return impuestos

@app.get("/pruebaAPI")
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

@app.delete("/eliminar")
def eliminar(request:Request):
    print('prueba')

