import bcrypt
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Database initial data
INITIAL_DATA = {
      'users': [
        {
            'name': 'admin',
            'lastname': 'admin',
            'email': 'admin@admin.com',
            'phone' : '123456789',
            'role_id' : 1,                
            'password': bcrypt_context.hash("123456")    
        }           
    ],
    'roles' : [
        {
            'role' : 'Owner',              
        },
        {
            'role' : 'SuperAdmin',              
        },
         
    ]
}


# This method receives a table, a connection and inserts data to that table.
def initialize_table(target, connection, **kw):
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        connection.execute(target.insert(), INITIAL_DATA[tablename])

