from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine('postgresql://nawal:handeercel@localhost/database_1')
db = scoped_session(sessionmaker(bind=engine))