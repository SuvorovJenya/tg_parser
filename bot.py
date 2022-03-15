import telebot
import module
from telebot import types
from main import upcoming_game, live_game, results_game


bot = telebot.TeleBot(module.TOKEN)
chat_id = module.chat_id


@bot.message_handler(commands=['help'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton('Upcoming game')
    item_2 = types.KeyboardButton('Live game')
    item_3 = types.KeyboardButton('Results game')
    markup.add(item_1, item_2, item_3)
    bot.send_message(message.chat.id, 
                     """This bot provides cs-go game from the HLTV""", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == 'Upcoming game' and len(upcoming_game()) > 0 :
        for i in upcoming_game():
            bot.send_message(message.chat.id, f"{i['date_game']}\n{i['team_1']} vs {i['team_2']}\n{i['event_name']}")
    elif message.text == 'Live game' and len(live_game()) > 0:   
        for i in live_game():
            bot.send_message(message.chat.id, f"{i['team_1']} vs {i['team_2']}\n{i['event_name']}")
    elif message.text == 'Results game' and len(results_game()) > 0:      
        for i in results_game():
                bot.send_message(message.chat.id, f"{i['team_won']} {i['score_won']} : {i['score_loser']} {i['team_loser']}\n{i['event_name']}")
    else:
        bot.send_message(message.chat.id, "empty...")
                
                                
if __name__ == "__main__":
    bot.polling(none_stop=True)            
    