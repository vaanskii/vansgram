<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div 
                class="p-4 bg-white border border-gray-200 text-start rounded-lg"
                v-if="post.id"
                >
                <FeedItem v-bind:post="post"></FeedItem>
            </div>


            <div 
            class="p-4 ml-6 border border-gray-200 bg-gray-200 rounded-lg"
            v-for="comment in post.comments"
            v-bind:key="comment.id"
            >

            <CommentItem v-bind:comment="comment"></CommentItem>

            </div>

            <div class="bg-white border border-gray-200 text-center rounded-lg">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">
                        <textarea @keydown.enter.prevent="commentOnEnter" v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Add a comment"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <a href="" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                            </svg>
                        </a>
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
                            </svg>
                        </button>
                    </div>     
                </form>
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
import FeedItem from '@/components/FeedItem.vue';
import CommentItem from '@/components/CommentItem.vue'

export default {
    name: 'PostView',

    components: {
         PeopleMayYouKnow, 
         Trends,
         FeedItem,
         CommentItem
    },

    data() {
        return {
            post: {
                id: null,
                comments: []
            },
            body: ''
        }
    },

    mounted() {
        this.getPost()
    },

    methods: {
        getPost() {
            axios
                .get(`/api/posts/${this.$route.params.id}/`)
                .then(response => {
                    this.post = response.data.post
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            axios
                .post(`/api/posts/${this.$route.params.id}/comment/`, {
                    'body': this.body
                }) 
                .then(response => {
                    this.post.comments.push(response.data)
                    this.post.comments_count += 1
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
            },
            commentOnEnter() {
                if (!event.shiftKey) {
                event.preventDefault();
                this.submitForm();
                }
            } 
        },
    }
</script>