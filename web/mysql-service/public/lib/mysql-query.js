"use restrict";

var mysql = require('mysql');

var MySqlQuery = function (host, port, name, passwd) {
    this.conn = mysql.createConnection({
        host: host,
        port: port,
        user: name,
        password: passwd
    });
    this.conn.connect();

    this.disconnect = function () {
        this.conn.end();
    }
    this.query = function (sql, fn) {
        this.conn.query(sql, function (err, rows, fields) {
            if (err) throw err;
            fn(err, rows, fields);
        });
    }
}

module.exports = MySqlQuery;