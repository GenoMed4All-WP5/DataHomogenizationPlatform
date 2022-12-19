from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi import Security, HTTPException, status, Depends
from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin
import json

import config

# This is just for fastapi docs

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.TOKEN_URL)

keycloak_openid = KeycloakOpenID(
    server_url=config.KEYCLOAK_URL,
    client_id=config.CLIENT_ID,
    realm_name=config.REALM,
    verify=True
)


# Get keycloak public key
async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )


# Token and scopes check
"""
without scope:
current_user: auth.User = Security(auth.get_current_user)

with scope (need to be admin)
current_user: auth.User = Security(auth.get_current_user, scopes=["/admin"])
"""


async def get_current_user(
        security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    try:
        user = keycloak_openid.userinfo(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str("Error: Invalid authentication credentials"),
            headers={"WWW-Authenticate": "Bearer"},
        )

    for scope in security_scopes.scopes:
        if scope not in user['orgs']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": "Bearer scope=" + scope},
            )
    user = keycloak_openid.userinfo(token)
    return user


# Admin function to retireve keycloack users
async def get_users():
    try:
        ADMIN_USERNAME = KeycloakAdmin(
            server_url=config.KEYCLOAK_URL,
            username=config.KEYCLOAK_ADMIN,
            password=config.KEYCLOAK_PASSWORD
        )
        users = ADMIN_USERNAME.get_users({})
        for user in users:
            user['groups'] = ADMIN_USERNAME.get_user_groups(user['id'])
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Admin function to retireve keycloack groups/orgs
async def get_groups():
    try:
        ADMIN_USERNAME = KeycloakAdmin(
            server_url=config.KEYCLOAK_URL,
            username=config.KEYCLOAK_ADMIN,
            password=config.KEYCLOAK_PASSWORD
        )
        return ADMIN_USERNAME.get_groups({})

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
