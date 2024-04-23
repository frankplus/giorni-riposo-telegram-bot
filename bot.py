#!/usr/bin/env python3
#env variables
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
import lib

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define state constants
RECEIVING_NEW_CONSTRAINTS = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text="Questo bot ti aiuta a generare i giorni di riposo per i dipendenti. "\
                                    "Usa il comando /genera per generare un nuovo programma settimanale.")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = str(lib.generate_weekly_schedule())
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def vincoli(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = lib.describe_scheduling_constraints()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def modifica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ok. Attualmente i vincoli definiti sono questi:')
    await update.message.reply_text(lib.describe_scheduling_constraints())
    await update.message.reply_text('Per favore, inviami i nuovi vincoli da impostare per il problema. Usa il comando /cancel per annullare.')
    return RECEIVING_NEW_CONSTRAINTS

async def receive_new_constraints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_constraints = update.message.text

    await update.message.reply_text('Sto aggiornando i vincoli...')

    result = lib.set_new_constraints_data_from_text(new_constraints)
    if result:
        await update.message.reply_text('Vincoli aggiornati.')
    else:
        await update.message.reply_text('Errore nell\'aggiornamento dei vincoli.')
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Modifica annullata.')
    return ConversationHandler.END

if __name__ == '__main__':
    print(TOKEN)
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('genera', generate))
    application.add_handler(CommandHandler('vincoli', vincoli))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('modifica', modifica)],
        states={
            RECEIVING_NEW_CONSTRAINTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_new_constraints)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)
    
    application.run_polling()
