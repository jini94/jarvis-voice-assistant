const button = document.getElementById("talkButton");
const orb = document.getElementById("orb");
const userText = document.getElementById("userText");
const jarvisText = document.getElementById("jarvisText");

button.addEventListener("click", async () => {
    button.disabled = true;
    orb.classList.add("active");
    userText.textContent = "Listening...";
    jarvisText.textContent = "";

    const response = await fetch("/talk", { method: "POST" });
    const data = await response.json();

    orb.classList.remove("active");
    userText.textContent = "You said: " + data.user_text;
    jarvisText.textContent = "Jarvis: " + data.jarvis_text;
    button.disabled = false;
});