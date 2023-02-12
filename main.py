from interface.index_page import IndexPage
from interface.home_page import HomePage
from data.database import Database

USERS_DATA_FILE = "data/users/users.txt"

database = Database()
database.load_dictionaries()
database.load_users(USERS_DATA_FILE)

languages = database.get_all_languages()
#IndexPage.run(database.users, database)
home_page = HomePage(database.users[1])
home_page.run(database)

database.export_users(USERS_DATA_FILE)
database.export_dictionaries()