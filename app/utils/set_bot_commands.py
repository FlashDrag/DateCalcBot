from aiogram.types.bot_command import BotCommand


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(dp):
    commands = [
        BotCommand(command="start", description="START ✅"),
        BotCommand(command="/info", description="INFO⚠️"),
        BotCommand(command="/cancel", description="CANCEL ❌")
        ]
    await dp.bot.set_my_commands(commands)
