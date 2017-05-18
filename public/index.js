
var x = 1, y = 1, num = 50;

document.getElementById('fib').innerHTML = '1';
for (var i = 0; i < num; i++) {
    document.getElementById('fib').innerHTML += ', ' + y;
    xOld = x;
    x = y;
    y += xOld;
};


newGameButton = document.getElementById('new_game');
newGameButton.onclick = function(e){
    size = document.getElementById('size').value;
    depth = document.getElementById('depth').value;
    id = 1;
    location = 'create_board?size=' + size
                      + '&depth=' + depth + '&id=' + id;
};
