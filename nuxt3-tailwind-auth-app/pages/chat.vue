<template>
  <div class="chat-container">
    <h1>WebSocket Chat</h1>
    <form @submit.prevent="sendMessage" class="message-form">
      <input type="text" v-model="messageText" autocomplete="off" />
      <button class="send-button">Send</button>
    </form>
    <ul id="messages" class="message-list">
      <li v-for="message in messages" :key="message.id" class="message-item">{{ message.v.first_name }}：{{ message.content }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messageText: '',
      messages: []
    };
  },
  mounted() {
    this.setupWebSocket();
  },
  methods: {
    setupWebSocket() {
      const ws = new WebSocket('ws://localhost:8000/ws');
      const auth = useAuth(); // useAuth関数の定義が必要
      const v = {
        first_name: String(auth.userState.value?.first_name)
      };
      ws.onmessage = (event) => {
        this.messages.push({ v, content: event.data });
      };
      this.ws = ws;
    },
    sendMessage() {
      this.ws.send(this.messageText);
      this.messageText = '';
    }
  }
};
</script>

<style>
.chat-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.message-form {
  display: flex;
  margin-bottom: 20px;
}

.message-form input {
  flex-grow: 1;
  padding: 5px;
}

.send-button {
  margin-left: 10px;
}

.message-list {
  list-style-type: none;
  padding: 0;
}

.message-item {
  margin-bottom: 5px;
}
</style>
