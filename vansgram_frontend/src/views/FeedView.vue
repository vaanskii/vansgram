<template>
    <div class="max-w-7xl mx-auto grid grid-cols-5 gap-4">
        
       <LeftPage/>

        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 text-center rounded-lg">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">
                        <textarea @keydown.enter.prevent="postOnEnter" v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>

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


<script>
import axios from 'axios'
import PeopleMayYouKnow from '@/components/PeopleMayYouKnow.vue'
import Trends from '@/components/Trends.vue'
import FeedItem from '@/components/FeedItem.vue'
import LeftPage from '@/components/LeftPage.vue'
import { useUserStore } from '@/stores/user'
import { RouterLink } from 'vue-router'

export default {
    name: 'FeedView',

    components: {
    PeopleMayYouKnow,
    Trends,
    FeedItem,
    RouterLink,
    LeftPage
},

    data() {
        return {
            posts : [],
            body: '',
            url: null
        }
    },

    mounted() {
        this.getFeed()
    },
    setup() {
          const userStore = useUserStore()

          return {
              userStore
          }
    },

    methods: {
        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },
        getFeed() {
            axios
                .get('/api/posts/')
                .then(response => {

                    this.posts = response.data;
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)


            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    this.posts.unshift(response.data)
                    this.body = ''
                    this.$refs.file.value = null
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
            postOnEnter() {
                if (!event.shiftKey) {
                event.preventDefault();
                this.submitForm();
                }
            },
            deletePost(id){
            this.posts = this.posts.filter(post => post.id !== id)
            },
        },
    }
</script>