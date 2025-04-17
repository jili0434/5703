import psycopg2

class DBConfig:
    def __init__(self, name, user, password, host, port):
        self.name = name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

def get_connection(config):
    return psycopg2.connect(
        dbname=config.name,
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port
    )