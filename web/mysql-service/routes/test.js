var express = require('express');
var router = express.Router();
var Query = require('../public/lib/mysql-query');

/* GET test listing. */
router.get('/', function(req, res, next) {
  var query = new Query('localhost',8889,"test","test123");
  query.disconnect();
  res.send('disconnect');
});

module.exports = router;
