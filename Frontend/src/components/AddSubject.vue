<template>
    <div class="container">
        <div v-if="errormessage" class="alert alert-danger text-center">
            {{ errormessage }}
            <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>
        <div v-if="successmessage" class="alert alert-success text-center">
            {{ successmessage }}
            <button @click="successmessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="add-subject-card">
            <h2 class="text-center">Add New Subject</h2>
            <form @submit.prevent="submitForm">
                <div class="form-group">
                    <label for="subjectName">Subject Name:</label>
                    <input type="text" id="subjectName" v-model="subject.sname" placeholder="Enter subject name"
                        required />
                </div>
                <div class="form-group">
                    <label for="subjectDescription">Description:</label>
                    <textarea id="subjectDescription" v-model="subject.description"
                        placeholder="Enter subject description"></textarea>
                </div>
                <button type="submit" class="btn-primary">Add Subject</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            subject: {
                sname: "",
                description: "",
            },
            errormessage: null,
            successmessage: null,
        };
    },
    methods: {
        async submitForm() {
            this.errormessage = null;
            this.successmessage = null;
            const payload = this.subject;
            const token = localStorage.getItem("admintoken");
            console.log(token);

            try {
                const response = await fetch("/api/subject", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify(payload),
                });
                console.log(response);

                const data = await response.json();

                if (response.ok) {
                    this.successmessage = "Subject added successfully!";
                    setTimeout(() => {
                        this.$router.push("/adminsubject");
                    }, 2000);
                } else {
                    console.error("Error:", data.message);
                    this.errormessage = data.message || "Failed to add subject.";
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
