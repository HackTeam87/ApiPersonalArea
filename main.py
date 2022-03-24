from db.models import Client, Agent, Agent_Subscription, Subscription
from db.db import database, SessionLocal

from typing import List
from fastapi import FastAPI, Request
from fastapi import Form
from fastapi.responses import UJSONResponse
import uvicorn




db = SessionLocal()
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



#/api/v1/wca/validate   

@app.get("/api/v1/wca/validate/{uuid}", response_class=UJSONResponse)
async def api_agent_uuid(uuid: str, request: Request):
    #IP с которого пришел запрос
    client_ip = request.client.host

    #Форматирует запрос 
    query = f'''
    SELECT a.id,
       a.client_id,
       a.created_at,
       a.uuid,
       a.ip_address,
       coalesce(subscriptions, 0) active_subscriptions
FROM agents a
         LEFT JOIN (
    SELECT count(*) subscriptions, asu.agent_id
    FROM agent_subscriptions asu
             JOIN subscriptions s on asu.subscription_id = s.id
    WHERE asu.expired_at > now()
    GROUP BY agent_id
) sbsrc on sbsrc.agent_id = a.id
WHERE uuid = '{uuid}';'''

    #Делаем выборку с БД
    rdb = await database.fetch_all(query)



    #Валидация
    if rdb == []:
        return {
   "data": "UUID_NOT_VALID",
   "error": None
       }
        
    
    if rdb[0]['ip_address'] == None:
        return {
   "data": "MUST_REGISTER",
   "error": None
       }
         

    if rdb[0]['ip_address'] != None and rdb[0]['ip_address'] != client_ip :
        return {
   "data": "IP_NOT_VALID",
   "error": None
       }
       

    if rdb[0]['active_subscriptions']  == False:
        return {
   "data": "NO_ACTIVE_SUBSCRIPTION",
   "error": None
       }   

    else:
        return {
   "data": "REGISTERED",
   "error": None
       } 
       
#/api/v1/wca/status

@app.get("/api/v1/wca/status/{uuid}")
async def api_agent_status(uuid: str, request: Request):
    #IP с которого пришел запрос
    client_ip = request.client.host

    #Форматирует запрос 
    query = f'''
    SELECT uuid,
       created_at activated_at,
       ip_address registered_ip,
       updated_at registered_at,
       concat(
               (SELECT "value" FROM configuration WHERE name = 'release_server_url'),
               '/',
               (SELECT version FROM releases ORDER BY id desc LIMIT 1),
               '/agent.tar.gz'
           ) load_url
FROM agents a
WHERE uuid = '{uuid}' and a.ip_address = '{client_ip}';'''

    #Делаем выборку с БД
    rdb = await database.fetch_one(query)

    if rdb == []:
        pass
    if rdb != []:
        return {
        "data": {
      "agent": '<Agent | null>',
      "ip_address": client_ip,
      "uuid": uuid,
      "status": "ACTIVATED"
   } ,"error": None
   }



    

@app.get("/clients/list")
async def clients_list():
    # query = '''SELECT * FROM clients'''
    # rdb = await database.fetch_all(query)
    res = db.query(Client).all()
    return res

@app.post("/api/v1/wca/client/add")
async def client(
    name: str = Form(...), company: str = Form(...), 
    email: str = Form(...), phone: str = Form(...), 
    password: str = Form(...), balance: str = Form(...)):

    res = Client(name=name, company=company, email=email,
                 phone=phone, password=password, balance=balance)
    db.add(res) 
    db.commit()            
    return {"name": name}   

@app.get("/ip")
def get_client_ip(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}     






if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

