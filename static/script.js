const selectBtns = document.querySelectorAll('.select');
let removeBTNS = document.querySelectorAll('.remove')
window.addEventListener("load", (event) => {
  rankSerials()
});
removeBTNS.forEach(rmv =>{
    rmv.addEventListener('click', function(){
        let titleRmv = this.parentElement.parentElement.children[2].textContent;
        send_rmv = {
            title:titleRmv
            }
        sendToRemove(send_rmv)
        this.parentElement.parentElement.remove()
        rankSerials()


    })
})

function rankSerials(){
    let serials = document.querySelectorAll(".serial")
    let s = 0
    serials.forEach(cell =>{
    s = s + 1;
    cell.textContent = s ;
})

}
selectBtns.forEach(btn => {
  btn.addEventListener('click', function() {
    let bookCover = this.parentElement.children[0].firstChild.src.trim();
    let bookTitle = this.parentElement.children[1].children[0].textContent.trim();
    let pubYear = this.parentElement.children[1].children[1].textContent.trim();
    let bookAuthor = this.parentElement.children[1].children[2].textContent.trim();
    let readingState = this.parentElement.children[1].children[3].value;
    send_data = {
      title:bookTitle,
      author:bookAuthor,
      year:pubYear,
      cover:bookCover,
      state:readingState
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
  fetch('/get', {
    method: 'POST', // Use POST for sending data
    headers: {
      'Content-Type': 'application/json' // Specify JSON data format
    },
    body: JSON.stringify(data) // Convert data to JSON string
  })
    var popup = document.createElement('div');
    popup.className = 'popup';
    popup.innerHTML = '<p>Book Added to Library!</p>';

    // Append the popup to the container
    var container = document.getElementById('popup-container');
    container.appendChild(popup);

    // Show the popup
    popup.style.display = 'block';
    popup.style.position = 'absolute';
    popup.style.margin = '20% 20%';
    popup.classList.add("card");

    // Set a timeout to hide the popup after a certain duration (e.g., 3000 milliseconds or 3 seconds)
    setTimeout(function() {
        popup.style.display = 'none';
    }, 3000);
 }
let currentYear = new Date().getFullYear();
const yearSpan = document.getElementById("year")
yearSpan.textContent = currentYear