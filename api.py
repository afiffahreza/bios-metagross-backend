from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from knowledge import *

with open("data.json") as read_file:
    data = json.load(read_file)


class Account(BaseModel):
    id: int
    name: str
    exp: int
    balance: int


class Project(BaseModel):
    id: int
    name: str
    exp: int
    minlvl: int
    payment: int
    description: str
    jenis: str
    waktu: int
    tools: str
    prototipe: str
    requirement: int


class ProjectCreate(BaseModel):
    name: str
    description: str
    jenis: str
    waktu: int
    tools: str
    prototipe: str
    requirement: int


class Course(BaseModel):
    id: int
    name: str
    exp: int
    difficulty: int
    price: int
    description: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Tes"}


@app.get("/account")
async def read_account():
    if data['account']:
        return data['account']


@app.get("/account/{account_id}")
async def read_account_by_id(account_id: int):
    for account_data in data['account']:
        if account_data['id'] == account_id:
            return account_data
    raise HTTPException(status_code=404, detail=f'Not Found')


@app.get("/projects")
async def read_projects():
    if data['project']:
        return data['project']


@app.get("/projects/{project_id}")
async def read_project_by_id(project_id: int):
    for project_data in data['project']:
        if project_data['id'] == project_id:
            return project_data
    raise HTTPException(status_code=404, detail=f'Not Found')


@app.post("/projects")
async def create_project(project: ProjectCreate):
    id = 1

    if len(data['project']) > 0:
        id += data['project'][len(data['project'])-1]['id']
    project_dict = project.dict()

    # KBSHIT
    engine = ProjectCost()
    engine.reset(tipe=project_dict['jenis'], time=project_dict['waktu'], tech=project_dict['tools'],
                 prototipe=project_dict['prototipe'], n_req=project_dict['requirement'])
    engine.run()
    # print(EXP, MIN_LEVEL, PAYMENT)

    res = {
        "id": id,
        "name": project_dict['name'],
        "exp": engine.EXP,  # KBS
        "minlevel": engine.MIN_LEVEL,  # KBS
        "payment": engine.PAYMENT,  # KBS
        "description": project_dict['description'],
        "jenis": project_dict['jenis'],
        "waktu": project_dict['waktu'],
        "tools": project_dict['tools'],
        "prototipe": project_dict['prototipe'],
        "requirement": project_dict['requirement']
    }
    data['project'].append(dict(res))
    if res:
        read_file.close()
        with open("data.json", "w") as write_file:
            json.dump(data, write_file)
        write_file.close()
        return res
    raise HTTPException(status_code=400, detail=f'Bad request')


@app.get("/courses")
async def read_courses():
    if data['course']:
        return data['course']


@app.get("/courses/{course_id}")
async def read_course_by_id(course_id: int):
    for course_data in data['course']:
        if course_data['id'] == course_id:
            return course_data
    raise HTTPException(status_code=404, detail=f'Not Found')
