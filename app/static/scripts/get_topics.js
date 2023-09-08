//get_topics.js

function topics(){
  fetch( topics_url )
  .then(response => response.json())
  .then(json => console.log(JSON.stringify(json)))
}

const topics_url = "/api/topics"


app/static/topics.js