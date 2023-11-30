async function postData(url = "", data = {}) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return response.json();
}

const state = {
    isChatting: false,
}

document.addEventListener("DOMContentLoaded", function () {
  const chatMessages = document.getElementById("chat-messages");
  const messageInput = document.getElementById("message-input");
  const sendBtn = document.getElementById("send-btn");
  const introSection = document.getElementById("intro-section");

  sendBtn.addEventListener("click", async () => {
    questionInput = messageInput.value;
    messageInput.value = "";
    let result = await postData("/api/chat", { prompt: questionInput });
    appendMessage("user", result.message);
  });

  function appendMessage(sender, text) {
    introSection.style.display = "none";
    
    const messageDiv = document.createElement("div");
    messageDiv.className = `mb-2 ${sender === "user" ? "text-right" : ""}`;
    messageDiv.textContent = `${sender === "user" ? "You:" : "Bot:"} ${text}`;
    chatMessages.appendChild(messageDiv);
    // Scroll to the bottom to always show the latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
