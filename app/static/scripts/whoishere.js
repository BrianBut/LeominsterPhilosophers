//whoishere.js
  function whoishere(){
    fetch("/api/usercount")
  .then(response => {
    // indicates whether the response is successful (status code 200-299) or not
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`)
    }
    return response.json()
  })
  .then(data => {
    console.log(data.count)
    //document.getElementById("usercount").innerHTML = data.count;
  })
  .catch(error => console.log(error))
  }
  
  function myFunction() {
    setInterval( function() {whoishere()}, 10000);
  }
  
  const ping_url = "/api/usercount"
  
  myFunction( ping_url ) 
  
