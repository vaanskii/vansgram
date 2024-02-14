<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">

        <div class="main-left ">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Edit profile</h1>

                <p class="mb-6 text-gray-500">
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                </p>
                <RouterLink to="/profile/edit/password" class="underline">Change password</RouterLink>
            </div>
        </div>

        <div class="main-right ">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">

                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>Name</label>
                        <input type="text" v-model="form.name" placeholder="Your full name" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Email</label>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div class="border-t border-gray-100 flex flex-col items-center">
                        <label class="my-5 font-mono">Upload profile picture</label>
                        <label for="fileInput" class="flex items-center justify-center py-4 bg-gray-600 text-white rounded-lg w-[200px] cursor-pointer">
                            <input type="file" ref="file" id="fileInput" @change="onFileChange">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                            </svg>
                        </label>
                    </div>


                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Save changes</button>
                    </div>
                </form>

            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import { RouterLink } from 'vue-router';

export default{
    setup() {
        const toastStore = useToastStore();
        const userStore = useUserStore();
        return {
            toastStore,
            userStore
        };
    },
    data() {
        return {
            form: {
                email: this.userStore.user.email,
                name: this.userStore.user.name,
            },
            errors: [],
        };
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }

            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('avatar', this.$refs.file.files[0])
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)

                axios
                    .post('/api/editprofile/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'information updated') {
                            this.toastStore.showToast(5000, 'The information was saved', 'bg-emerald-500')

                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email: this.form.email,
                                avatar: response.data.user.get_avatar
                            })

                            this.$router.back()
                        } else {
                            this.toastStore.showToast(5000, `${response.data.message}. Please try again`, 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    },
    components: { RouterLink }
}

</script>