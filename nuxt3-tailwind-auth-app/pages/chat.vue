<template>
  <div>
    <h1>リアルタイム掲示板</h1>
    <ul>
      <li v-for="(message, index) in messages" :key="index">
        {{ message }}
      </li>
    </ul>
    <form @submit.prevent="sendMessage">
      <input type="text" v-model="newMessage" />
      <button type="submit">送信</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: [],
      newMessage: "",
      websocket: null
    };
  },
  mounted() {
    this.setupWebSocket();
  },
  beforeUnmount() {
    this.closeWebSocket();
  },
  methods: {
    setupWebSocket() {
      this.websocket = new WebSocket("ws://localhost:8000/ws");

      this.websocket.onmessage = (event) => {
        const message = event.data;
        this.messages.push(message);
      };

      this.websocket.onclose = () => {
        // WebSocketが閉じられた場合の処理
      };
    },
    closeWebSocket() {
      if (this.websocket) {
        this.websocket.close();
      }
    },
    sendMessage() {
      const message = this.newMessage;
      this.websocket.send(message);
      this.newMessage = "";

      // 送信したメッセージを即座に表示
      this.messages.push(message);
    }
  }
};
</script>
