from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql://mysql_api_maps:mysql_api_maps@154.53.52.50:3307/LaRolitaDB"
#SQLALCHEMY_DATABASE_URL= "mysql+pymysql://mysql_api_maps:mysql_api_maps@154.53.52.50:3307/LaRolitaDB?allowPublicKeyRetrieval=true"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:dbmysql@localhost:3306/LaRolitaDB"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
