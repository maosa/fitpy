# Add the following two lines into your .bash_profile file
# This prevents us from hard-coding variables into our scripts
# export EMAIL_USER="YourEmail@gmail.com"
# export EMAIL_PASS="YourPassword"

import os

db_user = os.environ.get('EMAIL_USER')
db_password = os.environ.get('EMAIL_PASS')

print(db_user)
print(db_password)
