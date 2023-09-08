//sorted_topics.js

  function make_elements( topic, listItem ){
    const nameElement = document.createElement("h4");
    let stringContent = `${topic.title}`
    nameElement.textContent = stringContent;
          
    const summaryElement = document.createElement("div");
    summaryElement.textContent = topic.summary;

    const discussion_dateElement = document.createElement("div");
    if( topic.discussion_date != 'Mon 01 Jan 1'){
      discussion_dateElement.textContent = topic.discussion_date + ' ' + topic.discussion_time;
    }

    const authorElement = document.createElement("div");
    authorElement.authorContent = topic.author_fullname

    const linkElement = document.createElement('a');
    linkElement.href = `${topic.url}`;
    linkElement.classList.add('btn');
    //linkElement.classList.add('dac');
    linkElement.textContent = 'Detail and Comments'
    linkElement.style.display = 'inline' // 'inline' to show or 'none' to remove

    const newlineElement = document.createElement("br");

    const hrElement = document.createElement("hr");

    listItem.append(
      hrElement,
      nameElement,
      summaryElement,
      authorElement,
      discussion_dateElement,
      linkElement,
      newlineElement,
    );
  }


  fetch("/api/sorted_topics")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error, status = ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      //console.log(data)
      for (const topic of data.future_topics) {
        const listItem = document.createElement("li"); 
        make_elements( topic, listItem )
        future_topics.appendChild(listItem);
      }
      for (const topic of data.past_topics) {
        const listItem = document.createElement("li"); 
        make_elements( topic, listItem )
        past_topics.appendChild(listItem);
      }
      for (const topic of data.proposed_topics) {
        const listItem = document.createElement("li"); 
        make_elements( topic, listItem )
        proposed_topics.appendChild(listItem);
      }
    })
    .catch((error) => {
      const p = document.createElement("p");
      p.appendChild(document.createTextNode(`Error: ${error.message}`));
      document.body.insertBefore(p, myList);
    });