<template>
    <div class="container mt-4">
        <div v-if="errormessage" class="alert alert-danger text-center ">
            {{ errormessage }}
            <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>
        <div v-if="successmessage" class="alert alert-success text-center ">
            {{ successmessage }}
            <button @click="successmessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="card p-4">
            <h2 class="text-center">Add New Quiz</h2>
            <form @submit.prevent="submitForm">
                <div class="form-group">
                    <label for="topic">Topic Name:</label>
                    <input type="text" id="topic" v-model="quiz.topic" class="form-control"
                        placeholder="Enter topic name" required />
                </div>

                <div class="form-group">
                    <label for="chname">Chapter Name:</label>
                    <input type="text" id="chname" v-model="quiz.chname" class="form-control" readonly />
                </div>

                <div class="form-group">
                    <label for="date">Date:</label>
                    <input type="date" id="date" v-model="quiz.date" class="form-control" required />
                </div>

                <div class="form-group">
                    <label for="duration">Duration (HH:MM):</label>
                    <input type="time" id="duration" v-model="quiz.duration" class="form-control" required />
                </div>

                <div class="form-group">
                    <label for="remarks">Remarks (Optional):</label>
                    <textarea id="remarks" v-model="quiz.remarks" class="form-control"
                        placeholder="Enter remarks"></textarea>
                </div>

                <button type="submit" class="btn btn-primary btn-block mt-3">Add Quiz</button>
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
                chname: this.$route.params.chname, 
                date: "",
                duration: "",
                remarks: ""
            },
            errormessage: null,
            successmessage: null
        };
    },
    methods: {
        async submitForm() {
            this.errormessage = null;
            this.successmessage = null;
            const token = localStorage.getItem("admintoken");

            if (!this.quiz.topic.trim() || !this.quiz.date || !this.quiz.duration) {
                this.errormessage = "Please fill all required fields.";
                return;
            }

            try {
                const response = await fetch("/api/quiz", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`
                    },
                    body: JSON.stringify(this.quiz)
                });

                const data = await response.json();

                if (response.ok) {
                    this.successmessage = "Quiz added successfully!";
                    setTimeout(() => {
                        this.$router.push(`/adminquiz/${this.quiz.chname}`);
                    }, 2000);
                } else {
                    this.errormessage = data.message || "Failed to add quiz.";
                }
            } catch (error) {
                console.error("Error:", error);
                this.errormessage = "An error occurred. Please try again.";
            }
        }
    }
};
</script>

<style scoped>
.form-group {
    margin-bottom: 15px;
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
