import os
os.environ['DATABASE_URL']='postgresql://grin:qwer1234t5@localhost/api_personal_area'
print(os.environ['DATABASE_URL'])
from .db import Base, engine
Base.metadata.create_all(bind=engine)