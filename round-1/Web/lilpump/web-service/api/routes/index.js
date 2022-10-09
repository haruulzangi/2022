var express = require("express");

var router = express.Router();
var DataBaseHandler = require("../config/DataBaseHandler");
var dataBaseHandler = new DataBaseHandler();

var connection = dataBaseHandler.createConnection();

router.get("/", function (req, res, next) {
  connection.query("SELECT * FROM SONG;", function (error, result, fields) {
    if (error) {
      res.status(500).send({
        status: "Error",
        message: "Internal Server Error",
      });
    } else if (result.length == 0) {
      res.status(404).send({
        status: "ERROR",
        message: "User does not exist",
      });
    } else {
      res.status(202);
      res.render("index.jade", { data: result });
    }
  });
});

router.ws("/ws", function (ws, req) {
  ws.on("message", function (msg) {
    if (msg == "__ping__") {
      ws.send("__pong__");
      return;
    }
    try {
      eJson = JSON.parse(msg);
      songname = eJson.songname;
      console.log(songname);
      query = `SELECT * FROM SONG where SongName like "${songname}";`;
      console.log(query);
      connection.query(query, function (error, result, fields) {
        if (error) {
          ws.send('{"message": "<span class=red>Song not found.</span>"}');
        } else if (result.length == 0) {
          ws.send('{"message": "<span class=red>Song not found.</span>"}');
        } else {
          var rows = JSON.parse(JSON.stringify(result[0]));
          ws.send(
            '{"message": "<span class=lime>Song ID: ' +
              rows.SongId +
              " Song name: " +
              rows.SongName +
              '</span>"}'
          );
        }
      });
    } catch (e) {
      ws.send('{"message":"invalid command!"}');
    }
  });
});

module.exports = router;
