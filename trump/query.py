try:
    from .config import DB
except:
    DB = 'mysql'

if DB == 'mysql':
    from trump_db_mysql.query import *
elif DB == 'oracle':
    from trump_db_oracle.query import *
elif DB == 'pgsql':
    from trump_db_pgsql.query import *
