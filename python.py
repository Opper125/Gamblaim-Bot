import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import random
import requests

# Bot Token
TOKEN = "7514994664:AAHWJZG940D-d8DDggdCneu3SpWdLe8s4V8"

# User Data Storage
user_data = {}

# Slot Games List
slot_games = [
    {"name": "Fruit Slot", "cost": 1000, "animation": "🍒🍋🍊"},
    {"name": "Diamond Slot", "cost": 2000, "animation": "💎💎💎"},
    {"name": "Gold Slot", "cost": 3000, "animation": "💰💰💰"},
    {"name": "Lucky 7", "cost": 5000, "animation": "🎰🎰🎰"},
    {"name": "Treasure Hunt", "cost": 10000, "animation": "🗺️⚓💎"},
    {"name": "Mystic Moon", "cost": 15000, "animation": "🌕🔮✨"},
    {"name": "Pirate Booty", "cost": 20000, "animation": "🏴‍☠️⚔️💎"},
    {"name": "Dragon's Hoard", "cost": 25000, "animation": "🐉💰🔥"},
    {"name": "Starburst", "cost": 30000, "animation": "🌌✨💫"},
    {"name": "Pharaoh's Fortune", "cost": 50000, "animation": "🐪🏺👑"},
]

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start Command
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_data[user_id] = {"balance": 0}
    update.message.reply_text(
        "Welcome to Gamblaim Mini Bot!\n\n"
        "Use /deposit to add funds.\n"
        "Use /games to play slot games.\n"
        "Use /withdraw to withdraw your balance."
    )

# Deposit Command
def deposit(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    update.message.reply_text(
        "To deposit, please send money to:\n\n"
        "KPay: 09786284670\n"
        "WavePay: 09786284670\n\n"
        "After sending, reply with the amount you deposited."
    )

# Handle Deposit Amount
def handle_deposit(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    amount = int(update.message.text)
    user_data[user_id]["balance"] += amount
    update.message.reply_text(f"Deposited {amount} MMK. New balance: {user_data[user_id]['balance']} MMK")

# Games Command
def games(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(game["name"], callback_data=f"play_{i}")] for i, game in enumerate(slot_games)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose a game to play:", reply_markup=reply_markup)

# Play Game
def play_game(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    game_index = int(query.data.split("_")[1])
    game = slot_games[game_index]

    if user_data[user_id]["balance"] >= game["cost"]:
        user_data[user_id]["balance"] -= game["cost"]
        result = random.choice(["win", "lose"])
        if result == "win":
            winnings = game["cost"] * 2
            user_data[user_id]["balance"] += winnings
            query.edit_message_text(f"{game['animation']}\nYou won {winnings} MMK! New balance: {user_data[user_id]['balance']} MMK")
        else:
            query.edit_message_text(f"{game['animation']}\nYou lost. Better luck next time! New balance: {user_data[user_id]['balance']} MMK")
    else:
        query.edit_message_text("Insufficient balance to play this game.")

# Withdraw Command
def withdraw(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    update.message.reply_text("Enter the amount you want to withdraw:")
    context.user_data["action"] = "withdraw"

# Handle Withdraw Amount
def handle_withdraw(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    amount = int(update.message.text)
    if user_data[user_id]["balance"] >= amount:
        user_data[user_id]["balance"] -= amount
        update.message.reply_text(f"Withdrawn {amount} MMK. New balance: {user_data[user_id]['balance']} MMK")
    else:
        update.message.reply_text("Insufficient balance.")

# Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("deposit", deposit))
    dp.add_handler(CommandHandler("games", games))
    dp.add_handler(CommandHandler("withdraw", withdraw))
    dp.add_handler(CallbackQueryHandler(play_game, pattern="^play_"))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_deposit))

    # Start Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()