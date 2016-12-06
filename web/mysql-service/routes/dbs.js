var express = require('express');
var router = express.Router();
var Query = require('../public/lib/mysql-query');

/* GET dbs listing. */
router.get('/', function(req, res, next) {
  let q = new Query('localhost', 8889, "test", "test123");
  q.query('SHOW DATABASES', function(err, rows, fields) {
    let arr = new Array();
    rows.forEach(function(element) {
        arr.push(element['Database']);
    });
  res.send(`${arr}`);
});

q.disconnect();
});

module.exports = router;
