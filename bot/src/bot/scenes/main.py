from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.scene import SceneRegistry
from enums.profile_enums import BotWords

import bot.main.scenes.accounts.accounts_list as account_scene
import bot.main.scenes.accounts.edit_and_save as edit_and_save_scene
import bot.main.scenes.data_account as data_account_scene
import bot.main.scenes.feedback as feedback_scene
import bot.main.scenes.settings as setting_scene
import bot.main.scenes.start_msg as start_scene
from bot.main.keyboards import KeyboardText

main_router = Router()
main_router.message.register(
    start_scene.StartMsgScene.as_handler(), CommandStart(),
)
main_router.message.register(
    start_scene.StartMsgScene.as_handler(),
    F.text.lower().in_(BotWords.START.value),
)
main_router.message.register(
    start_scene.StartMsgScene.as_handler(),
    F.text.lower().in_(BotWords.EXIT.value),
)

main_router.message.register(
    account_scene.ListUtilitiesAccountsScene.as_handler(),
    F.text == KeyboardText.CHANGE_ID.value,
)

main_router.message.register(
    setting_scene.SettingScene.as_handler(),
    F.text == KeyboardText.SETTINGS.value,
)
main_router.message.register(
    setting_scene.SettingScene.as_handler(),
    Command(commands=['settings']),
)
main_router.message.register(
    data_account_scene.GetDataAccountScene.as_handler(),
    F.text == KeyboardText.CHECK_DEBT.value,
)
main_router.message.register(
    data_account_scene.GetDataAccountScene.as_handler(),
    Command(commands=['my_accounts']),
)

main_router.message.register(
    feedback_scene.FeedbackScene.as_handler(),
    Command(commands=['feedback']),
)

main_scene_registry = SceneRegistry(main_router)
main_scene_registry.add(
    start_scene.StartMsgScene,

    data_account_scene.GetDataAccountScene,
    data_account_scene.CheckDataAccountScene,

    account_scene.ListUtilitiesAccountsScene,

    edit_and_save_scene.EditElectricityAccountScene,
    edit_and_save_scene.SaveElectricityAccountScene,

    edit_and_save_scene.EditGasAccountScene,
    edit_and_save_scene.SaveGasAccountScene,

    edit_and_save_scene.EditGasServiceAccountScene,
    edit_and_save_scene.SaveGasServiceAccountScene,

    edit_and_save_scene.EditWaterAccountScene,
    edit_and_save_scene.SaveWaterAccountScene,

    setting_scene.SettingScene,
    setting_scene.EditNoticeIntervalScene,
    setting_scene.EditNoticeStateScene,
    setting_scene.EditPeriodNoticeInterval,

    feedback_scene.FeedbackScene,
    feedback_scene.FeedbackReviewScene,
    feedback_scene.FoundErrorScene,
)
