function makeRequest(url, callback) {
  var r = new XMLHttpRequest();
  r.open("GET", url, true);
  r.onreadystatechange = function () {
    if (r.readyState != 4 || r.status != 200) return;
    alert(r.responseText);
  };
  r.send();
}
