from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import DB_URL

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    alert_type = Column(String)
    message = Column(String)
    severity = Column(String)

def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def save_alert(t, m, s):
    db = Session()
    db.add(Alert(alert_type=t, message=m, severity=s))
    db.commit()
    db.close()