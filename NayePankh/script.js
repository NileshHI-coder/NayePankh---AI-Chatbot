
const chatbox=document.getElementById("chatbox");


async function sendMessage(){

let input=document.getElementById("message");

let msg=input.value;

if(msg==="") return;


chatbox.innerHTML+=`

<div class='user'>

<b>You:</b>

${msg}

</div>

`;

input.value="";


const response=await fetch("/chat",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

message:msg

})

});


const data=await response.json();


chatbox.innerHTML+=`

<div class='bot'>

<b>Bot:</b>

${data.reply}

</div>

`;


chatbox.scrollTop=chatbox.scrollHeight;

}



async function clearChat(){

await fetch("/clear");

chatbox.innerHTML="";

}