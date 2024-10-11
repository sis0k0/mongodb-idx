const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const { Database, applySchemaValidation } = require('./database');
const { databaseConfiguration } = require('./config');

/**
 * Connection URI for a MongoDB instance. By default, this the local instance running in Project IDX.
 * See https://docs.mongodb.com/drivers/node/ for more details.
 */
const uri = process.env.MONGODB_CONNECTION_STRING || databaseConfiguration.uri;
const databaseName = databaseConfiguration.databaseName;
const collectionName = databaseConfiguration.collectionName;

/**
 * Sample validation schema for the 'users' collection. Replace with your own collection schemas.
 * Schema validation is applied by the database server and is optional when creating a collection.
 * See https://www.mongodb.com/docs/manual/core/schema-validation/ for more details.
 */
const usersCollectionSchema = {
  $jsonSchema: {
    bsonType: 'object',
    title: 'User Document Validation',
    required: ['name', 'email'],
    properties: {
      name: {
        bsonType: 'string',
        description: '\'name\' must be a string and is required'
      },
      email: {
        bsonType: 'string',
        pattern: '^.+@.+$',
        description: '\'email\' must be a valid email address and is required'
      },
      age: {
        bsonType: 'int',
        minimum: 0,
        description: '\'age\' must be a non-negative integer if the field exists'
      }
    }
  }
};

Database.connectToDatabase(uri).then(async databaseClient => {
  const db = databaseClient.db(databaseName);
  await applySchemaValidation(db, collectionName, usersCollectionSchema);

  const app = express();
  // Set up a middleware to parse JSON data in the request body
  app.use(bodyParser.json());
  app.use(cors());

  // Define routes for the 'users' collection
  const userRoutes = require('./user.routes');
  app.use('/users', userRoutes);

  app.use('/', (_req, res) => res.status(200).send('API v1.0 is running...'));

  // Start the server
  const port = 3000;
  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
  });
});
