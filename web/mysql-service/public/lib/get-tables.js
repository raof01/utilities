var Query = require('./mysql-query');

const SQL_SHOW_TABLES = 'SHOW TABLES IN ';
const FIELD_NAME = 'Tables_in_';

function queryResultToArray(dbName, rows) {
    let arr = new Array();
    rows.forEach(function (element) {
        arr.push(element[FIELD_NAME + dbName.toLowerCase()]);
    });
    return arr;
}

function query(q, dbName, fn) {
    console.log(`sql = ${SQL_SHOW_TABLES}${dbName}`);
    q.query(SQL_SHOW_TABLES + dbName, function(err, rows, fields) {
        if (err) throw err;
        fn(queryResultToArray(dbName, rows));
    });
}

function getTables(req, fn) {
    let p = req.query;
    let q = new Query(p.host, parseInt(p.port), p.user, p.password);
    query(q, p.dbName, fn);
    q.disconnect();
}

module.exports = getTables;
