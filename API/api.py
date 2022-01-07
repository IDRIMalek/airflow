
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Optional
from pydantic import BaseModel
import uvicorn
import json
import secrets

security = HTTPBasic()
app = FastAPI()
df = pd.read_csv("questions.csv")

class Question(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str]
    remark: Optional[str]

users_db = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    username = True if credentials.username in users_db else False
    password = False
    if (username):
        password = secrets.compare_digest(credentials.password, users_db[credentials.username])
    if not (username and password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def log_admin(credentials: HTTPBasicCredentials = Depends(security)):
    username = secrets.compare_digest(credentials.username, "admin")
    password = secrets.compare_digest(credentials.password, "4dm1N")
    if not (username and password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get('/')
def get_index():
    return {'data': 'hello world'}


@app.get('/status')
def get_status():
    return {
        'status': 'Ok'
    }

@app.post('/qcm/{nb_result:str}')
def generate_QCM(nb_result: int, use: Optional[str] = None, subject: Optional[str] = None,
                 username: str = Depends(get_current_username)):
    try:
        # copy mélangé
        echantillons = df.copy().sample(frac=1)
        if use:
            echantillons = echantillons.loc[(df["use"] == use)]

        if subject:
            echantillons = echantillons.loc[(df["subject"] == subject)]
        # Récupération d'un échantillon qui sera aléatoire
        if (len(sample) >= nb_result):
            echantillons = echantillons.sample(nbr_result)
        elif len(sample) > 0:
            echantillons = echantillons.sample(len(echantillons) - 1)

        # on supprime les null
        json_str = echantillons.apply(lambda x: [x.dropna()], axis=1).to_json()
        parsed = {'QCM': json.loads(json_str)}
        return JSONResponse(parsed)
    except IndexError:
        return {}

@app.get('/uses/')
def get_all_uses(username: str = Depends(get_current_username)):
    try:
        response = json.dumps(df['use'].unique().tolist())
        return {'use': json.loads(response)}
    except IndexError:
        return {}

@app.get('/subjects/')
def get_all_subjects(username: str = Depends(get_current_username)):
    try:
        response = json.dumps(df['subject'].unique().tolist())
        return {'subjects': json.loads(response)}
    except IndexError:
        return {}

@app.put('/question')
def put_question(question: Question,username: str = Depends(log_admin)):
    global df
    new_question = {
        'question': question.question,
        'subject': question.subject,
        'use': question.use,
        'correct': question.correct,
        'responseA': question.responseA,
        'responseB': question.responseB,
        'responseC': question.responseC,
        'responseD': question.responseD,
        'remark': question.remark
    }

    df=df.append(new_question, ignore_index=True)
    return new_question

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
