from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import BaseFilter, invert_f
from aiogram.filters import Command
from aiogram.filters import and_f
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = 'BOT TOKEN HERE'

# Создаем объекты бота и диспетчера
bot = Bot(token='7573631171:AAEBYmKHoMnhapTwoqi9ErXKaw2e310OIZM')
dp = Dispatcher()
admin_ids: list[int] = [833266070]
kb_builder = ReplyKeyboardBuilder()
admin_mode = KeyboardButton(
    text='Админский режим'
)
user_mode = KeyboardButton(
    text='Пользовательский режим'
)
kb_builder.row(admin_mode,user_mode, width=2)
async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/support',
                   description='Поддержка'),
        BotCommand(command='/contacts',
                   description='Другие способы связи'),
        BotCommand(command='/payments',
                   description='Платежи')
    ]

    await bot.set_my_commands(main_menu_commands)
# Собственный фильтр, проверяющий юзера на админа
class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        # В качестве параметра фильтр принимает список с целыми числами
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
@dp.message(and_f(IsAdmin(admin_ids),F.text.startswith('Выбрать режим')))
async def answer_if_admins_update(message: Message):
    await message.answer(
        text='...',
        reply_markup=kb_builder.as_markup(resize_keyboard=True)
    )
@dp.message(Command(commands='start'))
async def start_message(message:Message):
    await message.answer(text='Привет,это мой бот')
# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(F.text.startswith('Выбрать режим'))
async def user_message(message: Message):
    await message.answer(text='У вас нет прав админа(хуй тебе)'
                         )
@dp.message()
async def user_message(message: Message):
    await message.answer(text=message.text
                         ,reply_markup=ReplyKeyboardRemove()
                         )

if __name__ == '__main__':
    dp.run_polling(bot)