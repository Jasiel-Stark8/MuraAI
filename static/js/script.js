function chatBot() {
  return {
    botTyping: false,
    messages: [],
    lastIdx: null,
    output: function (input) {
      let text = input.trim();
      // Add user message
      this.messages.push({
        from: "user",
        text: text,
      });

      this.scrollChat();
      this.botTyping = true;
      this.sendPromptRequest(
        input,
        (response) => {
          if (response != null) {
            let lastId = this.lastIdx;
            if (lastId === null) {
              const newidx = this.messages.push({
                from: "bot",
                text: response,
              });
              this.lastIdx = newidx - 1;
            } else {
              this.messages[
                lastId
              ].text = `${this.messages[lastId].text} ${response}`;
            }
            this.botTyping = false;
          } else {
            this.lastIdx = null;
          }
          this.scrollChat();
        },
        (error) => {
          this.lastIdx = null;
        }
      );
    },
    sendPromptRequest: async function (prompt, onType, onError) {
      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ prompt: prompt }),
        });
        const reader = response.body.getReader();
        reader.read().then(function pump({ done, value }) {
          if (done) {
            onType(null);
            return;
          }
          if (value != null) {
            var string = new TextDecoder().decode(value);
            onType(string);
          }
          return reader.read().then(pump);
        });
      } catch (error) {
        onError(error);
      }
    },
    scrollChat: function () {
      const messagesContainer = document.getElementById("messagesContainer");
      messagesContainer.scrollTop =
        messagesContainer.scrollHeight - messagesContainer.clientHeight;
      setTimeout(() => {
        messagesContainer.scrollTop =
          messagesContainer.scrollHeight - messagesContainer.clientHeight;
      }, 100);
    },
    updateChat: function (target) {
      if (target.value.trim()) {
        this.output(target.value.trim());
        target.value = "";
      }
    },
    usePreDefined: function (target) {
      const cardElement = target.closest(".predef-content");

      if (cardElement) {
        this.output(cardElement.querySelector("p").textContent);
      }
    },
  };
}
