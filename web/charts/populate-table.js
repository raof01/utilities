"use strict";

function readFileContent(files, onFileContentRead) {
    var fileReader = new FileReader();
    fileReader.onload = function (fileLoadedEvent) {
	onFileContentRead(fileLoadedEvent.target.result);
    }
    var fNum = files.length;
    fileReader.readAsText(files[0], "UTF-8")
}

var tableId = "data-table";

function removeTable(tableParent) {
    if (tableParent.children.length === 0) return;
    tableParent.removeChild(tableParent.children[0]);
}

function createTable() {
    var tParent = document.getElementById("data");
    removeTable(tParent);
    var table = document.createElement("TABLE");
    tParent.appendChild(table);
    return table;
}

function generateTables(contents) {
    if (contents === undefined || contents.length == 0)
	return;
    var lines = contents.split("\n");
    var table = createTable();
    populateTableData(table, lines);
}

function insertDataToTableAtRow(tableElem, i, line) {
    var words = line.split(",");
    var row = tableElem.insertRow(i);
    for (var w in words) {
	row.insertCell(w).innerHTML = words[w];
    }
}

function insertTableHead(tableElem, line) {
    var headers = line.split(",");
    var header = tableElem.createTHead();
    var row = header.insertRow(0);
    for (var w in headers){
	var cell = row.insertCell(w);
	cell.innerHTML = headers[w];
	cell.style = "background-color:black;color:white;font:bold;border:1px solid white;";
    }
}

function clearTable(tableElem) {
    var len = tableElem.rows.length;
    for (var i  = 0; i < len; ++i) {
	tableElem.deleteRow(-1);
    }
}

function populateTableData(tableElem, lines) {
    clearTable(tableElem);
    insertTableHead(tableElem, lines[0]);
    var len = lines.length;
    for (var i = 1; i < len; ++i){
	if (lines[i].length == 0)
	    continue;
	insertDataToTableAtRow(tableElem, i, lines[i]);
    }
}

