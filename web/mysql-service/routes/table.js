var express = require('express');
var router = express.Router();
var getValues = require('../public/lib/select');

/* GET columns listing. */
router.get('/', function(req, res, next) {
    getValues(req, function(result) {
        res.send(result);
    });
});

module.exports = router;
