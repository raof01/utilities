var Query = require('./mysql-query');

const SQL_SHOW_COLUMNS = 'SHOW COLUMNS IN ';
const SQL_USE_DB = 'USE ';
const FIELD = 'Field';

function queryResultToArray(tableName, rows) {
    let arr = new Array();
    rows.forEach(function (element) {
        arr.push(element[FIELD]);
    });
    console.log(arr);
    return arr;
}

function query(q, dbName, tableName, fn) {
    console.log(`sql = ${SQL_USE_DB}${dbName}`);
    q.query(SQL_USE_DB + dbName, (err, rows, field) => {
        if (err) throw err;
    });
    console.log(`sql = ${SQL_SHOW_COLUMNS}${tableName}`);
    q.query(SQL_SHOW_COLUMNS + tableName, function(err, rows, fields) {
        if (err) throw err;
        fn(queryResultToArray(tableName, rows));
    });
}

function getColumns(req, fn) {
    let p = req.query;
    let q = new Query(p.host, parseInt(p.port), p.user, p.password);
    query(q, p.dbName, p.tableName, fn);
    q.disconnect();
}

module.exports = getColumns;
