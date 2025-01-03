# Welcome to Chess Tournaments schedule 

## In this programme we will be able to organize the Tournemant of chees by being able to operate and save the next datas.
### Creating new player
### Checking existing players
### Checking existing tournaments
### Creat player list for specific tournament
### Organizing round games and adding game result
### Creating tournament
### Creating report.


#### Creating our envirenment.
Checking the version of our pip
```bash
pip -V
# if we don't pip or we have an older version than 24.0
# we can install it.
python3 -m pip install 'requests==24.0'
# or upgrading it
python3 -m pip install --upgrade pip
```
Checking or installing git
```bash
git --version
# If it is not installed:
sudo apt install git-all
```
Once the git is installed we can download the github repository
You can go to the github repository page
```html
https://github.com/gltwodotlineci/schedule_chess_games
```

You have two options to clone the project. HTTPS or SSH

HTTPS:
```bash
https://github.com/gltwodotlineci/schedule_chess_games
```
```ssh
git@github.com:gltwodotlineci/schedule_chess_games
```
> If you have allredy saved your public RSA key to github you can use the ssh method. if not the http


You can clone the project on your local folder by executing
```bash
# SSH
git clone git@github.com:gltwodotlineci/schedule_chess_games
# Or HTTPS
git clone https://github.com/gltwodotlineci/schedule_chess_games
```

Creating the virtual envirenment and installing dependences
```bash
cd books_to_scrap
python3 -m venv ./virtual_schedule_proj
# Activating the virtual envirenment
source ~/virtual_schedule_proj/bin/activate
# installing libraries
python3 -m pip install -r requirements.txt
```

To enter to your sub folder of execution, you write.
```bash
cd schedule_chess_game
```
And to execute the programme you shall just write the next command.
```bash
python main.py
```
