from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import random
import pytz
from datetime import datetime, timedelta
import string

# Вопросы разделены по категориям
questions = [
    "Какое воспоминание из детства всегда вызывает у тебя улыбку?",
    "Если бы ты мог жить в любой точке мира, где бы это было и почему?",
    "Какие три вещи входят в твой список желаний?",
    "Какая книга или фильм были твоими любимыми в детстве и почему?",
    "Кто был самым влиятельным человеком в твоей жизни?",
    "Опиши свой идеальный уик-энд.",
    "Какой один талант или хобби ты всегда хотел развить?",
    "Чего ты боишься и что хочешь преодолеть?",
    "Если бы ты мог поужинать с любыми тремя людьми (мертвыми или живыми), кто бы это был?",
    "Какой твой любимый способ провести время в одиночестве?",
    "Какую детскую мечту ты до сих пор хочешь осуществить?",
    "Как ты предпочитаешь отмечать свой день рождения?",
    "Каким навыком ты восхищаешься в других и хотел бы обладать сам?",
    "Какая твоя самая заветная семейная традиция?",
    "Что нового ты недавно узнал о себе?",
    "Что для тебя значит близость и как ты лучше всего ее выражаешь?",
    "Как, по твоему мнению, наша эмоциональная связь влияет на физическую близость?",
    "Что из того, что я делаю, заставляет тебя чувствовать себя глубоко любимым?",
    "Как, по-твоему, мы можем поддерживать страсть в наших отношениях?",
    "Какие у тебя есть любимые способы проявить привязанность?",
    "Каким образом ты чувствуешь себя наиболее ценным и значимым в наших отношениях?",
    "Как мы можем лучше сообщать о своих желаниях и границах в спальне?",
    "Какую фантазию или желание тебе было интересно исследовать со мной?",
    "Как ты относишься к роли романтики в долгосрочных отношениях?",
    "Что нового ты хотел бы попробовать вместе, чего мы еще не делали?",
    "Насколько важно физическое влечение в наших отношениях и как его поддерживать?",
    "Что из того, что я делаю, заставляет тебя чувствовать себя наиболее привязанным ко мне в сексуальном плане?",
    "Как, по-твоему, изменилась наша личная жизнь с тех пор, как мы вместе?",
    "Какими способами мы можем углубить нашу эмоциональную близость?",
    "Какие твои любимые воспоминания связаны с нашими интимными моментами?",
    "Что для тебя значит любовь?",
    "Что ты думаешь о балансе между работой и личной жизнью?",
    "Как ты справляешься со стрессом или сложными ситуациями?",
    "Каковы твои самые важные ценности?",
    "Как ты видишь свою жизнь через 5 лет?",
    "Что было твоей самой большой проблемой в жизни, и как ты ее преодолел?",
    "Что ты думаешь о прощении и затаивании обиды?",
    "Что бы ты хотел, чтобы люди понимали о тебе?",
    "Какой опыт сильно повлиял на твое мировоззрение?",
    "Как, по твоему мнению, выглядят успешные отношения?",
    "Какой жизненный урок ты усвоил с трудом?",
    "Что ты думаешь о духовности или религии?",
    "Как ты относишься к созданию семьи?",
    "Какой важный урок ты извлек из прошлых отношений?",
    "Как, по-твоему, мы можем поддержать мечты и цели друг друга?",
    "Если бы ты был животным, кем бы ты был и почему?",
    "Какой самый глупый поступок ты когда-либо совершал?",
    "Если бы ты мог обладать суперспособностью, что бы это было?",
    "Какую самую неловкую песню ты любишь?",
    "Что бы ты сделал, если бы завтра выиграл в лотерею?",
    "Если бы ты мог стать персонажем любого фильма, то кем бы ты был?",
    "Какой у тебя самый необычный талант?",
    "Если бы ты мог есть только одну еду до конца жизни, что бы это было?",
    "Какой самый безумный сон тебе когда-либо снился?",
    "Если бы ты стал невидимым на один день, что бы ты сделал?",
    "Какая твоя любимая шутка?",
    "Если бы ты мог путешествовать в прошлое, какую эпоху ты бы посетил?",
    "Что у тебя плохо получается, но тебе все равно нравится это делать?",
    "Какой самый спонтанный поступок ты когда-либо совершал?",
    "Если бы ты мог поменяться жизнью с кем угодно на один день, кто бы это был?",
    "Где ты видишь себя живущим в будущем?",
    "К какой карьерной цели ты сейчас стремишься?",
    "Какую одну вещь ты хочешь выполнить до своей смерти?",
    "Какое наследие ты хочешь оставить после себя?",
    "Как ты представляешь себе свой выход на пенсию?",
    "Какой отпуск мечты ты всегда хотел провести?",
    "Если бы ты мог начать любой бизнес, что бы это было?",
    "Какой одной вещи ты надеешься достичь в ближайший год?",
    "Где ты видишь наши отношения через 5 лет?",
    "Что ты никогда не делал, но всегда хотел попробовать?",
    "Как ты хочешь вырасти или измениться в ближайшие несколько лет?",
    "Какой навык или хобби вы хотели бы освоить вместе?",
    "Какую важную цель мы должны иметь как пара?",
    "О каком способе отпраздновать годовщину ты мечтаешь?",
    "Какое одно приключение ты хочешь пережить вместе?"
]

