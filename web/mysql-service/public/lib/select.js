var Query = require('./mysql-query');

const SQL_SELECT = 'SELECT ';
const SQL_FROM = ' FROM '

function queryResultToArray(tableName, rows) {
    let arr = new Array();
    rows.forEach(function (element) {
        arr.push(element);
    });
    return arr;
}

function query(q, dbName, tableName, fields, fn) {
    console.log(`sql = ${SQL_SELECT}${fields}${SQL_FROM}${tableName}`);
    q.query(SQL_SELECT + fields + SQL_FROM + dbName + '.' + tableName, function(err, rows, fields) {
        if (err) throw err;
        fn(queryResultToArray(tableName, rows));
    });
}

function getValues(req, fn) {
    let p = req.query;
    let q = new Query(p.host, parseInt(p.port), p.user, p.password);
    query(q, p.dbName, p.tableName, p.fields, fn);
    q.disconnect();
}

module.exports = getValues;
