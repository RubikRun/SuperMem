from interface.index_page import IndexPage
from data.database import Database

USERS_DATA_FILE = "data/users/users.txt"

database = Database()
database.load_users(USERS_DATA_FILE)
database.load_dictionaries()

IndexPage.run(database.users)

database.export_users(USERS_DATA_FILE)
database.export_dictionaries()