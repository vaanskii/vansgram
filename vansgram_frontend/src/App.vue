<template>
  <nav class="py-10 px-8 border-b border-gray-200">
      <div class="max-w-7xl mx-auto">
          <div class="flex items-center justify-between">
              <div class="menu-left">
                  <a href="#" class="text-xl font-extrabold">VANSGRAM</a>
              </div>

              <div class="menu-center flex space-x-12" v-if="userStore.user.isAuthenticated">
                  <RouterLink to="/feed" class="text-purple-700">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                      </svg>
                  </RouterLink>

                  <RouterLink to="/chat">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z" />
                    </svg>                             
                  </RouterLink>

                  <RouterLink to="/notifications">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"></path>
                      </svg>                              
                  </RouterLink>

                  <RouterLink to="/search">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                      </svg>                                                         
                  </RouterLink>
              </div>

              <div class="menu-right">
                <template v-if="userStore.user.isAuthenticated && userStore.user.id">
                    
                    <button @click="toggleDropdown" class="flex items-center text-sm pe-1 font-medium text-gray-900 rounded-full hover:text-blue-600 dark:hover:text-blue-500 md:me-0 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:text-white" type="button">
                    <img :src="userStore.user.avatar" class="w-12 h-12 rounded-full">
                    <p class="text-black font-bold ml-3">{{ this.userStore.user.name }}</p>
                    <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
                    </svg>
                    </button>

                    <div v-if="dropDown" id="dropdown" class="w-[250px] absolute z-10 bg-white divide-y divide-gray-100 rounded-lg shadow w-100 dark:bg-gray-600 mt-5 dark:divide-gray-600">
                        <ul class="py-2 text-sm text-gray-700 dark:text-gray-200">
                            <div class="px-4 py-3 text-sm text-gray-900 dark:text-white flex justify-center">
                            <div class="truncate">{{ this.userStore.user.email }}</div>
                            </div>
                        <li>
                            <RouterLink :to="{name: 'profile', params: {'id': userStore.user.id}}" @click="closeDropdown" class="flex items-center px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                </svg>
                                Profile
                            </RouterLink>
                        </li>
                        <li>
                            <RouterLink :to="{name: 'editprofile'}" @click="closeDropdown" class="flex items-center px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 0 1 1.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.559.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.894.149c-.424.07-.764.383-.929.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 0 1-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.398.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 0 1-.12-1.45l.527-.737c.25-.35.272-.806.108-1.204-.165-.397-.506-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.108-1.204l-.526-.738a1.125 1.125 0 0 1 .12-1.45l.773-.773a1.125 1.125 0 0 1 1.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894Z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                </svg>
                                Settings
                            </RouterLink>
                        </li>
                        </ul>
                        <div class="py-2">
                        <a href="#" @click="logout(); closeDropdown()" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">Sign out</a>
                        </div>
                    </div>
                </template>

                <template v-else>
                    <RouterLink to="/login" class="mr-4 py-4 px-6 bg-gray-600 text-white rounded-lg">Log in</RouterLink>
                    <RouterLink to="/signup" class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign up</RouterLink>
                </template>
              </div>
          </div>
      </div>
  </nav>

  <main class="px-8 py-6 bg-gray-100">
      <RouterView />
  </main>

  <Toast />
</template>

<script>
  import axios from 'axios'
  import Toast from '@/components/Toast.vue'
  import { useUserStore } from '@/stores/user'
import { RouterLink } from 'vue-router'

  export default {
      data() {
        return {
            dropDown: false
        }
      },
      methods: {
      toggleDropdown(event) {
        event.stopPropagation()
        this.dropDown = !this.dropDown;
        if (this.dropDown) {
          window.addEventListener('click', this.closeIfClickedOutside);
        } else {
          window.removeEventListener('click', this.closeIfClickedOutside);
        }
      },
      closeIfClickedOutside(event) {
        if (!document.getElementById('dropdown').contains(event.target)) {
          this.dropDown = false;
          window.removeEventListener('click', this.closeIfClickedOutside);
        }
      },
      closeDropdown() {
        this.dropDown = false;
        window.removeEventListener('click', this.closeIfClickedOutside);
      },
      logout() {
            this.userStore.removeToken()

            this.$router.push('/login')
        }
    },

      setup() {
          const userStore = useUserStore()

          return {
              userStore
          }
      },

      components: {
    Toast,
    RouterLink
},

      beforeCreate() {
          this.userStore.initStore()

          const token = this.userStore.user.access

          if (token) {
              axios.defaults.headers.common["Authorization"] = "Bearer " + token;
          } else {
              axios.defaults.headers.common["Authorization"] = "";
          }
      }
  }
</script>


