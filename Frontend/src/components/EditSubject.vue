<template>
    <div class="container">
        <div v-if="errormessage" class="alert alert-danger text-center ">
            {{ errormessage }}
            <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>
        <div v-if="successmessage" class="alert alert-success text-center">
            {{ successmessage }}
            <button @click="successmessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="add-subject-card">
            <h2 class="text-center">Edit {{ subject.sname }}</h2>
            <form @submit.prevent="submitForm">
                <div class="form-group">
                    <label for="subjectName">Subject Name:</label>
                    <input type="text" id="subjectName" v-model="subject.sname" :placeholder="subject.sname" required />
                </div>
                <div class="form-group">
                    <label for="subjectDescription">Description:</label>
                    <textarea id="subjectDescription" v-model="subject.description"
                        :placeholder="subject.description"></textarea>
                </div>
                <button type="submit" class="btn-primary">Edit Subject</button>
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
    mounted() {
        this.fetchSubject();
    },
    methods: {
        async fetchSubject() {
            const token = localStorage.getItem("admintoken");
            const subjectId = this.$route.params.id;
            try {
                const response = await fetch(`/api/subject/${subjectId}`, {
                    method: "GET",
                    headers: { Authorization: `Bearer ${token}` },
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch subject");
                }

                const data = await response.json();
                this.subject = data;
            } catch (error) {
                console.error("Error fetching subject:", error);
                this.errormessage = "Failed to load subject data.";
            }
        },
        async submitForm() {
            this.errormessage = null;
            this.successmessage = null;

            const token = localStorage.getItem("admintoken");
            const subjectId = this.$route.params.id; 

            try {
                const response = await fetch(`/api/subject/${subjectId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify(this.subject),
                });

                const data = await response.json();

                if (response.ok) {
                    this.successmessage = "Subject edited successfully!";
                    setTimeout(() => {
                        this.$router.push("/adminsubject");
                    }, 2000);
                } else {
                    this.errormessage = data.message || "Failed to edit subject.";
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
