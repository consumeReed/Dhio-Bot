## About The Project

The Dhio Bot is a Discord Bot that keeps inventory of loot from Dhiothu from Celtic Heroes. 


### Built With and Using

* Python
* Discord Python
* MongoDB


### Getting Started and Requirements
Dependencies and Requirements
* Requires Python 3.8 or higher
* Requires a MongoDB connection
* Requires a unique Discord Bot Authentication Token

Creating database, downloading assets, and starting bot
* Run makedb.py and then fix_db.py with a valid MongoDB database connection
* Run get_items.py to download each Dhiothu loot image locally
* Change the .env file to a valid Discord Bot Authentication Token
* Run bot.py to start bot

### Usage
The Dhiothu Bot commands all use ! before each command. Use help while running for list of all commands.

General usage
* find - query database with item name or class
* show/find - retrieve image of item based on item id
* kill - simulates a Dhiothu kill

Admin
* update - Modify individual item quantities based on id

### Roadmap

-  Fixes to text output
-  Send message to embedded message in Discord channels
-  Allow for recent Dhiothu kills to be posted, viewed, and modified
-  Add more users to have admin privileges


### Status

The project is currently under development. You can find current releases at the releases tab. If downloading from
releases, ensure database and images are created and run bot.exe.

