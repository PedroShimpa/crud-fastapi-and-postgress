from core.configs import settings

from sqlalchemy import Column, Integer, String

class ClienteModel(settings.DBBaseModel):
    __tablename__ = 'clientes'

    id: int =Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(190))
    email: str=  Column(String(190))
