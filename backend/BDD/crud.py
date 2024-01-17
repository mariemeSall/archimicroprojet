from sqlalchemy.orm import Session
from . import models

def get_coordonnees(db: Session, ip):
    return db.query(models.Coordonnee).filter(models.Coordonnee.ip == ip)