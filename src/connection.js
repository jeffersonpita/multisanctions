
const mongoose = require("mongoose");

const Sanctioned = require("./Sanctioned.model");

const connection = "mongodb://mongo:27018/mongo-test";

const connectDb = () => {
  return mongoose.connect(connection);
};

module.exports = connectDb;
