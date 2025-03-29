<template>
    <div class="container mt-4">
        <div v-if="errorMessage" class="alert alert-danger text-center">
            {{ errorMessage }}
            <button @click="errorMessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="display-4 fw-bold">Quiz: {{ quizName }}</h2>
            <h4 class="text-danger">Time Left: {{ formattedTime }}</h4>
        </div>

        <div v-if="questions.length">
            <div v-for="(question, index) in questions" :key="question.id" class="mb-4">
                <h5>{{ index + 1 }}. {{ question.question }}</h5>
                <div v-for="answer in question.answers" :key="answer.id" class="form-check">
                    <input type="radio" class="form-check-input" :name="'question_' + question.id"
                        :id="'answer_' + answer.id" :value="answer.id" v-model="selectedAnswers[question.id]" />
                    <label class="form-check-label" :for="'answer_' + answer.id">
                        {{ answer.answer }}
                    </label>
                </div>
            </div>

            <div class="mt-4">
                <button @click="submitQuiz" class="btn btn-success me-3">Submit</button>
                <button @click="cancelQuiz" class="btn btn-danger">Cancel</button>
            </div>
        </div>

        <div v-else class="alert alert-info text-center">Loading quiz...</div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            quizId: this.$route.params.quiz_id,
            quizName: "",
            duration: 0,
            questions: [],
            selectedAnswers: {},
            correctAnswers: {},
            timer: null,
            timeLeft: 0,
            errorMessage: null,
            previousAttempts: [],
            attempt: 1
        };
    },
    computed: {
        formattedTime() {
            const minutes = Math.floor(this.timeLeft / 60);
            const seconds = this.timeLeft % 60;
            return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
        }
    },
    created() {
        this.fetchQuizDetails();
        this.fetchQuestions();
        this.fetchPreviousAttempts();
    },
    methods: {
        async fetchQuizDetails() {
            const token = localStorage.getItem("usertoken");
            try {
                const response = await fetch(`/api/quiz/${this.quizId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (!response.ok) throw new Error("Failed to fetch quiz details");

                const data = await response.json();
                this.quizName = data.chname;
                this.duration = this.parseDuration(data.duration);
                this.timeLeft = this.duration;
                this.startTimer();
            } catch (error) {
                this.errorMessage = error.message;
            }
        },

        async fetchQuestions() {
            const token = localStorage.getItem("usertoken");
            try {
                const response = await fetch(`/api/ques/${this.quizId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (!response.ok) throw new Error("Failed to fetch questions");

                const data = await response.json();
                this.questions = data;

                for (let question of this.questions) {
                    await this.fetchAnswers(question);
                }
            } catch (error) {
                this.errorMessage = error.message;
            }
        },
        startTimer() {
            this.timer = setInterval(() => {
                if (this.timeLeft > 0) {
                    this.timeLeft--;
                } else {
                    this.submitQuiz();
                }
            }, 1000);
        },

        async fetchAnswers(question) {
            const token = localStorage.getItem("usertoken");
            try {
                const response = await fetch(`/api/answer/${question.id}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (!response.ok) throw new Error(`Failed to fetch answers for question ${question.id}`);

                const answers = await response.json();
                question.answers = answers;
                this.correctAnswers[question.id] = answers.find(a => a.is_true)?.id || null;
            } catch (error) {
                this.errorMessage = error.message;
            }
        },

        async fetchPreviousAttempts() {
            const token = localStorage.getItem("usertoken");
            const decodedToken = JSON.parse(atob(token.split(".")[1]));
            const user = decodedToken.sub;
            const userId = user.user_id;

            try {
                const response = await fetch(`/api/scores/${this.quizId}/${userId}`, {
                    method: "GET",
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (response.ok) {
                    this.previousAttempts = await response.json();
                    this.attempt = this.previousAttempts.length + 1;
                }
            } catch (error) {
                console.error("Error fetching previous attempts:", error);
            }
        },

        async submitQuiz() {
            clearInterval(this.timer);
            let totalQuestions = this.questions.length;
            let score = 0;

            for (let questionId in this.selectedAnswers) {
                if (this.selectedAnswers[questionId] === this.correctAnswers[questionId]) {
                    score++;
                }
            }

            let normalizedScore = (score / totalQuestions) * 100;

            await this.saveScore(normalizedScore);
        },

        async saveScore(score) {
            const token = localStorage.getItem("usertoken");

            if (!token) {
                console.error("No token found in localStorage");
                return;
            }

            const decodedToken = JSON.parse(atob(token.split(".")[1]));
            const user = decodedToken.sub;
            const userId = user.user_id;
            const username = user.username;

            const scoreData = {
                user_id: userId,
                quiz_id: this.quizId,
                score: score,
                username: username,
                attempt: this.attempt
            };

            console.log("Sending Score Data:", scoreData);

            try {
                const response = await fetch(`/api/scores/${this.quizId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`
                    },
                    body: JSON.stringify(scoreData)
                });

                if (!response.ok) throw new Error("Failed to save score");

                this.$router.push("/dashboard");
            } catch (error) {
                this.errorMessage = error.message;
            }
        },

        parseDuration(duration) {
            if (!duration) return 300;
            const [hours, minutes] = duration.split(":").map(Number);
            return hours * 3600 + minutes * 60;
        }
    },
    beforeUnmount() {
        clearInterval(this.timer);
    }
};
// again a commit for milestone 6
</script>
