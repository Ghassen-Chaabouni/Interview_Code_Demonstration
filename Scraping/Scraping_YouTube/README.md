# Scraping Youtube comments
Scraping Youtube comments based on the channel name and the name of the videos.

For more information about the implementation open the notebook ```test.ipynb```.

## Settings
#### Prepare the code_secret_client files
1/ Login into your gmail account.

2/ Go to https://console.cloud.google.com/

3/ Click on ```Select a project```.

4/ Click on ```NEW PROJECT```.

5/ Type the project name and click on ```CREATE```.

6/ Wait for the creation of the project.

7/ Click on the created project.

8/ Go to https://console.cloud.google.com/apis

9/ Click on ```OAuth Consent Screen```.

10/ Click on ```External```.

11/ Click on ```CREATE```.

12/ Type the application name, scroll down and click on ```Save```.

13/ Click on ```Credentials```.

14/ Click on ```CREATE IDENTIFIERS```.

15/ Click on ```ID client OAuth```.

16/ Click on ```Application type``` and select ```Desktop application```.

17/ Click on ```CREATE```.

18/ Click on ```OK```.

19/ Download the file ```Desktop client 1``` in ```ID clients OAuth 2.0```.

20/ Place the code_secret_client file in the config folder.

21/ Click on ```Dashboard```.

22/ Click on ```ENABLE APIS AND SERVICES```.

23/ Search for ```YouTube Data API v3``` and click on the search result.

24/ Click on ```ACTIVATE```.

25/(Optional) Repeat these steps 10 times (that's the limit).

26/(Optional) Create another account and repeate these steps.

27/ You need to be logged into your gmail account before running the script.

## Some commands
```
import youtube_driver 

info = youtube_driver.YoutubeDriver()

info.get_user_info("<channel name>")

info.get_posts_from_key("<video name>")

info.get_posts_from_keys(<list of video names>)

!youtube-driver --help
```