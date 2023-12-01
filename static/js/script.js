const state = {
  lastId: null,
};

document.addEventListener("DOMContentLoaded", function () {
  const chatMessages = document.getElementById("chat-messages");
  const messageInput = document.getElementById("message-input");
  const sendBtn = document.getElementById("send-btn");
  const introSection = document.getElementById("intro-section");

  sendBtn.addEventListener("click", async () => {
    questionInput = messageInput.value;
    introSection.style.display = "none";
    appendUserMessage();
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: questionInput }),
    });
    const reader = response.body.getReader();
    reader.read().then(function pump({ done, value }) {
      console.log({ done, value });
      if (done) {
        state.lastId = null;
        return;
      }
      if (value != null) {
        var string = new TextDecoder().decode(value);
        appendBotMessage(string, done);
      }
      return reader.read().then(pump);
    });
  });

  function appendBotMessage(text) {
    let messageDiv;
    let lastId;
    let isNew = false;
    if (state.lastId === null) {
      state.lastId = Math.random().toString(36).substring(7);
      messageDiv = document.createElement("div");
      lastId = state.lastId;
      isNew = true;
    } else {
      messageDiv = document.getElementById(state.lastId);
    }

    if (isNew) {
      messageDiv.className = `mb-2 flex flex-col w-full gap-6`;
      messageDiv.innerHTML = `
            <div class="flex flex-row gap-4 items-center">
                <img class="bg-primary rounded-full w-8 h-8 p-2" src="/static/images/logo_small.png" alt="">
                <span>Mura AI</span>
            </div>
            <p id="${lastId}">${text}</p>
      `;
      chatMessages.appendChild(messageDiv);
    } else {
      messageDiv.textContent = `${messageDiv.textContent} ${text}`;
    }
    // Scroll to the bottom to always show the latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendUserMessage() {
    const messageDiv = document.createElement("div");
    messageDiv.className = "mb-2 text-right";
    messageDiv.innerHTML = `
        <div class="flex flex-row gap-4 items-center">
                <img class="bg-neutral-content rounded-full w-8 h-8 p-2" src="/static/images/user.png" alt="">
                <span>You</span>
            </div>
            <p>${messageInput.value}</p>
    `;
    messageInput.value = "";
    chatMessages.appendChild(messageDiv);
  }
});
