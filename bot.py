#!/usr/bin/env python3
#env variables
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import lib

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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

if __name__ == '__main__':
    print(TOKEN)
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('genera', generate))
    application.add_handler(CommandHandler('vincoli', vincoli))
    
    application.run_polling()
