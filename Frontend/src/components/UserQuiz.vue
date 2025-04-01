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
                                :class="attemptedQuizzes[quiz.id] ? 'btn-warning' : 'btn-info'">
                                {{ attemptedQuizzes[quiz.id] ? "Try Again" : "Start Quiz" }}
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
            attemptedQuizzes: {},
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
                this.checkAttemptedQuizzes();
            } catch (error) {
                console.error("Error fetching quizzes:", error);
                this.errormessage = "Failed to fetch quizzes.";
            }
        },
        async checkAttemptedQuizzes() {
            const token = localStorage.getItem("usertoken");
            const decodedToken = JSON.parse(atob(token.split(".")[1]));
            const user = decodedToken.sub;
            const userId = user.user_id;

            for (const quiz of this.quizzes) {
                try {
                    const response = await fetch(`/api/check/${userId}/${quiz.id}`, {
                        method: "GET",
                        headers: { Authorization: `Bearer ${token}` },
                    });

                    if (!response.ok) {
                        console.error(`Failed to check quiz ${quiz.id}`);
                        continue;
                    }

                    const data = await response.json();
                    this.$set(this.attemptedQuizzes, quiz.id, data.message === "True");
                } catch (error) {
                    console.error("Error checking quiz attempt:", error);
                }
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
