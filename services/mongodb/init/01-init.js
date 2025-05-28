// Create application database and user
db = db.getSiblingDB('starter_kit');

// Create application user
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    { role: 'readWrite', db: 'starter_kit' },
    { role: 'dbAdmin', db: 'starter_kit' }
  ]
});

// Create collections with schema validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['email', 'hashed_password', 'is_active'],
      properties: {
        email: {
          bsonType: 'string',
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
        },
        hashed_password: {
          bsonType: 'string'
        },
        full_name: {
          bsonType: 'string'
        },
        is_active: {
          bsonType: 'bool'
        },
        is_superuser: {
          bsonType: 'bool'
        },
        created_at: {
          bsonType: 'date'
        },
        updated_at: {
          bsonType: 'date'
        }
      }
    }
  }
});

// Create indexes
db.users.createIndex({ 'email': 1 }, { unique: true });
db.users.createIndex({ 'is_active': 1 }); 