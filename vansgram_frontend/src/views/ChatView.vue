<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
      <div class="main-left col-span-1">
          <div class="p-4 bg-white border border-gray-200 rounded-lg">
              <h3 class="mb-6 text-xl">People you may know</h3>
              
              <div class="space-y-4">
                  <div 
                      class="flex items-center justify-between cursor-pointer"
                      v-for="conversation in conversations"
                      v-bind:key="conversation.id"
                      v-on:click="setActiveConversation(conversation.id)"
                      >
                      <div class="flex items-center space-x-2"> 
                          <template 
                          v-for="user in conversation.users"
                          v-bind:key="user.id"
                          >
                          <div v-if="user.id !== userStore.user.id">
                              <img :src="user.get_avatar" class="w-[40px] rounded-full" alt="">
                          </div>
                              <p
                              class="text-xs font-bold"
                              v-if="user.id !== userStore.user.id"
                              >
                              {{ user.name }} 
                              </p>
                          
                          </template>

                      </div>
                      <span class="text-xs text-gray-500">{{ conversation.modified_at_formatted }}</span>
                  </div>


              </div>
          </div>
      </div>

      <div class="main-center col-span-3 space-y-4">
          <div ref="messageContainer" class="bg-white border border-gray-200 rounded-lg h-[600px] overflow-x-auto">
              <div class="flex flex-col flex-grow p-4">
                  <template 
                  v-for="message in activeConversation.messages"
                  v-bind:key="message.id"
                  >
                  <div 
                  class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
                  v-if="message.created_by.id == userStore.user.id"
                  >
                      <div>
                          <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                              <p class="text-sm max-w-xs break-words">{{ message.body }}</p>
                          </div>
                          <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }}</span>
                      </div>
                      <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                          <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full">
                      </div>
                  </div>

                  <div 
                  class="flex w-full mt-2 space-x-3 max-w-md"
                  v-else
                  >
                      <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                          <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full">
                      </div>
                      <div>
                          <div class="bg-gray-300 p-3 rounded-r-lg">
                              <p class="text-sm max-w-xs break-words">{{ message.body }}</p>
                          </div>
                          <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }}</span>
                      </div>
                  </div>

                  </template>
                  
              </div>
          </div>

          <div v-if="Object.keys(activeConversation).length > 0" class="bg-white border border-gray-200 rounded-lg">
              <form v-on:submit.prevent="submitForm"> 
                  <div class="p-4 flex justify-between items-center ">
                      <textarea v-model="body" @keydown.enter.prevent="sendMessageOnEnter" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Write a message"></textarea>
                      <button class="inline-block py-7 mx-3 px-6 bg-purple-600 text-white rounded-lg">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
                          </svg>
                      </button>
                  </div>
              </form>  
          </div>

      </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user';

export default {
name: 'chat',

setup() {
  const userStore = useUserStore();
  return {
    userStore
  };
},

data() {
  return {
    conversations: [],
    activeConversation: {},
    body: '',
    loading: true,
    socket: null,
    status: 'disconnected'
  };
},

  mounted() {
    this.getConversations();
    this.connectToWebSocket();
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  },

watch: {
  'activeConversation.id': function(newVal, oldVal) {
    if (newVal !== oldVal) {
      this.connectToWebSocket(newVal);
    }
  },
  '$route': {
    immediate: true,
    handler: 'setActiveConversationFromRoute'
  }
},

methods: {
  setActiveConversationFromRoute() {
    if (!this.loading) {
      const conversationId = this.$route.params.id;
      if (conversationId) {
        this.setActiveConversation(conversationId);
      } else {
        this.activeConversation = {};
      }
    }
  },
  getConversations() {
    this.loading = true;
    axios
      .get('/api/chat/')
      .then(response => {
        this.conversations = response.data;
        this.loading = false;
        this.setActiveConversationFromRoute();
      })
      .catch(error => {
        this.loading = false;
        console.error('error', error);
      });
  },
  setActiveConversation(conversationId) {
    const conversation = this.conversations.find(convo => convo.id === conversationId);
    if (conversation) {
      this.activeConversation = conversation;
      this.$router.push({ name: 'chat', params: { id: conversationId } });
      this.getMessages();
    }
  },
  connectToWebSocket(conversationId) {
    if (this.socket) {
      this.socket.close();
    }
    if (conversationId) {
      this.socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${conversationId}/`);
      this.socket.onopen = function(e) {
        console.log('WebSocket connection established')
        this.status = 'connected'
      };
      this.socket.onmessage = (event) => {
        const receivedMessage = JSON.parse(event.data);
        if (receivedMessage.conversationId === this.activeConversation.id) {
          if (!this.activeConversation.messages.some(msg => msg.id === receivedMessage.id)) {
            this.activeConversation.messages.push({
              ...receivedMessage,
              created_by: {
                ...receivedMessage.created_by,
                get_avatar: receivedMessage.created_by.get_avatar 
              },
              created_at_formatted: receivedMessage.created_at_formatted 
            });
            this.$nextTick(() => {
              this.scrollMessagesToBottom();
            });
          }
        }
      };
      this.socket.onclose = (event) => {
        this.status = 'disconnected';
        console.log('WebSocket disconnected. Attempting to reconnect...');
        setTimeout(() => {
          this.connectToWebSocket();
        }, 1000);
      };
    }
  },
  getMessages() {
    if (this.activeConversation && this.activeConversation.id) {
      axios
        .get(`/api/chat/${this.activeConversation.id}/`)
        .then(response => {
          this.activeConversation = response.data;
          this.$nextTick(() => {
            this.scrollMessagesToBottom();
          });
        })
        .catch(error => {
          console.log('error', error);
        });
    }
  },
  submitForm() {
  if (this.socket && this.activeConversation.id) {
    const messageData = {
      conversationId: this.activeConversation.id,
      body: this.body,
      created_by: {
        id: this.userStore.user.id
      }
    };
    this.socket.send(JSON.stringify(messageData));
    this.body = '';
  }
},
  scrollMessagesToBottom() {
    const container = this.$refs.messageContainer;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  },
  sendMessageOnEnter() {
    if (!event.shiftKey) {
      event.preventDefault();
      this.submitForm();
    }
  }
}
};
</script>