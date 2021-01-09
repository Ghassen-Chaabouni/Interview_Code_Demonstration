# Scraping Discord conversations
Scraping Discord conversations based on the name of the game, a start date, an end date and a list of words.

For more information about the implementation open the notebook ```test.ipynb```.

## Settings 
1/(Optional) Configure ```email```, ```password```, ```start_date_(dd/mm/yyyy)```, ```end_date_(dd/mm/yyyy)```, ```game_name```in ```config.json``` file.

2/ Paste the words that you want to search in ```words_data.txt``` file (One word per line).

## Docker
If you will use this library in a docker like environment, uncomment these lines in ```Login.py```:
```
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--window-size=1366,768')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)
```
and comment this line in ```Login.py```
```
driver = webdriver.Firefox()
```
## Some commands
```
import discord_driver 

info = discord_driver.DiscordDriver() 

info.get_user_info("<username>", params={"email":"<email>", "password":"<password>"})

info.get_posts_from_key("<word>", params={"email": "<email>", "password": "<password>" , "start_date": "<start date (dd/mm/yyyy)>", "end_date": "<end_date (dd/mm/yyyy)>", "game_name": "<game name>"}) 

info.get_posts_from_keys(<list of words>, params={"email": "<email>", "password": "<password>" , "start_date": "<start date (dd/mm/yyyy)>", "end_date": "<end_date (dd/mm/yyyy)>", "game_name": "<game name>"}) 

!discord-driver --help
```
