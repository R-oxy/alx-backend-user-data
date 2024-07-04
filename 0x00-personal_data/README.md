# 0x00. Personal data

## Resources
Read or watch:
- [What Is PII, non-PII, and Personal Data?](https://link/to/resource)
- [logging documentation](https://docs.python.org/3/library/logging.html)
- [bcrypt package](https://pypi.org/project/bcrypt/)
- [Logging to Files, Setting Levels, and Formatting](https://link/to/resource)

## Learning Objectives
By the end of this project, you should be able to explain to anyone, without the help of Google:
- Examples of Personally Identifiable Information (PII)
- How to implement a log filter that will obfuscate PII fields
- How to encrypt a password and check the validity of an input password
- How to authenticate to a database using environment variables

## Requirements
- All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All your files should end with a new line
- The first line of all your files should be exactly `#!/usr/bin/env python3`
- A README.md file, at the root of the folder of the project, is mandatory
- Your code should use the pycodestyle style (version 2.5)
- All your files must be executable
- The length of your files will be tested using `wc`
- All your modules should have documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
- All your classes should have documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
- All your functions (inside and outside a class) should have documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)' and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
- A documentation is not a simple word, it’s a real sentence explaining the purpose of the module, class, or method (the length of it will be verified)
- All your functions should be type annotated

## Tasks

### 0. Regex-ing
Write a function called `filter_datum` that returns the log message obfuscated:

Arguments:
- `fields`: a list of strings representing all fields to obfuscate
- `redaction`: a string representing by what the field will be obfuscated
- `message`: a string representing the log line
- `separator`: a string representing by which character is separating all fields in the log line (message)

The function should use a regex to replace occurrences of certain field values. `filter_datum` should be less than 5 lines long and use `re.sub` to perform the substitution with a single regex.

Example:
```python
#!/usr/bin/env python3
"""
Main file
"""

filter_datum = __import__('filtered_logger').filter_datum

fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))
```

```bash
$ ./main.py
name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
```

### 1. Log formatter
Copy the following code into `filtered_logger.py`:
```python
import logging

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
```

Update the class to accept a list of strings `fields` constructor argument. Implement the `format` method to filter values in incoming log records using `filter_datum`. Values for fields in `fields` should be filtered.

Example:
```python
#!/usr/bin/env python3
"""
Main file
"""

import logging
import re

RedactingFormatter = __import__('filtered_logger').RedactingFormatter

message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
print(formatter.format(log_record))
```

```bash
$ ./main.py
[HOLBERTON] my_logger INFO 2019-11-19 18:24:25,105: name=Bob; email=***; ssn=***; password=***;
```

### 2. Create logger
Implement a `get_logger` function that takes no arguments and returns a `logging.Logger` object. The logger should be named "user_data" and only log up to `logging.INFO` level. It should not propagate messages to other loggers. It should have a `StreamHandler` with `RedactingFormatter` as formatter.

Create a tuple `PII_FIELDS` constant at the root of the module containing the fields from `user_data.csv` that are considered PII. `PII_FIELDS` can contain only 5 fields - choose the right list of fields that are considered “important” PIIs or information that you must hide in your logs. Use it to parameterize the formatter.

Example:
```python
#!/usr/bin/env python3
"""
Main file
"""

import logging

get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

print(get_logger.__annotations__.get('return'))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))
```

```bash
$ ./main.py
<class 'logging.Logger'>
PII_FIELDS: 5
```

### 3. Connect to secure database
Database credentials should NEVER be stored in code or checked into version control. One secure option is to store them as environment variables on the application server.

In this task, you will connect to a secure Holberton database to read a `users` table. The database is protected by a username and password that are set as environment variables on the server named `PERSONAL_DATA_DB_USERNAME` (set the default as “root”), `PERSONAL_DATA_DB_PASSWORD` (set the default as an empty string) and `PERSONAL_DATA_DB_HOST` (set the default as “localhost”).

The database name is stored in `PERSONAL_DATA_DB_NAME`.

Implement a `get_db` function that returns a connector to the database (`mysql.connector.connection.MySQLConnection` object).

Example:
```bash
$ cat main.sql
-- setup mysql server
-- configure permissions
CREATE DATABASE IF NOT EXISTS my_db;
CREATE USER IF NOT EXISTS root@localhost IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON my_db.* TO 'root'@'localhost';

USE my_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    email VARCHAR(256)
);

INSERT INTO users(email) VALUES ("bob@dylan.com");
INSERT INTO users(email) VALUES ("bib@dylan.com");
```

```bash
$ cat main.sql | mysql -uroot -p
Enter password: 
$ echo "SELECT COUNT(*) FROM users;" | mysql -uroot -p my_db
Enter password: 
2
$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db

db = get_db()
cursor = db.cursor()
cursor.execute("SELECT COUNT(*) FROM users;")
for row in cursor:
    print(row[0])
cursor.close()
db.close()
```

```bash
$ PERSONAL_DATA_DB_USERNAME=root PERSONAL_DATA_DB_PASSWORD=root PERSONAL_DATA_DB_HOST=localhost PERSONAL_DATA_DB_NAME=my_db ./main.py
2
```

### 4. Read and filter data
Implement a `main` function that takes no arguments and returns nothing. The function will obtain a database connection using `get_db` and retrieve all rows in the `users` table and display each row under a filtered format.

Example:
```bash
$ cat main.sql
-- setup mysql server
-- configure permissions
CREATE DATABASE IF NOT EXISTS my_db;
CREATE USER IF NOT EXISTS root@localhost IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON my_db.* TO root@localhost;

USE my_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    name VARCHAR(256), 
    email VARCHAR(256), 
    phone VARCHAR(16),
    ssn VARCHAR(16), 
    password VARCHAR(256),
    ip VARCHAR(64), 
    last_login TIMESTAMP,
    user_agent VARCHAR(512)
);

INSERT INTO users(name, email, phone, ssn, password, ip, last_login, user_agent) VALUES ("Marlene Wood","hwestiii@att.net","(473)

 432-2152","261-72-6783","njTG!9vj", "123.123.123.123", "2019-11-14 06:14:24","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.3 Safari/601.6.17");
```

```bash
$ cat main.sql | mysql -uroot -p
Enter password: 
$ echo "SELECT * FROM users;" | mysql -uroot -p my_db
Enter password: 
Marlene Wood	hwestiii@att.net	(473) 432-2152	261-72-6783	njTG!9vj	123.123.123.123	2019-11-14 06:14:24	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.3 Safari/601.6.17
$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""

import logging
import mysql.connector
from os import getenv

get_db = __import__('filtered_logger').get_db
filter_datum = __import__('filtered_logger').filter_datum
RedactingFormatter = __import__('filtered_logger').RedactingFormatter
PII_FIELDS = __import__('filtered_logger').PII_FIELDS


def main():
    """ Obtain a database connection and retrieve rows in users table """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = "name={}; email={}; phone={}; ssn={}; password={}; ip={}; last_login={}; user_agent={};".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        print(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
```

```bash
$ PERSONAL_DATA_DB_USERNAME=root PERSONAL_DATA_DB_PASSWORD=root PERSONAL_DATA_DB_HOST=localhost PERSONAL_DATA_DB_NAME=my_db ./main.py
name=Marlene Wood; email=hwestiii@att.net; phone=(473) 432-2152; ssn=261-72-6783; password=njTG!9vj; ip=123.123.123.123; last_login=2019-11-14 06:14:24; user_agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.3 Safari/601.6.17;
```

### 5. Encrypting passwords
User passwords should NEVER be stored in plain text in a database.

Implement a `hash_password` function that expects one string argument name `password` and returns a salted, hashed password, which is a byte string.

Use the `bcrypt` package to perform the hashing.

Example:
```python
#!/usr/bin/env python3
"""
Main file
"""

hash_password = __import__('encrypt_password').hash_password

password = "Hello Holberton"
print(hash_password(password))
```

```bash
$ ./main.py
b'$2b$12$KPOs0fQ8iVozI5ywR8F29O5yHVd7aZq4B7n4aVtP5JDIpM5c8BJLm'
```

### 6. Check valid password
Implement an `is_valid` function that expects 2 arguments and returns a boolean. The first argument is a `hashed_password`, which is a byte string, and the second is a `password`, which is a string. Use `bcrypt` to validate that the provided password matches the hashed password.

Example:
```python
#!/usr/bin/env python3
"""
Main file
"""

hash_password = __import__('encrypt_password').hash_password
is_valid = __import__('encrypt_password').is_valid

password = "Hello Holberton"
hashed_password = hash_password(password)
print(hashed_password)
print(is_valid(hashed_password, password))
```

```bash
$ ./main.py
b'$2b$12$KPOs0fQ8iVozI5ywR8F29O5yHVd7aZq4B7n4aVtP5JDIpM5c8BJLm'
True
```