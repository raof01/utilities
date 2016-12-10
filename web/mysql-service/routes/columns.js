var express = require('express');
var router = express.Router();
var getColumns = require('../public/lib/get-columns');

/* GET columns listing. */
router.get('/', function(req, res, next) {
    getColumns(req, function(result) {
        res.send(result);
    });
});

module.exports = router;
