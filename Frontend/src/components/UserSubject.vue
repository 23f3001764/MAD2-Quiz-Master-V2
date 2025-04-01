<template>
    <div class="container mt-4">
        <div v-if="errormessage" class="alert alert-danger text-center fade-in">
            {{ errormessage }}
            <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="display-1 fw-bold">Subjects</h2>
        </div>

        <div class="mb-3">
            <input type="text" v-model="searchQuery" class="form-control" placeholder="Search subjects..." />
        </div>

        <div v-if="filteredSubjects.length">
            <table class="table table-hover table-bordered">
                <thead class="table-dark">
                    <tr>
                        <th>#</th>
                        <th>Subject Name</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(subject, index) in filteredSubjects" :key="subject.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ subject.sname }}</td>
                        <td>{{ subject.description }}</td>
                        <td>
                            <router-link :to="'/chapter/' + subject.sname" class="btn btn-info btn-sm">
                                View Chapters
                            </router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="alert alert-info text-center">No subjects available.</div>
        <div class="text-center mt-4">
            <h5 class="text-info">More Subjects Coming Soon...</h5>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            subjects: [],
            searchQuery: "",
            errormessage: null,
        };
    },
    computed: {
        filteredSubjects() {
            return this.subjects.filter(subject =>
                subject.sname.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        },
    },
    created() {
        this.fetchSubjects();
    },
    methods: {
        async fetchSubjects() {
            const token = localStorage.getItem("usertoken"); 
            try {
                const response = await fetch("/api/subject", {
                    method: "GET",
                    headers: { Authorization: `Bearer ${token}` },
                });
                const data = await response.json();
                this.subjects = data;
            } catch (error) {
                console.error("Error fetching subjects:", error);
                this.errormessage = "Failed to fetch subjects.";
            }
        }
    },
};
</script>
<!-- already added search funtinaliy -->