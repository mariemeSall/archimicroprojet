from fastapi import APIRouter
router = APIRouter()


@router.get('/test')
async def test():
    return {'Hello test'}




"""
    Retourne les adresses ip et leur couleur
"""
@router.get('/ip')
async def get_ip():
    return []