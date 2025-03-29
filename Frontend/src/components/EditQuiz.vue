<template>
    <div class="container">
        <div v-if="errormessage" class="alert alert-danger text-center">
            {{ errormessage }}
            <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>
        <div v-if="successmessage" class="alert alert-success text-center ">
            {{ successmessage }}
            <button @click="successmessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="edit-quiz-card">
            <h2 class="text-center">Edit Quiz</h2>
            <form @submit.prevent="submitForm">
                <div class="form-group">
                    <label for="topic">Quiz Topic:</label>
                    <input type="text" id="topic" v-model="quiz.topic" required />
                </div>
                <div class="form-group">
                    <label for="date">Date:</label>
                    <input type="date" id="date" v-model="quiz.date" required />
                </div>
                <div class="form-group">
                    <label for="duration">Duration:</label>
                    <input type="time" id="duration" v-model="quiz.duration" required />
                </div>
                <div class="form-group">
                    <label for="remarks">Remarks:</label>
                    <textarea id="remarks" v-model="quiz.remarks"></textarea>
                </div>
                <button type="submit" class="btn-primary">Save Changes</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            quiz: {
                topic: "",
                date: "",
                duration: "",
                remarks: "",
            },
            errormessage: null,
            successmessage: null,
        };
    },
    mounted() {
        this.fetchQuiz();
    },
    methods: {
        async fetchQuiz() {
            const token = localStorage.getItem("admintoken");
            const quizId = this.$route.params.id;
            try {
                const response = await fetch(`/api/quiz/${quizId}`, {
                    method: "GET",
                    headers: { Authorization: `Bearer ${token}` },
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch quiz data");
                }

                const data = await response.json();
                this.quiz = data;
            } catch (error) {
                console.error("Error fetching quiz:", error);
                this.errormessage = "Failed to load quiz data.";
            }
        },
        async submitForm() {
            this.errormessage = null;
            this.successmessage = null;
            const token = localStorage.getItem("admintoken");
            const quizId = this.$route.params.id;

            try {
                const response = await fetch(`/api/quiz/${quizId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify(this.quiz),
                });

                const data = await response.json();

                if (response.ok) {
                    this.successmessage = "Quiz updated successfully!";
                    setTimeout(() => {
                        this.$router.push(`/adminquiz/${this.quiz.chname}`);
                    }, 2000);
                } else {
                    this.errormessage = data.message || "Failed to update quiz.";
                }
            } catch (error) {
                this.errormessage = "An error occurred. Please try again.";
                console.error("Error:", error);
            }
        },
    },
};
</script>

<style scoped>
.form-group {
    margin-bottom: 15px;
    text-align: left;
}

label {
    font-weight: bold;
}

input,
textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
    box-sizing: border-box;
    font-size: 14px;
}

.btn-primary {
    width: 100%;
    padding: 12px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.3s ease;
}

.btn-primary:hover {
    background-color: #0056b3;
}

</style>
