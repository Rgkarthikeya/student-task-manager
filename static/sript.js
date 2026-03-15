function searchTask(){

let input = document.getElementById("search").value.toLowerCase()

let tasks = document.querySelectorAll(".task-card")

tasks.forEach(task=>{

let text = task.innerText.toLowerCase()

if(text.includes(input))
task.style.display="block"

else
task.style.display="none"

})

}

function confirmDelete(){

return confirm("Delete this task?")

}