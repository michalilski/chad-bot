import sqlalchemy
from sqlalchemy.orm import sessionmaker

from app.core.db.models import Base

db_engine = sqlalchemy.create_engine("mysql+pymysql://root:chadboys@chadbot-db:3306/cinema")
Base.metadata.create_all(db_engine)

Session = sessionmaker()
Session.configure(bind=db_engine)
db_session = Session()
