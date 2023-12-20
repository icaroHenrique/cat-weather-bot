# cat-weather-bot

Cat Weather Bot is a Telegram bot that receives a location sent by the user and returns the temperature and apparent temperature of the sent location. It presents an image of a kitten and a phrase based on the indicated temperature. The project is intended for Python studies. Its main purpose is to be used to apply new concepts and techniques learned in language studies and enhance the use of what has already been learned. However, you can use it for your entertainment and/or as a basis for other projects!

The bot uses the Telegram API to communicate within the chat (it can be used by calling the bot privately or adding it to a group) and the Open Weather API, which provides the temperature based on the coordinates captured within Telegram when the location is sent. The Open Weather API has a free subscription sufficient for our bot, but it is possible to switch to a paid subscription to obtain more data beyond temperature.

## How to use
### Authorization with API Keys

A token is required for each of the APIs mentioned for the bot's usage. You will find more details in the official documentation for each API below:

**Telegram Bot**: https://core.telegram.org/bots/features#botfather

**Open Weather API**:  https://openweathermap.org/current

## Installing locally
To use and test the bot locally, it is recommended to create a virtual environment with **venv** and activate the environment to start installing dependencies:
```
python -m venv .venv
.venv/scripts/activate
```

Now, create a **.env** file based on **.env-sample**. Edit the file by inserting the API tokens for each service and finish by installing the project's dependencies with **pip**:
```
cp .env-sample .env
vi .env
pip install -r requirements.txt
```

As we use **Dynaconf** in conjunction with **dotenv**, the variables will be automatically loaded based on the **.env** file.