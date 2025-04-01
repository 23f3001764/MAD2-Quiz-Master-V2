<template>
    <div class="container mt-4">
        <div v-if="errormessage" class="alert alert-danger text-center ">
            {{ errormessage }}
            <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="display-1 fw-bold">Quizzes</h2>
            <router-link :to="'/addquiz/' + chname" class="btn btn-primary btn-lg">+ Add Quiz</router-link>
        </div>

        <div class="mb-3">
            <input type="text" v-model="searchQuery" class="form-control" placeholder="Search Quiz..." />
        </div>

        <!-- Quizzes Table -->
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
                            <router-link :to="'/adminquestion/' + quiz.id" class="btn btn-info btn-sm me-2">
                                View Questions
                            </router-link>
                            <router-link :to="'/editQuiz/' + quiz.id" class="btn btn-warning btn-sm me-2">
                                Edit
                            </router-link>
                            <button @click="deleteQuiz(quiz.id)" class="btn btn-danger btn-sm">
                                Delete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="alert alert-info text-center">No Quiz available.</div>
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
    },
    methods: {
        async fetchQuizzes() {
            const token = localStorage.getItem("admintoken");
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
        async deleteQuiz(quizId) {
            const token = localStorage.getItem("admintoken");

            if (!confirm("Are you sure you want to delete this quiz?")) return;

            try {
                const response = await fetch(`/api/quiz/${quizId}`, { 
                    method: "DELETE",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    this.errormessage = errorData.message || "Failed to delete quiz.";
                    return;
                }

                this.quizzes = this.quizzes.filter(quiz => quiz.id !== quizId);
            } catch (error) {
                console.error("Error deleting quiz:", error);
                this.errormessage = "An error occurred while deleting the quiz.";
            }
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
