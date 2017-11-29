"use strict";

function Record(strDate, val) {
    this.recordDate = new Date(strDate);
    this.value = parseFloat(val);
}

var records = [];

function addRecord(strDate, val) {
    records[records.length] = new Record(strDate, val);
}

function clearRecord() {
    records = [];
}

function addRecords(contents) {
    clearRecord();
    var lines = contents.split("\n");
    var len = lines.length;
    for (var i = 1; i < len; ++i) {
        if (!lines[i]) { continue; }
	var words = lines[i].split(",");
	addRecord(words[0], words[1]);
    }
}

function getLabels() {
    var l = [0];
    var len = records.length;
    for (var i = 1; i < len; ++i) {
	l[i] = (records[i].recordDate - records[i-1].recordDate) / 1000 / 3600 / 24 + l[i-1];
    }
    return l;
}

function getSeries() {
    var s = [{x: 0, y:records[0].value}];
    var len = records.length;
    for (var i = 1; i < len; ++i) {
	s[i] = {x: daysBetween(records[i].recordDate, records[i-1].recordDate) + s[i-1].x, y: records[i].value};
	
    }
    return s;
}

function daysBetween(endDate, startDate) {
    return (endDate - startDate) / 1000 / 3600 / 24;
}

function getAvgSeries() {
    var s = [{x: 0, y: records[0].value}];
    var len = records.length;
    for (var i = 1; i < len; ++i) {
        var days = daysBetween(records[i].recordDate, records[i-1].recordDate);
        // var sLen = s.length;
        var avg = (records[i].value - records[i-1].value) / days;
        s[i] = {x: days + s[i-1].x, y: avg};
        if (i === 1) s[0].y = avg;
    }
    var s1 = [];
    for (var i = 0; i < len; ++i) {
        s1[i] = { x: s[i].x, y: s[i].y };
    }
    var allAvg = (records[len - 1].value - records[0].value) / s[len - 1].x;
    s1.map(e => e.y = allAvg);
    return [s, s1];
}

function getAvgLabels(arr) {
    return arr.map(e => e.x);
}

function getAvgs(arr) {
    return arr.map(e => e.y);
}

