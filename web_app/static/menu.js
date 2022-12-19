const games = document.getElementById("games");

for (var i = 0, row; (row = games.rows[i]); i++) {
  for (var j = 0, col; (col = row.cells[j]); j++) {
    if (col.textContent == "True") {
      console.log(col.textContent);
      col.style.color = "green";
    } else if (col.textContent == "False") {
      col.style.color = "red";
    }
  }
}
