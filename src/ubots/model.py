from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class TipoAtendimento(StrEnum):
    CARTOES = "CARTOES"
    EMPRESTIMOS = "EMPRESTIMOS"
    OUTROS = "OUTROS"


class AtendimentoRequest(BaseModel):
    cliente: str
    mensagem: str
    assunto: TipoAtendimento


@dataclass
class Atendimento:
    id: UUID
    cliente: str
    mensagem: str
    assunto: TipoAtendimento
