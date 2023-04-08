from typing import List


from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.cliente_model import ClienteModel
from schemas.cliente_schema import ClienteSchema
from core.deps import get_session

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ClienteSchema)
async def post_cliente(cliente: ClienteSchema, db: AsyncSession = Depends(get_session)):
    novo_cliente = ClienteModel(nome=cliente.nome, email=cliente.email)
    db.add(novo_cliente)
    await db.commit()
    return novo_cliente


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ClienteSchema])
async def get_clientes(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ClienteModel)
        result = await session.execute(query)
        clientes: List[ClienteModel] = result.scalars().all()
        return clientes


@router.get('/{cliente_id}', status_code=status.HTTP_200_OK, response_model=ClienteSchema)
async def get_cliente(cliente_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ClienteModel).filter(ClienteModel.id == cliente_id)
        result = await session.execute(query)
        cliente = result.scalar_one_or_none()
        if cliente:
            return cliente
        else:
            raise HTTPException(detail='Cliente não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{cliente_id}', status_code=status.HTTP_202_ACCEPTED, response_model=ClienteSchema)
async def update_cliente(cliente_id: int, cliente: ClienteSchema,  db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ClienteModel).filter(ClienteModel.id == cliente_id)
        result = await session.execute(query)
        cliente_up = result.scalar_one_or_none()
        if cliente_up:
            cliente_up.nome = cliente.nome
            cliente_up.email = cliente.email
            await session.commit()
            return cliente_up
        else:
            raise HTTPException(detail='Cliente não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{cliente_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(cliente_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ClienteModel).filter(ClienteModel.id == cliente_id)
        result = await session.execute(query)
        cliente_del = result.scalar_one_or_none()
        if cliente_del:

            await session.delete(cliente_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Cliente não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
