const form = document.getElementById("nameForm");
const input = document.getElementById("nameInput");
const nameList = document.getElementById("nameList");
const escapeContainer = document.getElementById("escapeContainer");

form.addEventListener("submit",function (event){
    event.preventDefault();
    // stop the default function of the submit button

    const newName = input.value.trim();
    if (newName === ""){
        return;
    }

    const li = document.createElement("li");
    li.textContent = newName;

    nameList.appendChild(li);

    if (newName.toLowerCase() === "hacker"){
        document.body.classList.remove("blue");
        document.body.classList.add("red");
        alert("YOU HAVE BEEN HACKED ! HEHEHE");

        const escapeButton = document.createElement("button");
        escapeButton.id = "escapeButton";
        escapeButton.textContent = "Press to Escape !";


        escapeButton.addEventListener("click",function (){
            location.href = "index.html";
        })
        escapeContainer.appendChild(escapeButton);
    }




});