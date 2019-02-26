# Tournament Manager

This is a Python utility to help manage a tournament with ability to create, start and 
end a match and also to save save data generated during it and get it back too analyse 
the data. This is an extension to 
[Tournament Management](https://github.com/SanketRevankar/TournamentManagement) to support
more functionality. This utility is configured to use Google Datastore to fetch data 
related to the above mentioned web application and MySQL for data related to match servers.

## Requirements
 
### Register your application

- Register on [Google Cloud](https://console.cloud.google.com)
- Set-up Billing and create an account.
- Go to
  [Google Developers Console](https://console.developers.google.com/project)
  and create a new project. This will automatically enable an App
  Engine application with the same ID as the project.

- Enable the "Google Cloud Datastore API" under "APIs & auth > APIs."

### Python3 Libraries

- [Google Datastore Client API](https://pypi.org/project/google-cloud-datastore/) 
is used for [Google Datastore](https://cloud.google.com/datastore/) connection.
```
pip install google-cloud-datastore
```

- [Apache Libcloud](https://libcloud.apache.org/) is used for connecting 
[Google Compute Engine](https://cloud.google.com/compute/) instances to start/stop 
the servers.
```
pip install apache-libcloud
```

- [Pycryptodome](https://pypi.org/project/pycryptodome/) is used by libcloud for 
cryptographic libraries for connection
```
pip install pycryptodome
```

### Create a google cloud service account
- Open 
[Google Cloud Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
- Select your project
- Create a service account
- Enter any name for the account
- Add roles: Editor
- Create a Key in JSON format, it will download automatically.

### Enable Google Cloud API

Open 
[Compute Engine Instance Group Manager API](https://console.cloud.google.com/apis/api/replicapool.googleapis.com/overview) 
and enable this API

### Steam API 

Generate API Key from [Steam API Key](https://steamcommunity.com/dev/apikey)

### Creating a MySQL Database Server

- Run below commands to upgrade the current packages to the latest version.
```
$ sudo apt-get update 
$ sudo apt-get upgrade
```

- Configure MySQL PPA
```
$ wget http://repo.mysql.com/mysql-apt-config_0.8.9-1_all.deb
$ sudo dpkg -i mysql-apt-config_0.8.9-1_all.deb
```

- Install MySQL Server
```
$ sudo apt update 
$ sudo apt install mysql-server
```

- Secure MySQL Installation (Optional)
```
$ sudo systemctl restart mysql
$ sudo mysql_secure_installation
```

- Set global connection for DB
    - Open
    ```
    $ sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
    ```
    - Set bind address to the IP of the database server
    ```
    bind-address = 10.142.0.0 (Change it to IP of your server)
    ```
    - Restart MySQL Service
    ```
    $ sudo systemctl restart mysql
    ```
    
- Create a user to connect to DB
```
$ sudo mysql -u root -p
mysql> CREATE USER 'user'@'%' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'user'@'%'; 
```

## Configuration

Default configuration file is `resources/config.conf`

- **Database config**

Enter the database details, database whose name is mentioned may have not been created
```
USERNAME=username                      # Database User's Username
PASSWORD=password                      # Database User's Password
HOSTNAME=10.1.1.1                      # IP of Database Server
DATABASE=tm                            # Name of the Database
```

- **Project Config**

Enter the details of the account you created [here](#create-a-google-cloud-service-account)
```
SERVICE_ACCOUNT_EMAIL                   # Service Account Email id
SERVICE_ACCOUNT_KEY_PATH                # Service Account JSON Key Path
PROJECT_ID                              # Project ID of GCP Project
```
Enter the Key which you got from [here](#steam-api)
```
STEAM_API_KEY=key                       # Steam API Key
```
Adjust Maximum players in a team and number of matches that would be played in the tournament
```
MAX_PLAYERS=32                          # Maximum Players in a team
MAX_MATCHES=50                          # Number of matches
```

- **Folder paths**
```
FILES_HOME=C:/TourneyManager            # Base folder to store all data
LOGS_STARTING=${FILES_HOME}/Logs        # Folder to store all Logs
SCORE_STARTING=${FILES_HOME}/Score/     # Folder to store all Scores
HLTV_STARTING=${FILES_HOME}/Matches/ # Folder to store all Demos
IP_LOG_STARTING=${FILES_HOME}/IP_Logs/  # Folder to store all Logs
CERTIFICATES=Certificates               # Folder name for storing certificates
CONFIGS_RESULTS                         # Path where score logs are saved server
```

- **File Locations**
```
LOGGING_CONF=resources/logging.conf     # Path to logging config
STEAM_ID_LIST_TXT                       # Absolute path to resources/Steam_id_list.txt
STEAM_BANNED_USERS_FILE                 # Absolute path to resources/Data_bans.json
FONT_PATH                               # Absolute path to resources/TektonPro-Bold.otf
CERT_IMG_PATH                           # Path where the certificate template is stored
```

### Adding servers to Tourney Manager

- **Note:** Turning on servers remotely is only supported on servers hosted on Google
 Compute Engine

- Match servers are stored in `constants/MatchServers.py`

- Match server format in the above file: 
```
'1': {                                              # Id of the server
    sC.SERVER_NAME: 'Match Server #1',              # Name of the Match Server
    sC.SERVER_IP: '10.160.0.0:11111',               # Internal Compute Engine IP with Port
    sC.HLTV_SERVER_NAME: 'HLTV Server #1',          # Name of the HLTV Server
    sC.HLTV_IP: '10.160.0.0:11111',                 # Internal Compute Engine IP with Port 
    sC.INSTANCE_NAME: 'instance-cs-1',              # Instance name of Match Server
    sC.HLTV_NAME: 'instance-hltv',                  # Instance name of HLTV Server
    sC.PORT: '11111',                               # Port of the server
    sC.USERNAME: '2',                               # FTP Username of Match Server
    sC.PASSWORD: 'js8czih0',                        # FTP Password of Match Server
    sC.HLTV_USERNAME: '3',                          # FTP Username of HLTV Server
    sC.HLTV_PASSWORD: 'lgov8e18',                   # FTP Password of HLTV Server
},
```

## Functionality available

**Create a New Match**
- Used to Create a New Match.
- Inputs:

    - `Match Id` - Enter a Match Id, if repeated you will have a option to replace old 
    match or discard current
    - `Server Id` - Enter Server Id from the List on screen
    - `Team Id` - Enter Team Id from the List on screen
    
**Start Match**
- Used to Start a match which was created.
- Input:

    - `Match Id` - Enter Match Id from the List on screen
    
**End Match**
- Used to end a Match which was started.
- Inputs:

    - `Match Id` - Enter Match Id from the List on screen
    - `Number of Maps` - Number of maps played in that match
    - `Map` - Select a map from given list, you can change the list in constants/Config.py
    - `Map Score` - Enter the score for the match for teams as mentioned on the screen
    
**Get Match Data**

Get Different Data fetched from matches
- **Save Team-wise Player Stats to Excel File**
    - Save Team-wise Player Stats to Excel File, default to `team-wise_player-stats.xlsx`
    - Stats which are saved are:
        - `Matches` - Number of matches played
        - `Kills` - Total number of Kills
        - `Deaths` - Total number of Deaths
        - `HS` - Total number of Head shots
        - `Knifes` - Total number of Knife Kills
        - `Grenade` - Total number of Grenade Kills
        - `Suicide` - Total number of Suicides
        - `Plants` - Total number of Bomb Plants
        - `Defuses` - Total number of Bomb Defuses

- **Get Players with Highest Stats**
    - Get top players for all stats over all matches, stats can be either actual values of
    stats or average over number of matches played by that player 
    - This can be set in `constants/Config.py` using `AVERAGE_STATS_BY_MATCHES_PLAYED`, 
    if set to `True` average of stats will be used and if `False` actual values will be used,
    default is `False`
    - This will print Top players, the number of top players to print is set using
    `NUMBER_OF_TOP_PLAYERS` in `constants/Config.py`, default is `15`

- **Show Match Scores of all Matches**
    - Print map scores of all completed matches

- **Get IP matches for every Player**
    - Print IPs of players if IP of 2 or more players matches over the period of tournament

- **Get Connections of a Player by his Steam ID**
    - Print all connections and disconnections of a specific player
    - Input:
        - `Steam Id`: Steam Id of the player whose connections are required

- **Save Team Details (Players in a team) to Excel File**
    - Save list of players per team to Excel File, default location `team_details.xlsx`

- **Check VAC Bans of Players Registered**   
    - Check for VAC Bans of players using community Ids stored, default location
    `resources/Steam_id_list.txt`

**Get Player List**
- Get the Player List from Datastore and save it in `constants/PlayerDetails.py`

**Get Team List**
- Get the Team List from Datastore and save it in `constants/TeamDetails.py`

**Add Steam IDs to MySQL DB**
- Add all the players in `constants/PlayerDetails.py` to MySQL Database by Team Id 

**Create Participation certificates for players**
- Prints certificates for players using a template image without any name printed and
print names of the players

**Convert Steam Ids to community Ids for Ban check**
- Converts the Steam Ids of all players present in `constants/PlayerDetails.py` to 
Steam Community Ids and save it to a text file, default to `resources/Steam_id_list.txt`
- This step is needed for VAC Ban check for all players.

**Get Access list for captains**
- Print access strings for all captains
- You need to add captains manually to Team List at `constants/TeamDetails.py`
- Format for adding Captain Names:
```
    'Captain 1': '[Steam ID]',          # Steam Id of Captain 1
    'Captain 2': '[Steam ID]',          # Steam Id of Captain 2
    'Captain 1 Name': '[Name]',         # Name of Captain 1
    'Captain 2 Name': '[Name]',         # Name of Captain 2
```
- This needs to be added for each team separately
