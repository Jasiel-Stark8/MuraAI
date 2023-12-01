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
        },
        (error) => {
          this.lastIdx = null;
        }
      );
    },
    compare: function (promptsArray, repliesArray, string) {
      let reply;
      let replyFound = false;
      for (let x = 0; x < promptsArray.length; x++) {
        for (let y = 0; y < promptsArray[x].length; y++) {
          if (promptsArray[x][y] === string) {
            let replies = repliesArray[x];
            reply = replies[Math.floor(Math.random() * replies.length)];
            replyFound = true;
            // Stop inner loop when input value matches this.prompts
            break;
          }
        }
        if (replyFound) {
          // Stop outer loop when reply is found instead of interating through the entire array
          break;
        }
      }
      if (!reply) {
        for (let x = 0; x < promptsArray.length; x++) {
          for (let y = 0; y < promptsArray[x].length; y++) {
            if (this.levenshtein(promptsArray[x][y], string) >= 0.75) {
              let replies = repliesArray[x];
              reply = replies[Math.floor(Math.random() * replies.length)];
              replyFound = true;
              // Stop inner loop when input value matches this.prompts
              break;
            }
          }
          if (replyFound) {
            // Stop outer loop when reply is found instead of interating through the entire array
            break;
          }
        }
      }
      return reply;
    },
    levenshtein: function (s1, s2) {
      var longer = s1;
      var shorter = s2;
      if (s1.length < s2.length) {
        longer = s2;
        shorter = s1;
      }
      var longerLength = longer.length;
      if (longerLength == 0) {
        return 1.0;
      }
      return (
        (longerLength - this.editDistance(longer, shorter)) /
        parseFloat(longerLength)
      );
    },
    editDistance: function (s1, s2) {
      s1 = s1.toLowerCase();
      s2 = s2.toLowerCase();

      var costs = new Array();
      for (var i = 0; i <= s1.length; i++) {
        var lastValue = i;
        for (var j = 0; j <= s2.length; j++) {
          if (i == 0) costs[j] = j;
          else {
            if (j > 0) {
              var newValue = costs[j - 1];
              if (s1.charAt(i - 1) != s2.charAt(j - 1))
                newValue =
                  Math.min(Math.min(newValue, lastValue), costs[j]) + 1;
              costs[j - 1] = lastValue;
              lastValue = newValue;
            }
          }
        }
        if (i > 0) costs[s2.length] = lastValue;
      }
      return costs[s2.length];
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
      const messagesContainer = document.getElementById("messages");
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
  };
}
