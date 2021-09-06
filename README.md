# Slowify
Get songs from a specified Spotify playlist URL and create a slowed and reverbed version of the songs in a Youtube Playlist.

## Prequesites
Install these using pip

`pip install --upgrade google-api-python-client`

`pip install --upgrade google-auth-oauthlib google-auth-httplib2`

`pip install spotipy`

`pip3 install youtube-search-python`

## How to get it to work
1) Go to the Google Developer's Console and create a new project

3) Go to library, search for "**youtube data api v3**" and enable the api for your project

4) Click the three lines on the top left, click "**APIs and Services**" and then click "**OAUTH Consent Screen**" in the drop-down menu

5) Set the user type to external and click create
 
6) Fill out the next section, you only need to fill out the input fields with red asterisks, you can skip the rest

7) **THIS IS THE MOST IMPORTANT PART**: click the add scope button and add the scope with the user-facing description of "**Manage your youtube account**", it should end in "**/auth/youtube**" and be part of the **Youtube Data API v3**

8) On the test users page, click add users and type in the email address that you used to create the project with

9) Click the credentials tab on the side

10) Click create credentials at the top and click **OAUTH Client ID**

11) Under the application type dropdown, select **Desktop App** and type any name you want

12) Download the JSON file, rename it to client_secret and save it to the directory the slowify python file is in.
