import asyncio
import json
from dataclasses import asdict
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, HTTPException, Request, status

from ubots import model
from ubots.auth_bearer import BearerToken

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.queues = {
        model.TipoAtendimento.CARTOES: [],
        model.TipoAtendimento.EMPRESTIMOS: [],
        model.TipoAtendimento.OUTROS: [],
    }
    app.state.times = {
        model.TipoAtendimento.CARTOES: dict(),
        model.TipoAtendimento.EMPRESTIMOS: dict(),
        model.TipoAtendimento.OUTROS: dict(),
    }
    app.state.atendentes = dict()


@app.post("/api/login/{time}")
async def __login(time: model.TipoAtendimento, request: Request):
    atendente_id = uuid4()
    request.app.state.times[time][str(atendente_id)] = dict()
    request.app.state.atendentes[str(atendente_id)] = time
    return atendente_id


@app.post("/api/atendimento")
async def __atendimento(payload: model.AtendimentoRequest, request: Request):
    atendimento = model.Atendimento(
        id=uuid4(),
        cliente=payload.cliente,
        mensagem=payload.mensagem,
        assunto=payload.assunto,
    )
    app.state.queues[payload.assunto].append(atendimento)
    return asdict(atendimento)


@app.post("/api/atender")
async def __atender(request: Request, atendente_id=Depends(BearerToken())):
    if str(atendente_id) not in request.app.state.atendentes:
        raise HTTPException(status_code=401)
    time = request.app.state.atendentes[str(atendente_id)]
    if len(request.app.state.queues[time]) == 0:
        raise HTTPException(status_code=400, detail="Fila vazia.")
    if len(request.app.state.times[time][str(atendente_id)]) >= 3:
        raise HTTPException(status_code=400, detail="Máximo de atendimentos atingidos.")
    atendimento = request.app.state.queues[time].pop(0)
    request.app.state.times[time][str(atendente_id)][atendimento.id] = atendimento
    return asdict(atendimento)


@app.post("/api/finalizar/{id}")
async def __finalizar(id: UUID, request: Request, atendente_id=Depends(BearerToken())):
    if str(atendente_id) not in request.app.state.atendentes:
        raise HTTPException(status_code=401)
    time = request.app.state.atendentes[str(atendente_id)]
    if id not in request.app.state.times[time][str(atendente_id)]:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado.")
    atendimento = request.app.state.times[time][str(atendente_id)][id]
    del request.app.state.times[time][str(atendente_id)][id]
    return asdict(atendimento)


@app.get("/api/atendendo")
async def __atender(request: Request, atendente_id=Depends(BearerToken())):
    if str(atendente_id) not in request.app.state.atendentes:
        raise HTTPException(status_code=401)
    time = request.app.state.atendentes[str(atendente_id)]
    return request.app.state.times[time][str(atendente_id)]
