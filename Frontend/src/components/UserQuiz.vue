<template>
    <div class="container mt-4">
        <div v-if="errormessage"
            class="alert alert-danger text-center fade-in d-flex justify-content-between align-items-center">
            <span>{{ errormessage }}</span>
            <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="display-1 fw-bold">Quizzes for {{ chname }}</h2>
        </div>

        <div class="mb-3">
            <input type="text" v-model="searchQuery" class="form-control" placeholder="Search chapters..." />
        </div>

        <div v-if="filteredQuizzes.length">
            <table class="table table-hover table-bordered">
                <thead class="table-dark">
                    <tr>
                        <th>#</th>
                        <th>Topic Name</th>
                        <th>Chapter Name</th>
                        <th>Duration</th>
                        <th>Date of creation</th>
                        <th>Remarks</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(quiz, index) in filteredQuizzes" :key="quiz.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ quiz.topic }}</td>
                        <td>{{ quiz.chname }}</td>
                        <td>{{ formatDuration(quiz.duration) }}</td>
                        <td>{{ quiz.date }}</td>
                        <td>{{ quiz.remarks }}</td>
                        <td>
                            <router-link :to="'/question/' + quiz.id" class="btn btn-sm"
                                :class="hasAttempted(quiz.id) ? 'btn-warning' : 'btn-info'">
                                {{ hasAttempted(quiz.id) ? "Try Again" : "Start Quiz" }}
                            </router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="alert alert-info text-center">No Quizzes available.</div>
        <div class="text-center mt-4">
            <h5 class="text-info">More Quizzes Coming Soon...</h5>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            quizzes: [],
            searchQuery: "",
            errormessage: null,
            chname: this.$route.params.chname,
            attemptedQuizIds: new Set(),
        };
    },
    computed: {
        filteredQuizzes() {
            return this.quizzes.filter(quiz =>
                quiz.topic.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        },
    },
    created() {
        this.fetchQuizzes();
        this.fetchUserScores();
    },
    methods: {
        async fetchQuizzes() {
            const token = localStorage.getItem("usertoken");
            try {
                const response = await fetch(`/api/quiz/${this.chname}`, {
                    method: "GET",
                    headers: { Authorization: `Bearer ${token}` },
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch quizzes.");
                }

                const data = await response.json();
                this.quizzes = data;
            } catch (error) {
                console.error("Error fetching quizzes:", error);
                this.errormessage = "Failed to fetch quizzes.";
            }
        },
        async fetchUserScores() {
            const token = localStorage.getItem("usertoken");
            try {
                const response = await fetch("/api/score", {
                    method: "GET",
                    headers: { Authorization: `Bearer ${token}` },
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch user scores.");
                }

                const data = await response.json();

                this.attemptedQuizIds = new Set(data.map(score => score.quiz_id));
            } catch (error) {
                console.error("Error fetching user scores:", error);
                this.errormessage = "Failed to fetch scores.";
            }
        },
        hasAttempted(quizId) {
            return this.attemptedQuizIds.has(quizId);
        },
        formatDuration(duration) {
            if (!duration) return "";
            const [hours, minutes] = duration.split(":").map(Number);
            let result = "";
            if (hours > 0) result += `${hours} hour${hours > 1 ? "s" : ""} `;
            if (minutes > 0) result += `${minutes} minute${minutes > 1 ? "s" : ""}`;
            return result.trim();
        }
    },
};
</script>
