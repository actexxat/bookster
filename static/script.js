const selectBtns = document.querySelectorAll('.select');
let serials = document.querySelectorAll(".serial")
let removeBTNS = document.querySelectorAll('.remove')

let s = 0
serials.forEach(cell =>{
    s = s + 1;
    cell.textContent = s ;
})

removeBTNS.forEach(rmv =>{
    rmv.addEventListener('click', function(){
        let titleRmv = this.parentElement.parentElement.children[2].textContent;
        send_rmv = {
            title:titleRmv
            }
        sendToRemove(send_rmv)

    })
})


console.log(serials)
selectBtns.forEach(btn => {
  btn.addEventListener('click', function() {
    let bookCover = this.parentElement.children[0].firstChild.src.trim();
    let bookTitle = this.parentElement.children[1].children[0].textContent.trim();
    let pubYear = this.parentElement.children[1].children[1].textContent.trim();
    let bookAuthor = this.parentElement.children[1].children[2].textContent.trim();
    send_data = {
      title:bookTitle,
      author:bookAuthor,
      year:pubYear,
      cover:bookCover
      }
    sendDataToFlask(send_data)
})
});

function sendToRemove(titleToRemove){
    fetch('/remove', {
    method: 'POST', // Use POST for sending data
    headers: {
      'Content-Type': 'application/json' // Specify JSON data format
    },
    body: JSON.stringify(titleToRemove) // Convert data to JSON string
  })


}

function sendDataToFlask(data) {
  fetch('/results', {
    method: 'POST', // Use POST for sending data
    headers: {
      'Content-Type': 'application/json' // Specify JSON data format
    },
    body: JSON.stringify(data) // Convert data to JSON string
  })


}
