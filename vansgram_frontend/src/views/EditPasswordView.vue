<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">

        <div class="main-left ">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Edit password</h1>

                <p class="mb-6 text-gray-500">
                    Here you can change your password.
                </p>
            </div>
        </div>

        <div class="main-right ">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">

                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>Old password</label>
                        <input type="password" v-model="form.old_password" placeholder="Enter current password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>New password</label>
                        <input type="password" v-model="form.new_password1" placeholder="Enter new password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Confirm password</label>
                        <input type="password" v-model="form.new_password2" placeholder="Confirm password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
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
                old_password: '',
                new_password1: '',
                new_password2: '',
            },
            errors: [],
        };
    },
    methods: {
        submitForm() {
            this.errors = [];
            
            if (this.form.new_password1 !== this.form.new_password2) {
                this.errors.push('The passwords do not match');
            }

            if (this.errors.length === 0) {
                let formData = new FormData();
                formData.append('old_password', this.form.old_password);
                formData.append('new_password1', this.form.new_password1);
                formData.append('new_password2', this.form.new_password2);

                axios
                    .post('/api/editpassword/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data"
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The password is changed', 'bg-emerald-500');

                            this.$router.push(`/profile/${this.userStore.user.id}`);
                            this.$router.back()
                        }
                        else {
                            const data = JSON.parse(response.data.message);
                            for (const key in data) {
                                this.errors.push(data[key][0].message);
                            }
                        }
                    })
                    .catch(error => {
                        console.log('error', error);
                    });
            }
        }

    },
    components: { RouterLink }
}

</script>