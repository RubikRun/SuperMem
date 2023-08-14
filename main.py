from interface.index_page import IndexPage
from interface.home_page import HomePage
from data.database import Database

USERS_DATA_FILE = "data/users/users.txt"

database = Database()
database.load_dictionaries()
database.load_users(USERS_DATA_FILE)

languages = database.get_all_languages()
IndexPage.run(database.users, database)
#home_page = HomePage(database.users[1])
#home_page.run(database)

database.export_users(USERS_DATA_FILE)

# For now do not export dictionaries back to their files,
# because there's no functionality that changes a dictionary,
# and because empty lines are not handled yet and they are lost when exporting a dictionary
#database.export_dictionaries()