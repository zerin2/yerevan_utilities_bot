import datetime as dt
import decimal

from loguru import logger

from bot.crud.base import BaseBotManager
from bot.crud.users import UserBotManager
from bot.enums.scene_enums import UtilityName
from db.models import AccountsDetail, StatusType, UsersProfile, UtilitiesType
from exceptions import Account404


class AccountBotManager(BaseBotManager):
    """Менеджер для работы со счетами (электричество, газ, вода и др.)."""

    async def add_account_value_by_tg_id(
            self, tg_id: str, field_name: str, value: str,
    ) -> UsersProfile | None:
        """Обновляет указанное поле профиля пользователя по Telegram ID."""
        return await self.edit_one_value(
            model=self.USER_PROFILE_MODEL,
            field_name='telegram_id',
            value=str(tg_id),
            update_field_name=field_name,
            new_value=value,
        )

    async def get_all_account_by_tg_id(self, tg_id: str) -> dict:
        """Получение всех счетов user по tg_id."""
        user = await self.get_by_field(self.USER_PROFILE_MODEL, 'telegram_id', str(tg_id))
        if user is None:
            error = f'Не найден аккаунт "{tg_id}"'
            logger.error(error)
            raise Account404(error)
        user_accounts = {
            UtilityName.ELECTRICITY.value: user.electricity,
            UtilityName.GAS.value: user.gas,
            UtilityName.GAS_SERVICE.value: user.gas_service,
            UtilityName.WATER.value: user.water,
            UtilityName.VIVA_MTS.value: user.viva_mts,
            UtilityName.TEAM_TELECOM.value: user.team_telecom,
            UtilityName.U_COM.value: user.u_com,
            UtilityName.OVIO.value: user.ovio,
        }
        return user_accounts


class StatusTypeBotManager(BaseBotManager):
    """Менеджер для работы с типами статусов."""

    async def get_status_by_id(self, status_id: int) -> StatusType | None:
        """Получение 'status_type' из модели(StatusType) по 'id'."""
        return await self.get_by_field(self.STATUS_TYPE_MODEL, 'id', status_id)

    async def get_status_by_name(self, status_name: str) -> StatusType | None:
        """Получение 'status_type' из модели(StatusType) по 'name'."""
        return await self.get_by_field(self.STATUS_TYPE_MODEL, 'name', status_name)

    async def get_or_create_status_by_name(self, name: str) -> StatusType | None:
        """Получение 'status_type' из модели(StatusType) по 'id'.
        Если не существует, то создает и возвращает 'id'.
        """
        status = await self.get_status_by_name(name)
        if status:
            return status
        await self.add_status_by_name(name)
        return await self.get_status_by_name(name)

    async def add_status_by_name(self, name: str) -> StatusType | None:
        """Добавьте нового Status, если не существует."""
        return await self.add_new_instance(self.STATUS_TYPE_MODEL, {'name': str(name)})


class UtilitiesTypeBotManager(BaseBotManager):
    """Менеджер для работы с типами коммунальных услуг."""

    async def get_utility_by_id(self, utility_id: int) -> UtilitiesType | None:
        """Получение 'utility_type' из модели(UtilitiesType) по 'id'."""
        return await self.get_by_field(self.UTILITIES_TYPE_MODEL, 'id', utility_id)

    async def get_utility_by_name(self, utility_name: str) -> UtilitiesType | None:
        """Получение 'utility_type' из модели(UtilitiesType) по 'name'."""
        return await self.get_by_field(self.UTILITIES_TYPE_MODEL, 'name', utility_name)

    async def get_or_create_utility_by_name(self, name: str) -> UtilitiesType | None:
        """Получение 'utility_type' из модели(UtilitiesType) по 'id'.
        Если не существует, то создает и возвращает 'id'.
        """
        status = await self.get_utility_by_name(name)
        if status:
            return status
        await self.add_utility_by_name(name)
        return await self.get_utility_by_name(name)

    async def add_utility_by_name(self, name: str) -> UtilitiesType | None:
        """Добавьте нового utility, если не существует."""
        return await self.add_new_instance(self.UTILITIES_TYPE_MODEL, {'name': str(name)})


class AccountsDetailsBotManager(BaseBotManager):
    """Менеджер для работы с информацией о коммунальных счетах пользователя."""

    async def get_account_detail_by_tg_id(self, tg_id: str) -> AccountsDetail | None:
        """Получение 'account_detail' из модели(AccountsDetails) по 'tg_id'."""
        user_repo = UserBotManager(self.session)
        user = await user_repo.get_user_by_tg_id(str(tg_id))
        return await self.get_by_field(self.ACCOUNTS_DETAILS_MODEL, 'user_id', user.id)

    async def edit_or_create_account_detail(
            self,
            tg_id: str,
            utility_name: str,
            last_overpayment: decimal,
            last_debt: decimal,
            address: str,
            traffic: str,
            status_name: str,
            info: str = '',
    ) -> AccountsDetail | None:
        """

        """
        user_repo = UserBotManager(self.session)
        utility_repo = UtilitiesTypeBotManager(self.session)
        status_repo = StatusTypeBotManager(self.session)

        user = await user_repo.get_user_by_tg_id(str(tg_id))
        user_id = user.id
        utility = await utility_repo.get_or_create_utility_by_name(utility_name)
        status = await status_repo.get_or_create_status_by_name(status_name)
        now = dt.datetime.now()

        return await self.edit_or_create_values(
            model=self.ACCOUNTS_DETAILS_MODEL,
            field_name='user_id',
            value=user_id,
            new_values={
                'user_id': user_id,
                'utility_type_id': utility.id,
                'last_overpayment': last_overpayment,
                'last_debt': last_debt,
                'address': address,
                'traffic': traffic,
                'last_update': now,
                'notice_id': user.notice_type_id,
                'status': status.id,
                'info': info,
            },
        )
