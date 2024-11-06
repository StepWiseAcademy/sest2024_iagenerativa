<template>
  <div id="app">
    <div class="chat-container">
      <div class="messages">
        <!-- Render messages as separate divs -->
        <div v-for="(message, index) in messages" :key="index" :class="message.class">
          {{ message.text }}
        </div>
      </div>
      <input
        v-model="query"
        @keydown.enter="sendMessage"
        placeholder="Digite sua pergunta e aperte enter"
        class="input-box"
      />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: "",
      messages: [], // Array to store all messages
      isStreaming: false,
    };
  },
  methods: {
    sendMessage() {
      if (this.query.trim() === "" || this.isStreaming) return;

      // Add user's message to the messages array
      this.messages.push({ text: this.query, class: "message-user" });

      this.isStreaming = true;

      fetch("http://127.0.0.1:5000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query_text: this.query }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.body.getReader();
        })
        .then((reader) => {
          const decoder = new TextDecoder();

          // Add an empty assistant message placeholder
          const assistantMessage = { text: "", class: "message-assistant" };
          this.messages.push(assistantMessage);

          const readStream = () => {
            reader.read().then(({ done, value }) => {
              if (done) {
                this.isStreaming = false;
                return;
              }

              const chunk = decoder.decode(value);
              assistantMessage.text += chunk; // Append each chunk to the assistant's message
              
              // Trigger Vue to update the view
              this.$forceUpdate();

              readStream();
            });
          };

          readStream();
        })
        .catch((error) => {
          console.error("Error:", error);
          this.isStreaming = false;
        });

      this.query = "";
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}

body {
  background-color: #212121;
}

.chat-container {
  width: 50%;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
}

.messages {
  height: 700px;
  overflow-y: auto;
  margin-bottom: 10px;
  color: white;
  padding: 10px;
  border-radius: 8px;
  white-space: pre-wrap; /* Mantém quebras de linha e espaços */
  text-align: left;
}

.message-user {
  margin-top: 15px;
  background-color: rgb(47, 47, 47);
  border-radius: 15px;
  width: 60%;
  margin-left: auto;
  padding: 15px;
}

.message-assistant {
  color: #ffffff;
  margin-bottom: 20px;
  margin-top: 30px;
  line-height: 1.5em;
}

.input-box {
  width: 95%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 30px;
  background-color: rgb(58, 58, 58);
  color: white;
}
</style>
