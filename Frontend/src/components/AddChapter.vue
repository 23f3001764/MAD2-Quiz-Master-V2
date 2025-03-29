<template>
    <div class="container">
        <div v-if="errormessage" class="alert alert-danger text-center ">
            {{ errormessage }}
            <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>
        <div v-if="successmessage" class="alert alert-success text-center ">
            {{ successmessage }}
            <button @click="successmessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <div class="add-chapter-card">
            <h2 class="text-center">Add New Chapter</h2>
            <form @submit.prevent="submitForm">
                <div class="form-group">
                    <label for="chapterName">Chapter Name:</label>
                    <input type="text" id="chapterName" v-model="chapter.chname" placeholder="Enter chapter name"
                        required />
                </div>
                <div class="form-group">
                    <label for="chapterDescription">Description:</label>
                    <textarea id="chapterDescription" v-model="chapter.description"
                        placeholder="Enter chapter description"></textarea>
                </div>
                <button type="submit" class="btn-primary">Add Chapter</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            chapter: {
                chname: "",
                description: "",
                sname: "", 
            },
            errormessage: null,
            successmessage: null,
        };
    },
    created() {
        this.chapter.sname = this.$route.params.sname; 
    },
    methods: {
        async submitForm() {
            this.errormessage = null;
            this.successmessage = null;
            const token = localStorage.getItem("admintoken");

            try {
                const response = await fetch("/api/chapter", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify(this.chapter),
                });

                const data = await response.json();

                if (response.ok) {
                    this.successmessage = "Chapter added successfully!";
                    setTimeout(() => {
                        this.$router.push(`/adminchapter/${this.chapter.sname}`);
                    }, 2000);
                } else {
                    this.errormessage = data.message || "Failed to add chapter.";
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
