# Use PyMySQL as MySQLdb replacement so Django can talk to MySQL without mysqlclient
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # If PyMySQL is not installed yet this will fail silently until runtime
    pass
