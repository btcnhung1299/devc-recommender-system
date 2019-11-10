from sqlalchemy import exc
from database import db

def save_to_db(record):
   """Insert a record into database by adding it to the session, or transaction
   and commit the session.
   
   Args:
      record: an instance of mapped class

   Raises:
      - ConstaintViolation: Can't insert due to Constraint Violation
      - IntegrityError: Can't insert due to Integrity Error
      - Others
   """

   try:
      db.session.add(record)
      db.session.commit()
   except (exc.dataerror, exc.integrityerror, exc.sqlalchemy) as error:
      raise type(error)
      return
   except exc.sqlalchemyerror as error:
      raise Exception('UnhandleExceptions: {}'.format(error))
      return

