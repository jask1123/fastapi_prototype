<template>
  <div>
    <h1>WebSocket Chat</h1>
    <form @submit.prevent="sendMessage">
      <input type="text" v-model="messageText" autocomplete="off" />
      <button>Send</button>
    </form>
    <ul id="messages">
      <li v-for="message in messages" :key="message.id">{{ message.content }}</li>
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
      ws.onmessage = (event) => {
        this.messages.push({ id: Date.now(), content: event.data });
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
/* CSS スタイルを適用する場合はここに記述します */
</style>
