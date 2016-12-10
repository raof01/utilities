var Query = require('./mysql-query');

const SQL_SHOW_DB = 'SHOW DATABASES';

function queryResultToArray(rows) {
    let arr = new Array();
    rows.forEach(function (element) {
        arr.push(element['Database']);
    });
    return arr;
}

function query(q, fn) {
    console.log(`sql = ${SQL_SHOW_DB}`);
    q.query(SQL_SHOW_DB, function(err, rows, fields) {
        if (err) throw err;
        fn(queryResultToArray(rows));
    });
}

function postDatabases(req, fn) {
    let body = req.body;
    let q = new Query(body['host'], body['port'], body['user'], body['password']);
    query(q, fn);
    q.disconnect();
}

function getDatabases(req, fn) {
    let p = req.query;
    let q = new Query(p.host, parseInt(p.port), p.user, p.password);
    query(q, fn);
    q.disconnect();
}

module.exports = { postDatabases, getDatabases };
