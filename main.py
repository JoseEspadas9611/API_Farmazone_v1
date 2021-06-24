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
#datos = [{"id": 1 ,"lenguaje":"Python"}, 
#        {"id": 2,"lenguaje":"Java"}, 
#        {"id": 3,"lenguaje":"PHP"},
#        {"id": 4,"lenguaje":"Angular"}, 
#        {"id": 5,"lenguaje":"C#"}]

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


def someProducts(db,uid,password):
    someProducts = models.execute_kw(db,uid,password,'product.product', 'search_read',
                [],{'fields': ['name','lst_price','default_code']})
    return someProducts

@app.get("/")
def raiz():
    #sin_codificar = json.dumps(datos)
    mensaje = "Estamos trabajando en obtener los datos"
    return mensaje


@app.get("/traerDatos")
def traerDatos():
    datos = someProducts(db,uid,password)
    print(len(datos))
    sin_codificar = json.dumps(datos)
    return datos

@app.put("/agregar/{item_id}")
def update_item(item_id:int, item:Item):
    return {"item_name": item.name, "item_id": item_id}

@app.delete("/eliminar")
def eliminar(request:Request):
    print('prueba')