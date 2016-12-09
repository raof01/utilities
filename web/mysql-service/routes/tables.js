var express = require('express');
var router = express.Router();
var getTables = require('../public/lib/get-tables');

/* GET tables listing. */
router.get('/', function(req, res, next) {
    getTables(req, function(result) {
        res.send(result);
    });
});

module.exports = router;
