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
	s[i] = {x: (records[i].recordDate - records[i-1].recordDate) / 1000 / 3600 / 24 + s[i-1].x, y: records[i].value};
	
    }
    return s;
}

function plot(contents) {
    addRecords(contents);
    
    var data = {
//	labels: getLabels(),
	series: [
	    getSeries()
	]
    };
    new Chartist.Line('.ct-chart', data, {
	axisX: {
	    type: Chartist.AutoScaleAxis,
	    onlyInteger: true
	}
    });
}
