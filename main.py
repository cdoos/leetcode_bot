from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
from query.getUserProfile import getuser, getprofile
from sql.update_sql import get_top_10, update_user, update_all_users
import prettytable as pt
import imgkit

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

IMGKIT_CONFIG = imgkit.config(wkhtmltoimage='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')
IMGKIT_OPTIONS = {'width': 800, 'disable-smart-width': ''}

whitelist = [-1001386280522, -616311142]


def get_token() -> str:
    with open('token.txt') as f:
        token = f.read().strip()
    return token


def top_image(top: list) -> bytes:
    table = pt.PrettyTable(['Username', 'Easy', 'Medium', 'Hard', 'All', 'Recent Submission'])
    table.align['Username'] = 'c'
    table.align['Easy'] = 'c'
    table.align['Medium'] = 'c'
    table.align['Hard'] = 'c'
    table.align['All'] = 'c'
    table.align['Recent Submission'] = 'c'
    for user in top:
        row = []
        for data in user:
            row.append(data)
        table.add_row(row)
    img = imgkit.from_string(table.get_html_string(format=True), False, config=IMGKIT_CONFIG, options=IMGKIT_OPTIONS)
    return img


def profile(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    if chat.id not in whitelist:
        return
    message = update.message
    if len(message.text.split(' ')) != 2:
        message.reply_text('Incorrect arguments! Try: /profile <username>')
        return
    message.reply_text(getuser(message.text.split(' ')[1]))


def add_top(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    if chat.id not in whitelist:
        return
    message = update.message
    if len(message.text.split(' ')) != 2:
        message.reply_text('Incorrect arguments! Try: /add_top <username>')
        return
    try:
        user_data = getprofile(message.text.split(' ')[1])
    except ValueError as e:
        message.reply_text(str(e))
        return
    update_user(user_data)
    message.reply_text('Profile ' + user_data[0] + ' successfully added to the top list!')


def top_all(update: Update, context: CallbackContext) -> None:
    message = update.message
    top = get_top_10('count_all')
    message.reply_photo(top_image(top))


def top_easy(update: Update, context: CallbackContext) -> None:
    message = update.message
    top = get_top_10('easy')
    message.reply_photo(top_image(top))


def top_medium(update: Update, context: CallbackContext) -> None:
    message = update.message
    top = get_top_10('medium')
    message.reply_photo(top_image(top))


def top_hard(update: Update, context: CallbackContext) -> None:
    message = update.message
    top = get_top_10('hard')
    message.reply_photo(top_image(top))


def update_top(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    if chat.id not in whitelist:
        return
    message = update.message
    update_all_users()
    message.reply_text('The top list is successfully updated')


def commands(update: Update, context: CallbackContext) -> None:
    message = update.message
    response = 'The list of commands:\n\n' + \
               '/profile <username> - get user profile\n\n' + \
               '/add_top <username> - add profile to the top list\n\n' + \
               '/top_all - return the top 10 profiles sorted by all submissions\n\n' + \
               '/top_easy, /top_medium, /top_hard - top 10 sorted by easy, medium, hard respectively\n\n' + \
               '/update_top - updates the top list'
    message.reply_text(response)


def main() -> None:
    updater = Updater(token=get_token(), use_context=True)
    dispatcher = updater.dispatcher
    handlers = [CommandHandler('profile', profile),
                CommandHandler('add_top', add_top),
                CommandHandler('top_all', top_all),
                CommandHandler('top_easy', top_easy),
                CommandHandler('top_medium', top_medium),
                CommandHandler('top_hard', top_hard),
                CommandHandler('update_top', update_top),
                CommandHandler('commands', commands)]
    for handler in handlers:
        dispatcher.add_handler(handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
