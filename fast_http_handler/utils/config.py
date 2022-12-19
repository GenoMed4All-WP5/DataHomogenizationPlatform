import os

SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]
MLFLOW_URL = "http://localhost:5000"

# @@@@@@@ KC SETTINGS @@@@@@
REALM = os.environ['KEYCLOAK_REALM']
KEYCLOAK_URL = os.environ['KEYCLOAK_URL']
CLIENT_ID = os.environ['KEYCLOAK_CLIENT_ID']
AUTHORIZATION_URL = KEYCLOAK_URL + "realms/" + REALM + "/protocol/openid-connect/auth"
TOKEN_URL = KEYCLOAK_URL + "realms/" + REALM + "/protocol/openid-connect/token"
KEYCLOAK_ADMIN = os.environ['ADMIN_USERNAME']
KEYCLOAK_PASSWORD = os.environ['ADMIN_PASSWORD']
EXECUTOR_TYPE = "docker"
