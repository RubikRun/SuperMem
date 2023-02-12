from interface.index_page import IndexPage
from data.database import Database

USERS_DATA_FILE = "data/users/users.txt"

database = Database()
database.read_users(USERS_DATA_FILE)

IndexPage.run(database.users)

database.write_users(USERS_DATA_FILE)