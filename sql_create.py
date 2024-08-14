import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="lyborkiixd",
    database="linguine"
)

sqlcursor = db.cursor()

create_users = """
CREATE TABLE users
(
    id INT AUTO_INCREMENT, 
    user TEXT NOT NULL, 
    password TEXT NOT NULL, 
    PRIMARY KEY (id)
);
"""

create_texts = """
CREATE TABLE texts
(
    id INT AUTO_INCREMENT,
    text MEDIUMTEXT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

        
sqlcursor.execute(create_users)
sqlcursor.execute(create_texts)