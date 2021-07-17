## Hurricane Special Bot

This project is a Telegram bot to offer current hurricane information. Check the bot running [@HurricaneSpecialBot](https://t.me/HurricaneSpecialBot).

### Configuration
 
Before running need to add a `config.py` containing the:
 
* `API_KEY='<your bot key here>'`

* `URLS='<your_urls.yml>'`

* `OWNER_ID=<your_owner_id_integer>`

The url **YAML** file is going to be something like this:

```yaml
active: true
satellite_low: {url: 'https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/500x500.jpg'}
```

Then you can run as:

```bash
python3 main.py
```

### Utils

To send a message or a photo you can use the script `send_message.py`:

```bash
python3 send_message.py chat_ids.txt -t "Now tracking! Hurricane Felicia at the Eastern Pacific /hurricane" -p latest.jpg -c "Hurricane Felicia, Eastern Pacific."
```

To backend processing (`backend_processing.py`) calls `get_gif.sh` call it to download and process the clips. Call periodically.

```bash
python3 backend_processing.py
```

Where chat_ids.txt is a list of chat_ids as integers (no quotes) of your message recipient.

Note: The log file is going to be generated on the same directory than `main.py`