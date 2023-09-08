//keepAlive.js

function ping(u){
  fetch( u )
  .then(response => response.json())
  .then(json => console.log(JSON.stringify(json)))
}

function myFunction( url ) {
  const u = url
  setInterval( function() {ping(u)}, 102300);
}

const id = 1
const ping_url = "/api/ping/1"

myFunction( ping_url ) 

