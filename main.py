
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tinydb import TinyDB, Query
import re

app = FastAPI()
db = TinyDB('db.json')

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/create_data")
def create_data():
    table = db.table('Forms')
    table.insert({'form_name': 'Contact', 'user_name':'text', 'user_surname':'text', 'user_email':'email', 'user_phone':'phone'})
    table.insert({'form_name': 'Request a call', 'user_name':'text', 'user_phone':'phone'})
    table.insert({'form_name': 'Request Consultation', 'user_name':'text', 'user_phone':'phone', 'comment':'text'})
    table.insert({'form_name': 'Subscription', 'user_email':'email'})
    table.insert({'form_name': 'Lead', 'lead_email':'email', 'lead_date': 'date'})
    table.insert({'form_name': 'Order', 'user_name':'text', 'user_email':'email', 'order_date': 'date', 'order':'text'})
    table.insert({'form_name': 'Availability', 'user_name':'text', 'user_email':'email', 'availability_date': 'date'})
    table.all()

@app.get("/get_form")
def read_item(request: Request):
    params = request.query_params
    form = db.table('Forms')
    tmp_form = {k: validation(v) for k, v in params.items()}
    print(params)
    res = form.search(Query().fragment(tmp_form))
    if res:
        for f in res:
            if len(tmp_form) == (len(f)-1):
                return str(f['form_name'] + " Form")

        return str(res[0]['form_name'] + " Form")

    tmp_dic = {"form_name": "Unknown"}
    tmp_dic.update(tmp_form)
    form.insert(tmp_dic)
    return tmp_form

@app.post("/get_form")
def read_item(request: Request):
    params = request.query_params
    form = db.table('Forms')
    tmp_form = {k: validation(v) for k, v in params.items()}
    print(params)
    res = form.search(Query().fragment(tmp_form))
    if res:
        for f in res:
            if len(tmp_form) == (len(f)-1):
                return str(f['form_name'] + " Form")

        return str(res[0]['form_name'] + " Form")

    tmp_dic = {"form_name": "Unknown"}
    tmp_dic.update(tmp_form)
    form.insert(tmp_dic)
    return tmp_form

@app.get("/get_form_browser", response_class=HTMLResponse)
def read_item(request: Request):
    params = request.query_params
    form = db.table('Forms')
    tmp_form = {k: validation(v) for k, v in params.items()}
    res = form.search(Query().fragment(tmp_form))
    if res:
        for f in res:
            tmp = [i for i in f]
            print(f)
            if len(tmp_form) == (len(f)-1):
                return templates.TemplateResponse("contact_form.html", {"request": request, "form": f['form_name'], "fields": tmp[1:]})

        tmp = [i for i in res[0]]
        return templates.TemplateResponse("contact_form.html", {"request": request, "form": res[0]["form_name"], "fields": tmp[1:]})

    tmp_dic = {"form_name": "Unknown"}
    tmp_dic.update(tmp_form)
    form.insert(tmp_dic)
    tmp = [k for k in tmp_dic]
    return templates.TemplateResponse("contact_form.html", {"request": request, "form": "Unknown", "fields": tmp[1:]})

def validation(s):
    if re.match(r"^[\d]{2}[\.][\d]{2}[\.][\d]{4}", s) or re.match(r"^[\d]{2}[\-][\d]{2}[\-][\d]{2}", s):
        return "date" 
    elif re.match(r"\s?[\d]\s[\d]{3}\s[\d]{3}\s[\d]{2}\s[\d]{2}", s) or re.match(r"\s?[\d][\d]{3}[\d]{3}[\d]{2}[\d]{2}", s):
        return "phone"
    elif re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", s):
        return "email"
    else:
        return "text"