# Идеи для совместной деятельности
activities = [
    {"name": "Приготовить ужин вместе", "image_url": ""},
    {"name": "Посмотреть фильм", "image_url": ""},
    {"name": "Совместная прогулка в парке", "image_url": ""},

]

# Словарь для хранения данных пользователей и их ключей
user_data = {}

def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Команда для старта бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для пар. Вот что я могу делать:\n"
        "1. Помогать задавать друг другу интересные вопросы.\n"
        "2. Предлагать идеи для совместной деятельности.\n"
        "3. Устанавливать удобное время и напоминания.\n"
        "\nДоступные команды:\n"
        "/start - Запуск бота\n"
        "/key - Создать общий ключ для пары\n"
        "/join_key <ключ> - Присоединиться к паре по ключу\n"
        "/set_time - Установить время для вопросов\n"
        "/set_activity_time - Установить время для совместной деятельности\n"
        "/reset - Сбросить данные и начать заново\n"
        "/help - Показать список команд\n"
    )

# Команда для вывода списка всех команд
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вот список доступных команд:\n"
        "/start - Запуск бота\n"
        "/key - Создать общий ключ для пары\n"
        "/join_key <ключ> - Присоединиться к паре по ключу\n"
        "/set_time - Установить время для вопросов\n"
        "/set_activity_time - Установить время для совместной деятельности\n"
        "/reset - Сбросить данные и начать заново\n"
        "/help - Показать список команд"
    )

# Создание общего ключа для пары
async def create_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key = generate_key()
    user_data[update.message.chat_id] = {
        "key": key,
        "partner": None,
        "question_time": None,
        "activity_time": None,
        "answers": []
    }
    await update.message.reply_text(
        f"Ваш общий ключ: {key}.\n"
        f"Передайте его вашему партнеру или отправьте ссылку для подключения: \n"
        f"https://t.me/voprosiki_dly_nas_bot?start={key}"
    )

# Ввод ключа для подключения
async def join_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        partner_key = context.args[0]
        for user_id, data in user_data.items():
            if data.get("key") == partner_key:
                user_data[user_id]["partner"] = update.message.chat_id
                user_data[update.message.chat_id] = {
                    "key": partner_key,
                    "partner": user_id,
                    "question_time": None,
                    "activity_time": None,
                    "answers": []
                }
                await update.message.reply_text("Вы успешно подключены к вашей паре!")
                await context.bot.send_message(chat_id=user_id, text="Ваш партнер подключился!")
                return
        await update.message.reply_text("Ключ не найден. Убедитесь, что вы ввели правильный ключ.")
    except (IndexError, ValueError):
        await update.message.reply_text("Используйте: /join_key <ключ>")

