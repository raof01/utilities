var express = require('express');
var router = express.Router();
var mysql = require('mysql');

/* GET users listing. */
router.get('/', function(req, res, next) {
  let conn = mysql.createConnection(
    {
      host: 'localhost',
      port: 8889,
      user: "test",
      password: "test123",
    }
  );
  conn.connect();
  conn.query('SELECT 1 + 3 AS solution', function(err, rows, fields) {
    if (err) throw err;
 
  res.send(`The solution is: ${rows[0].solution}`);
});
 
conn.end();
});

module.exports = router;
