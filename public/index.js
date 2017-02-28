
var x = 1, y = 1, num = 50;

document.getElementById('fib').innerHTML = '1';
for (var i = 0; i < num; i++) {
    document.getElementById('fib').innerHTML += ', ' + y;
    xOld = x;
    x = y;
    y += xOld;
};

var table_container = document.getElementById('table_container');

function dothing(elem, size, depth) {
    var table = document.createElement('div');
    table.className = 'table';
    for (var r=0; r < size; r++) {
        var row = document.createElement('div');
        row.className = 'trow';
        for (var c=0; c < size; c++){
            var cell = document.createElement('div');
            cell.className = 'tcell';
            if (depth > 1){
                dothing(cell, size, depth-1);
            }
            else{
                cell.innerHTML = ' ';
            }
            row.appendChild(cell);
        }
        table.appendChild(row);
    }
    elem.appendChild(table);
}

dothing(table_container, 3, 2);





/*
// Requires server (can use Python)
var r = new XMLHttpRequest();
r.open("GET", "/");
r.onreadystatechange = function () {
  if (r.readyState != 4 || r.status != 200) return;
  alert("Success: " + r.responseText);
};
r.send();
*/