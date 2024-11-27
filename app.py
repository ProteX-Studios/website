from flask import Flask, render_template, request, redirect, jsonify
from flask_pymongo import PyMongo
import discord
from discord.ext import tasks

# Initialize Flask app and MongoDB
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dbadmin:pawsdb@cluster0.ycmr6ir.mongodb.net"
mongo = PyMongo(app)

# Discord client for bot status
intents = discord.Intents.default()
intents.members = True  # Ensure this is set to True to fetch member data
intents.presences = True  # Required to get bot presence status
intents.guilds = True
discord_client = discord.Client(intents=intents)

bot_ids = [1122366129994743858, 1184584467969495091, 973774121827717140]  # Replace with bot IDs



@app.route('/bot-status', methods=['GET'])
def bot_status():
    # This endpoint will receive the "ping" from the bot
    print("Received ping from bot.")
    return jsonify({"message": "Bot is alive."}), 200

@app.route("/")
async def index():    
    return render_template("index.html")

@app.route('/settings/<bot_name>', methods=['GET', 'POST'])
def bot_settings(bot_name):
    bot_data = mongo.db.bots.find_one({"bot_name": bot_name})

    if request.method == 'POST':
        mongo.db.bots.update_one(
            {"bot_name": bot_name},
            {"$set": {
                "settings.prefix": request.form['prefix'],
                "settings.status_message": request.form['status_message'],
                "settings.log_channel": request.form['log_channel'],
                "settings.welcome_message": request.form['welcome_message']
            }}
        )
        return redirect('/')

    return render_template('bot-settings.html', bot_data=bot_data)


app.run()