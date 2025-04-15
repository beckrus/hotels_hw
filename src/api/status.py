
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(prefix='', tags=['utils'])

@router.get('/')
async def app_status():
    return JSONResponse({'status': 'OK'})