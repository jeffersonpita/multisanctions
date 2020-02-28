const express = require("express");
const app = express();
const connectDb = require("./src/connection");
const Sanctioned = require("./src/Sanctioned.model");
var stringSimilarity = require('string-similarity');

const PORT = 8080;

app.get("/search", async (req, res) => {

  let sanctioneds = [];
  if(req.query.name!=null && req.query.name!=""){

    let res2 = await Sanctioned.find( {
       "$or": [
         { "name": { "$regex": req.query.name, "$options": "i" } },
         { "aliases": { "$regex": req.query.name, "$options": "i" } }
       ]
     } );
    sanctioneds = res2.map( function(obj){
                  obj = obj.toObject();
                  obj['relevance'] = stringSimilarity.compareTwoStrings(req.query.name, obj['name']);
                  if(obj['aliases']!=null){
                    for(var i in obj['aliases']){
                      let rel1 = stringSimilarity.compareTwoStrings(req.query.name, obj['aliases'][i]);
                      if(rel1>obj['relevance'])
                        obj['relevance'] = rel1;
                    }
                  }
                  return obj;
                });
  }
  else {
    sanctioneds = await Sanctioned.find();
  }
  res.json(sanctioneds);
});

app.get("/create", async (req, res) => {
  var person = {
      name:"Saddam Russain",
      aliases: ["Saddan", "Iraki Leader"],
      is_person: true,
      sanctioned: true,
      list: "european"
      };

  await Sanctioned.create(person);
  res.json(person);
});

app.get("/status", async (req, res) => {
  res.json({ status: { "up":true } });
});

app.listen(PORT, function() {
  console.log(`Listening on ${PORT}`);

  connectDb().then(() => {
    console.log("MongoDb connected");
  });
});
