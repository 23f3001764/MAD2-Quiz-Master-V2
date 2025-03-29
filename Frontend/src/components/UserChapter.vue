<template>
    <div class="container mt-4">
        <div v-if="errormessage"
            class="alert alert-danger text-center fade-in d-flex justify-content-between align-items-center">
            <span>{{ errormessage }}</span>
            <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="display-1 fw-bold">Chapters for {{ sname }}</h2>
        </div>

        <div class="mb-3">
            <input type="text" v-model="searchQuery" class="form-control" placeholder="Search chapters..." />
        </div>

        <div v-if="filteredChapters.length">
            <table class="table table-hover table-bordered">
                <thead class="table-dark">
                    <tr>
                        <th>#</th>
                        <th>Chapter Name</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(chapter, index) in filteredChapters" :key="chapter.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ chapter.chname }}</td>
                        <td>{{ chapter.description }}</td>
                        <td>
                            <router-link :to="'/quizzes/' + chapter.chname" class="btn btn-info btn-sm">
                                View Quizzes
                            </router-link>
                            <button v-if="notifiedChapters.includes(chapter.id)" class="btn btn-danger btn-sm ms-2"
                                @click="unnotifyMe(chapter.id)">
                                Unnotify Me
                            </button>
                            <button v-else class="btn btn-success btn-sm ms-2" @click="notifyMe(chapter.chname)">
                                Notify Me
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="alert alert-info text-center">No chapters available.</div>
        <div class="text-center mt-4">
            <h5 class="text-info">More Chapters Coming Soon...</h5>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            sname: this.$route.params.sname,
            chapters: [],
            notifiedChapters: [], 
            searchQuery: "",
            errormessage: null,
            chapID: null,
        };
    },
    computed: {
        filteredChapters() {
            return this.chapters.filter(chapter =>
                chapter.chname.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        },
    },
    created() {
        this.fetchChapters();
        this.fetchNotifiedChapters();
    },
    methods: {
        async fetchChapters() {
            const token = localStorage.getItem("usertoken");

            try {
                const response = await fetch(`/api/chapter/${this.sname}`, {
                    method: "GET",
                    headers: { Authorization: `Bearer ${token}` },
                });

                const data = await response.json();
                this.chapters = data;
            } catch (error) {
                console.error("Error fetching chapters:", error);
                this.errormessage = "Failed to fetch chapters.";
            }
        },

        async fetchNotifiedChapters() {
            const token = localStorage.getItem("usertoken");

            try {
                const response = await fetch(`/api/notify`, {
                    method: "GET",
                    headers: { Authorization: `Bearer ${token}` },
                });

                const text = await response.text();  
                console.log("Raw API Response:", text);

                const data = JSON.parse(text);

                this.notifiedChapters = data.map(notify => notify.chname);
            } catch (error) {
                console.error("Error fetching notifications:", error);
            }
        },

        async notifyMe(chname) {
            const token = localStorage.getItem("usertoken");

            const notifyTime = prompt("Enter notification time in 24 hour format (HH:MM):");
            if (!notifyTime) return;

            try {
                const response = await fetch(`/api/notifies/${chname}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({ time: notifyTime }),
                });

                if (!response.ok) throw new Error("Failed to set notification");

                this.notifiedChapters.push(chapId);
            } catch (error) {
                console.error("Error setting notification:", error);
            }
        },

        async unnotifyMe(chapId) {
            const token = localStorage.getItem("usertoken");

            try {
                const notifyId = this.notifiedChapters.find(id => id === chapId);
                if (!notifyId) return;

                const response = await fetch(`/api/notify/${notifyId}`, {
                    method: "DELETE",
                    headers: { Authorization: `Bearer ${token}` },
                });

                if (!response.ok) throw new Error("Failed to remove notification");

                this.notifiedChapters = this.notifiedChapters.filter(id => id !== chapId);
            } catch (error) {
                console.error("Error removing notification:", error);
            }
        },
    },
};
</script>

<style scoped>
.container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
}

h2 {
    font-weight: bold;
    margin-bottom: 20px;
}

.table {
    margin-bottom: 20px;
}

.btn {
    min-width: 100px;
}
</style>
