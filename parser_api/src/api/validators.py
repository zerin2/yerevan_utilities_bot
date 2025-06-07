from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from core.exceptions import DuplicateAccountError
from core.settings import settings

security = HTTPBearer()


def get_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme != 'Bearer':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication scheme',
        )
    if credentials.credentials != settings.api_parser_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication token',
        )
    return credentials.credentials


def check_duplicate_accounts(message_data_account: list[dict]) -> None:
    accounts = [
        account.get('account')
        for account in message_data_account
    ]
    if len(set(accounts)) != len(message_data_account):
        raise DuplicateAccountError('Найден дублирующийся аккаунт.')
