const mongoose = require("mongoose");

const sanctionedSchema = new mongoose.Schema({
  name: {
    type: String
  },
  aliases: {
    type: [String]
  },
  is_person: {
    type: Boolean
  },
  sanctioned: {
    type: Boolean
  },
  list: {
    type: String
  },
});

const Sanctioned = mongoose.model("Sanctioned", sanctionedSchema);

module.exports = Sanctioned;
