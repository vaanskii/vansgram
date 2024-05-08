 <template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center flex flex-col items-center rounded-lg">
                <img :src="user.get_avatar" class="mb-6 max-w-[233px] max-h-[233px] rounded-full">

                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
                    <RouterLink :to="{name : 'friends', params: {id: user.id}}" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink>
                    <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                </div>

                <div 
                
                class="mt-6">
                    <button 
                        class="inline-block py-4 px-3 text-xs bg-purple-600 text-white rounded-lg" 
                        @click="sendFriendshipRequest"
                        v-if="userStore.user.id !== user.id"
                        >
                        Send friend request
                    </button>

                    <button 
                        class="inline-block mt-4 ml-4 py-4 px-3 text-xs bg-blue-600 text-white rounded-lg" 
                        @click="sendDirectMessage"
                        v-if="userStore.user.id !== user.id"
                        >
                        Message
                    </button>

                </div>

            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div 
                class="bg-white border border-gray-200  rounded-lg"
                v-if="userStore.user.id === user.id"
                >
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">
                        <textarea @keydown.enter.prevent="postOnEnter" v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>

                        <label>
                            <input type="checkbox" v-model="is_private"> Private
                        </label>

                        <div id="preview" v-if="url" class="w-[90px] mt-3">
                            <img :src="url" >
                        </div>  

                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <label for="fileInput" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                            <input type="file" ref="file" id="fileInput" @change="onFileChange">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                            </svg>
                        </label>
                        

                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>     
                </form>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 text-start rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
                >
                <FeedItem v-bind:post="post" v-on:deletePost="deletePost"/>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleMayYouKnow />
            
            <Trends/>
        </div>
    </div>
</template>

<style>
input[type="file"]{
    display: none;
}

.custom-file-upload{
    cursor:pointer;
}
</style>


<script>
import axios from 'axios'
import PeopleMayYouKnow from '@/components/PeopleMayYouKnow.vue'
import Trends from '@/components/Trends.vue'
import { useUserStore } from '@/stores/user';
import FeedItem from '@/components/FeedItem.vue';
import { RouterLink } from 'vue-router';
import { useToastStore } from '@/stores/toast';

export default {
    name: 'FeedView',

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore() 

        return {
            userStore,
            toastStore
        }
    },
    components: {
    PeopleMayYouKnow,
    Trends,
    FeedItem,
    RouterLink
},

    data() {
        return {
            posts : [],
            user: {
                id: ''
            },
            body: '',
            is_private: false,
            url: null
        }
    },

    mounted() {
        this.getFeed()
    },

    watch: {
        '$route.params.id': {
            handler: function() {
                this.getFeed()
            },
            deep: true,
            immediate: true,
        }
    },

    methods: {
        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },
        deletePost(id){
            this.posts = this.posts.filter(post => post.id !== id)
            this.user.posts_count -= 1
        },
        
        sendDirectMessage() {
            axios
                .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    this.$router.push('/chat')
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        sendFriendshipRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`)
                .then(response => {
                    if (response.data.message == 'request already sent') {
                        this.toastStore.showToast(5000, 'The request already been sent!', 'bg-red-300')
                    }else {
                        this.toastStore.showToast(5000, 'The request was sent!', 'bg-emerald-300')
                    }
                    
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {

                    this.posts = response.data.posts
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)
            formData.append('is_private', this.is_private)

            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    this.posts.unshift(response.data)
                    this.body = ''
                    this.is_private = false
                    this.$refs.file.value = null
                    this.url = null
                    this.user.posts_count += 1
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        logout() {
            this.userStore.removeToken()

            this.$router.push('/login')
        },
        postOnEnter() {
                if (!event.shiftKey) {
                event.preventDefault();
                this.submitForm();
                }
            }
        },
     }
</script>