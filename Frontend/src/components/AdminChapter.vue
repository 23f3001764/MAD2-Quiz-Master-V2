<template>
    <div class="container mt-4">
        <div v-if="errormessage" class="alert alert-danger text-center">
            {{ errormessage }}
            <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="display-1 fw-bold">Chapters</h2>
            <router-link :to="'/addchapter/' + sname" class="btn btn-primary btn-lg">+ Add Chapter</router-link>
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
                        <th>Subject Name</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(chapter, index) in filteredChapters" :key="chapter.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ chapter.chname }}</td>
                        <td>{{ chapter.sname }}</td>
                        <td>{{ chapter.description }}</td>
                        <td>
                            <router-link :to="'/adminquiz/' + chapter.chname" class="btn btn-info btn-sm me-2">
                                Quiz
                            </router-link>
                            <router-link :to="'/editchapter/' + chapter.id" class="btn btn-warning btn-sm me-2">
                                Edit
                            </router-link>
                            <button @click="deleteChapter(chapter.id)" class="btn btn-danger btn-sm">
                                Delete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="alert alert-info text-center">No chapters available.</div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            chapters: [],
            searchQuery: "",
            errormessage: null,
            sname: this.$route.params.sname,
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
    },
    methods: {
        async fetchChapters() {
            const token = localStorage.getItem("admintoken");
            try {
                const response = await fetch(`/api/chapter/${this.sname}`, {
                    method: "GET",
                    headers: { Authorization: `Bearer ${token}` },
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch chapters.");
                }

                const data = await response.json();
                this.chapters = data;
            } catch (error) {
                console.error("Error fetching chapters:", error);
                this.errormessage = "Failed to fetch chapters.";
            }
        },
        async deleteChapter(chapterId) {
            const token = localStorage.getItem("admintoken");

            if (!confirm("Are you sure you want to delete this chapter?")) return;

            try {
                const response = await fetch(`/api/chapter/${chapterId}`, {
                    method: "DELETE",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    this.errormessage = errorData.message || "Failed to delete chapter.";
                    return;
                }

                this.chapters = this.chapters.filter(chapter => chapter.id !== chapterId);
            } catch (error) {
                console.error("Error deleting chapter:", error);
                this.errormessage = "An error occurred while deleting the chapter.";
            }
        }
    },
};
</script>
