var express = require('express');
var router = express.Router();
var getDbs = require('../public/lib/get-dbs');

/* GET dbs listing. */
/*
 * curl -i -H 'content-type: application/json' -X POST -d '{"host": "localhost", "port": 8889, "user": "test", "password": "test123"}' http://localhost:3000/dbs
 */

router.post('/', function(req, res, next) {
    getDbs.postDatabases(req, function(result) {
        res.send(result)
    });
});

router.get('/', function(req, res, next) {
    getDbs.getDatabases(req, function(result) {
        res.send(result);
    });
});

module.exports = router;
