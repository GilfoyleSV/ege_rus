#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that works with polls. Only 3 people are allowed to interact with each
poll/quiz the bot generates. The preview command generates a closed poll/quiz, exactly like the
one the user sends the bot
"""
import logging
import random

from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    PollHandler,
    filters,
)

accents_list = ["Иксы",
                "Отзыв",
                "Отрочество",
                "аэропОрты",
                "бАнты",
                "бОроду",
                "бралА",
                "бралАсь",
                "бухгАлтеров",
                "вОвремя",
                "вернА",
                "вероисповЕдание",
                "взялА",
                "взялАсь",
                "влилАсь",
                "водопровОд",
                "ворвалАсь",
                "воспринЯть",
                "воссоздалА",
                "вручИт",
                "газопровОд",
                "гналА",
                "гналАсь",
                "граждАнство",
                "дОверху",
                "дОнизу",
                "дОсуха",
                "дефИс",
                "дешевИзна",
                "диспансЕр",
                "добралА",
                "добралАсь",
                "довезЁнный",
                "договорЁнность",
                "дождалАсь",
                "дозИровать",
                "дозвонИтся",
                "докумЕнт",
                "донЕльзя",
                "досУг",
                "еретИк",
                "жалюзИ",
                "ждалА",
                "жилОсь",
                "зАгнутый",
                "зАнятый",
                "зАпертый",
                "зАсветло",
                "зАтемно",
                "закУпорив",
                "закУпорить",
                "занЯть",
                "заперлА",
                "запломбировАть",
                "заселЁнный",
                "защемИт",
                "звалА",
                "звонИт",
                "знАчимость",
                "знАчимый",
                "кАшлянуть",
                "кОнусов",
                "кУхонный",
                "каталОг",
                "квартАл",
                "киломЕтр",
                "клАла",
                "клЕить",
                "корЫсть",
                "кормЯщий",
                "крАлась",
                "крАны",
                "красИвее",
                "красИвее",
                "кремЕнь",
                "кровоточАщий",
                "кровоточИть",
                "лЕкторов",
                "лОктя",
                "лгалА",
                "лилА",
                "лилАсь",
                "ловкА",
                "лыжнЯ",
                "мЕстностей",
                "мозаИчный",
                "нАчатый",
                "нЕдруг",
                "нЕнависть",
                "нОгтя",
                "навралА",
                "надОлго",
                "наделИт",
                "надорвалАсь",
                "нажИвший",
                "назвалАсь",
                "накренИтся",
                "налИвший",
                "налилА",
                "намЕрение",
                "нанЯвшийся",
                "нарОст",
                "нарвалА",
                "начАв",
                "начАвший",
                "начАвшись",
                "начАть",
                "недУг",
                "некролОг",
                "ненадОлго",
                "нефтепровОд",
                "низведЁнный",
                "новостЕй",
                "обзвонИт",
                "облегчЁнный",
                "облегчИть",
                "облилАсь",
                "обнялАсь",
                "обогналА",
                "ободрЁнный",
                "ободрИть",
                "ободрИться",
                "ободралА",
                "обострЁнный",
                "обострИть",
                "одолжИть",
                "озлОбить",
                "оклЕить",
                "окружИт",
                "опОшлить",
                "оптОвый",
                "освЕдомиться",
                "отбылА",
                "отдАв",
                "отдалА",
                "отзЫв",
                "Отзыв",
                "откУпорить",
                "отключЁнный",
                "отозвалА",
                "отозвалАсь",
                "пОручни",
                "партЕр",
                "перезвонИт",
                "перелилА",
                "плодоносИть",
                "пломбировАть",
                "повторЁнный",
                "повторИт",
                "поделЁнный",
                "поднЯв",
                "позвалА",
                "позвонИт",
                "полилА",
                "положИть",
                "понЯв",
                "понЯвший",
                "понЯть",
                "портфЕль",
                "послАла",
                "прИнятый",
                "прибЫв",
                "прибЫть",
                "придАное",
                "призЫв",
                "принЯть",
                "приручЁнный",
                "прожИвший",
                "прозорлИвый",
                "рвалА",
                "сОгнутый",
                "свЁкла",
                "сверлИт",
                "сирОты",
                "слИвовый",
                "снялА",
                "снятА",
                "совралА",
                "созЫв",
                "создАв",
                "создалА",
                "сорИт",
                "сорвалА",
                "сосредотОчение",
                "срЕдства",
                "стАтуя",
                "столЯр",
                "тОрты",
                "тУфля",
                "тамОжня",
                "убралА",
                "углубИть",
                "углублЁнный",
                "укрепИт",
                "цЕнтнер",
                "цемЕнт",
                "цепОчка",
                "чЕрпать",
                "шАрфы",
                "шофЁр",
                "щЁлкать",
                "щемИт",
                "экспЕрт", ]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inform user about what this bot can do"""
    await update.message.reply_text(
        "Please select /poll to get a Poll, /quiz to get a Quiz or /preview"
        " to generate a preview for your poll"
    )


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a predefined poll"""
    correct_word = random.choice(accents_list)
    wrong_answer = correct_word.lower()
    s = []
    for i in range(len(correct_word)):
        if wrong_answer[i] in 'аоуиыеё':
            if wrong_answer[:i] + wrong_answer[i:].capitalize() != correct_word:
                s.append(wrong_answer[:i] + wrong_answer[i:].capitalize())
    questions = [correct_word, random.choice(s)]
    random.shuffle(questions)
    message = await update.effective_message.reply_poll(
        correct_word.lower(), questions, type=Poll.QUIZ, correct_option_id=questions.index(correct_word)
    )
    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    payload = {
        message.poll.id: {"chat_id": update.effective_chat.id, "message_id": message.message_id}
    }
    context.bot_data.update(payload)


async def receive_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Close quiz after three participants took it"""
    # the bot can receive closed poll updates we don't care about
    if update.poll.is_closed:
        return
    if update.poll.total_voter_count == 1:
        try:
            quiz_data = context.bot_data[update.poll.id]
        # this means this poll answer update is from an old poll, we can't stop it then
        except KeyError:
            return
        await context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])


async def preview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ask user to create a poll and display a preview of it"""
    # using this without a type lets the user chooses what he wants (quiz or poll)
    button = [[KeyboardButton("Press me!", request_poll=KeyboardButtonPollType())]]
    message = "Press the button to let the bot generate a preview for your poll"
    # using one_time_keyboard to hide the keyboard
    await update.effective_message.reply_text(
        message, reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a help message"""
    await update.message.reply_text("Use /quiz, /poll or /preview to test this bot.")


def main() -> None:
    application = Application.builder().token("7192061783:AAG3OJY1BiXdqMRRB-Gtpxnn9fu03BMy920").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("preview", preview))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(PollHandler(receive_quiz_answer))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
