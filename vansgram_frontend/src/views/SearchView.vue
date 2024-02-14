<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" class="p-4 flex space-x-4">
                    <input v-model="query" type="search" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Search">

                    <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                        </svg>
                    </button>
                </form>
            </div>

            <div
                class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4"
                v-if="users.length"
                >

                <div 
                    class="p-4 text-center bg-gray-100 rounded-lg flex flex-col items-center"
                    v-for="user in users"
                    v-bind:key="user.id"
                >
                    <img :src="user.get_avatar"  class="mb-6 rounded-full w-[153px] h-[153px]">
                    <p>
                        <strong>
                            <RouterLink :to="{name: 'profile', params: {'id': user.id}}"> {{ user.name }} </RouterLink>
                        </strong>
                    </p>
                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                        <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                    </div>
                </div>

            </div>

            <div 
                class="p-4 bg-white border border-gray-200 text-start rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
                >
            <FeedItem v-bind:post="post"></FeedItem>
            </div>
        </div>
        <div class="main-right col-span-1 space-y-4">
            <PeopleMayYouKnow />
            
            <Trends/>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import PeopleMayYouKnow from '@/components/PeopleMayYouKnow.vue'
import Trends from '@/components/Trends.vue'
import { RouterLink } from 'vue-router'
import FeedItem from '@/components/FeedItem.vue'

export default {
    name: 'SearchView',

    components: {
    PeopleMayYouKnow,
    Trends,
    FeedItem
},
    data() {
        return {
            query: '',
            users : [],
            posts: []
        }
    },
    methods: {
        submitForm() {
            console.log('submitForm', this.query)

            axios
                .post('/api/search/', {
                    query: this.query
                })
                .then(response => {
                    console.log('response:', response.data)

                    this.users = response.data.users
                    this.posts = response.data.posts
                })
                .catch(error => {
                    console.log('error:', error)
                })
            }
        }
    }
</script>