# Установка времени для вопросов
async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("13:00", callback_data="13:00")],
        [InlineKeyboardButton("17:00", callback_data="17:00")],
        [InlineKeyboardButton("21:00", callback_data="21:00")],
        [InlineKeyboardButton("Ввести вручную", callback_data="manual")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите время для вопросов:", reply_markup=reply_markup)

# Установка времени для совместной деятельности
async def set_activity_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("10:00", callback_data="10:00")],
        [InlineKeyboardButton("18:00", callback_data="18:00")],
        [InlineKeyboardButton("Ввести вручную", callback_data="manual_activity")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите время для совместной деятельности:", reply_markup=reply_markup)

# Обработка нажатий кнопок выбора времени
async def set_time_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id

    if query.data == "manual":
        await query.edit_message_text("Введите желаемое время в формате ЧЧ:ММ (например, 15:30):")
        return

    user_data[user_id]["question_time"] = query.data
    partner_id = user_data[user_id].get("partner")

    if partner_id:
        partner_time = user_data[partner_id].get("question_time")
        if partner_time and partner_time != query.data:
            await context.bot.send_message(
                chat_id=partner_id,
                text=f"Ваш партнер выбрал {query.data}, вы выбрали {partner_time}. Предлагаем выбрать среднее арифметическое или оставить одно из значений."
            )
    await query.edit_message_text(f"Вы выбрали время для вопросов: {query.data}")

async def set_activity_time_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id

    if query.data == "manual_activity":
        await query.edit_message_text("Введите желаемое время для совместной деятельности в формате ЧЧ:ММ:")
        return

    # Если пользователь еще не инициализирован, создаем пустую структуру данных
    if user_id not in user_data:
        user_data[user_id] = {'time': None, 'activity_time': None}
        
    # Теперь безопасно обновляем данные пользователя
    user_data[user_id]['time'] = time_value
        
    user_data[user_id]["activity_time"] = query.data
    await query.edit_message_text(f"Вы выбрали время для совместной деятельности: {query.data}")

# Обработка ввода времени вручную
async def manual_time_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    time_input = update.message.text

    # Проверяем инициализацию данных пользователя
    if user_id not in user_data:
        user_data[user_id] = {
            "key": None,
            "partner": None,
            "question_time": None,
            "activity_time": None,
            "answers": []
        }

    try:
        datetime.strptime(time_input, "%H:%M")
        if user_data[user_id]["question_time"] is None:
            user_data[user_id]["question_time"] = time_input
            partner_id = user_data[user_id].get("partner")
            if partner_id:
                partner_time = user_data[partner_id].get("question_time")
                if partner_time and partner_time != time_input:
                    await context.bot.send_message(
                        chat_id=partner_id,
                        text=f"Ваш партнер выбрал {time_input}, вы выбрали {partner_time}. Предлагаем выбрать среднее арифметическое или оставить одно из значений."
                    )
            await update.message.reply_text(f"Вы установили время для вопросов: {time_input}")
        else:
            user_data[user_id]["activity_time"] = time_input
            await update.message.reply_text(f"Вы установили время для совместной деятельности: {time_input}")
    except ValueError:
        await update.message.reply_text("Некорректный формат времени. Пожалуйста, введите в формате ЧЧ:ММ (например, 15:30).")

# Предложение совместной деятельности одному из участников пары
async def suggest_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    partner_id = user_data.get(user_id, {}).get("partner")

    if not partner_id:
        await update.message.reply_text("У вас пока нет пары. Используйте /key или /join_key для подключения.")
        return

    activity = random.choice(activities)
    await context.bot.send_message(
        chat_id=user_id,
        text=f"Попробуйте это: {activity['name']}"
    )
    await context.bot.send_message(
        chat_id=partner_id,
        text=f"Вашему партнёру предложено: {activity['name']}"
    )

# Сброс данных бота
async def reset_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    if user_id not in user_data:
        await update.message.reply_text("У вас пока нет данных. Используйте /start для начала.")
        return

    partner_id = user_data[user_id].get("partner")
    if partner_id:
        user_data.pop(partner_id, None)
        await context.bot.send_message(
            chat_id=partner_id,
            text="Ваши данные и данные вашей пары были сброшены. Вы можете начать заново."
        )

    user_data.pop(user_id, None)
    await update.message.reply_text(
        "Ваши данные и данные вашей пары были успешно сброшены. Вы можете начать заново, используя команду /start."
    )

# Регистрация хендлеров
def main():
    # API-ключ
    api_key = '7055486716:AAFpEl2cydDWw98BjRSeEsYmWFoUpjysdiQ'

    application = Application.builder().token(api_key).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("key", create_key))
    application.add_handler(CommandHandler("join_key", join_key))
    application.add_handler(CommandHandler("set_time", set_time))
    application.add_handler(CommandHandler("set_activity_time", set_activity_time))
    application.add_handler(CommandHandler("suggest_activity", suggest_activity))
    application.add_handler(CommandHandler("reset", reset_bot))

    # Обработчик для кнопок
    application.add_handler(CallbackQueryHandler(set_time_callback, pattern="^(13:00|17:00|21:00|manual)$"))
    application.add_handler(CallbackQueryHandler(set_activity_time_callback, pattern="^(10:00|18:00|manual_activity)$"))

    # Обработчик для ручного ввода времени
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manual_time_handler))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
