<template>
    <div class="container mt-4">
        <div v-if="successmessage" class="alert alert-success text-center">{{ successmessage }}</div>

        <div class="card p-4">
            <h3 class="text-center">{{ isEditingQuestion ? 'Edit Question' : 'Add New Question' }}</h3>
            <form @submit.prevent="submitQuestion">
                <div class="form-group">
                    <label>Question:</label>
                    <textarea v-model="questionText" class="form-control" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary mt-2">
                    {{ isEditingQuestion ? 'Update Question' : 'Add Question' }}
                </button>
                <button v-if="isEditingQuestion" @click="cancelEditQuestion" class="btn btn-secondary mt-2 ms-2">
                    Cancel
                </button>
            </form>
        </div>

        <h2 class="text-center mt-4">Quiz Questions</h2>

        <div v-if="questions.length">
            <div v-for="question in questions" :key="question.id" class="card my-3 p-3">
                <div class="d-flex justify-content-between align-items-center">
                    <h5>{{ question.question }}</h5>
                    <div>
                        <button @click="editQuestion(question)" class="btn btn-warning btn-sm me-2">Edit</button>
                        <button @click="deleteQuestion(question.id)" class="btn btn-danger btn-sm">Delete</button>
                    </div>
                </div>

                <!-- Answer Form -->
                <div class="mt-3">
                    <h6>{{ isEditingAnswer && editingAnswerQuestionId === question.id ? 'Edit Answer' : 'Add Answer' }}
                    </h6>
                    <form @submit.prevent="submitAnswer(question.id)">
                        <div class="d-flex">
                            <input type="text" v-model="answerInputs[question.id]" required
                                placeholder="Enter answer" />
                            <select v-model="isCorrect" class="form-select me-2">
                                <option :value="true">Correct</option>
                                <option :value="false">Wrong</option>
                            </select>
                            <button type="submit" class="btn btn-primary">
                                {{ isEditingAnswer && editingAnswerQuestionId === question.id ? 'Update' : 'Add' }}
                            </button>
                            <button v-if="isEditingAnswer && editingAnswerQuestionId === question.id"
                                @click="cancelEditAnswer" class="btn btn-secondary ms-2">
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>

                <!-- Answer List -->
                <div v-if="answers[question.id]?.length">
                    <ul class="list-group mt-3">
                        <li v-for="answer in answers[question.id]" :key="answer.id"
                            class="list-group-item d-flex justify-content-between"
                            :class="{ 'list-group-item-success': answer.is_true, 'list-group-item-danger': !answer.is_true }">
                            {{ answer.answer }}
                            <div>
                                <button @click="editAnswer(answer, question.id)"
                                    class="btn btn-warning btn-sm me-2">Edit</button>
                                <button @click="deleteAnswer(answer.id, question.id)"
                                    class="btn btn-danger btn-sm">Delete</button>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div v-else class="alert alert-info text-center">No questions available.</div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            questions: [],
            answers: {}, // Store answers per question ID
            questionText: "",
            answerInputs: {},
            isCorrect: false,
            isEditingQuestion: false,
            isEditingAnswer: false,
            editingQuestionId: null,
            editingAnswerId: null,
            editingAnswerQuestionId: null,
            successmessage: null,
            quiz_id: this.$route.params.quiz_id
        };
    },
    created() {
        this.fetchQuestions();
    },
    methods: {
        async fetchQuestions() {
            const token = localStorage.getItem("admintoken");
            try {
                const response = await fetch(`/api/ques/${this.quiz_id}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                if (!response.ok) throw new Error("Failed to fetch questions.");

                this.questions = await response.json();

                // Fetch answers for each question
                this.questions.forEach(q => this.fetchAnswers(q.id));
            } catch (error) {
                console.error(error);
            }
        },
        async fetchAnswers(question_id) {
            const token = localStorage.getItem("admintoken");
            try {
                const response = await fetch(`/api/answer/${question_id}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (!response.ok) return;

                const fetchedAnswers = await response.json();
                console.log(`Fetched answers for question ${question_id}:`, fetchedAnswers);

                // Ensure reactivity in Vue 3
                this.answers = { ...this.answers, [question_id]: fetchedAnswers };

                console.log(`Updated answers state:`, this.answers);
            } catch (error) {
                console.error(error);
            }
        },
        async submitQuestion() {
            try {
                const method = this.isEditingQuestion ? "PUT" : "POST";
                const endpoint = this.isEditingQuestion ? `/api/question/${this.editingQuestionId}` : `/api/ques/${this.quiz_id}`;
                const token = localStorage.getItem("admintoken");

                const response = await fetch(endpoint, {
                    method,
                    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
                    body: JSON.stringify({ question: this.questionText })
                });

                if (!response.ok) throw new Error("Failed to save question.");

                this.successmessage = this.isEditingQuestion ? "Question updated successfully!" : "Question added successfully!";
                this.cancelEditQuestion();
                this.fetchQuestions();
            } catch (error) {
                console.error(error);
            }
        },
        editQuestion(question) {
            this.isEditingQuestion = true;
            this.questionText = question.question;
            this.editingQuestionId = question.id;
        },
        async deleteQuestion(id) {
            if (!confirm("Are you sure?")) return;
            try {
                const token = localStorage.getItem("admintoken");
                await fetch(`/api/question/${id}`, { method: "DELETE", headers: { Authorization: `Bearer ${token}` } });
                this.fetchQuestions();
            } catch (error) {
                console.error(error);
            }
        },
        cancelEditQuestion() {
            this.isEditingQuestion = false;
            this.questionText = "";
        },
        async submitAnswer(question_id) {
            try {
                const method = this.isEditingAnswer ? "PUT" : "POST";
                const endpoint = this.isEditingAnswer ? `/api/ans/${this.editingAnswerId}` : `/api/answer/${question_id}`;
                const token = localStorage.getItem("admintoken");

                await fetch(endpoint, {
                    method,
                    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
                    body: JSON.stringify({
                        answer: this.answerInputs[question_id],is_true: this.isCorrect})
                });
                this.cancelEditAnswer();
                this.fetchAnswers(question_id);
            } catch (error) {
                console.error(error);
            }
        },
        editAnswer(answer, question_id) {
            this.isEditingAnswer = true;
            this.answerText = answer.answer;
            this.isCorrect = answer.is_true;
            this.editingAnswerId = answer.id;
            this.editingAnswerQuestionId = question_id;
        },
        async deleteAnswer(id, question_id) {
            if (!confirm("Are you sure?")) return;
            const token = localStorage.getItem("admintoken");
            await fetch(`/api/ans/${id}`, { method: "DELETE", headers: { Authorization: `Bearer ${token}` } });
            this.fetchAnswers(question_id);
        },
        cancelEditAnswer() {
            this.isEditingAnswer = false;
            this.answerText = "";
        }
    }
};
</script>
