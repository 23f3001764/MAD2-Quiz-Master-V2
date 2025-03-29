<template>
    <div class="logup-container">
        <div class="card logup-card">
            <div class="card-body">
                <h2 class="text-center mb-4">Signup</h2>

                <div v-if="errormessage" class="alert alert-danger text-center ">
                    {{ errormessage }}
                    <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
                </div>

                <div v-if="successMessage" class="alert alert-success text-center ">
                    {{ successMessage }}
                    <button @click="successMessage = null" class="btn-close" aria-label="Close"></button>
                </div>

                <div v-if="usernameMessage" class="alert alert-info text-center ">
                    {{ usernameMessage }}
                    <button @click="usernameMessage = null" class="btn-close" aria-label="Close"></button>
                </div>

                <form @submit.prevent="logupuser">
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="text" id="email" v-model="email" class="form-control" placeholder="Enter Email"
                            required />
                    </div>

                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" id="username" v-model="username" class="form-control"
                            placeholder="Enter Username" required />
                        <button @click.prevent="checkAvailability" class="btn btn-secondary mt-2">Check
                            Availability</button>
                    </div>

                    <div class="mb-3">
                        <label for="name" class="form-label">Full Name</label>
                        <input type="text" id="name" v-model="name" class="form-control" placeholder="Enter Full Name"
                            required />
                    </div>

                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" id="password" v-model="password" class="form-control"
                            placeholder="Enter Password" required />
                    </div>

                    <div class="text-center">
                        <button type="submit" class="btn btn-primary w-100">Signup</button>
                    </div>
                </form>

                <p class="text-center mt-3">
                    Already have an account? <router-link to="/login">Login</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "LogupView",
    data() {
        return {
            email: "",
            username: "",
            name: "",
            password: "",
            errormessage: null,
            successMessage: null, 
            usernameMessage: null, 
        };
    },
    methods: {
        async logupuser() {
            this.errormessage = null;
            this.successMessage = null; // Reset success message

            try {
                const payload = {
                    email: this.email,
                    username: this.username,
                    name: this.name,
                    password: this.password,
                };

                const response = await fetch("/api/signup", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload),
                });

                const data = await response.json();

                if (!response.ok) {
                    this.errormessage = data.message || "Sign-up failed. Please try again.";
                    console.error("Sign-up failed:", data);
                    return;
                }

                this.successMessage =   `Signup successful! Welcome, ${payload.username}. Redirecting to login...`;

                this.email = "";
                this.username = "";
                this.name = "";
                this.password = "";

                setTimeout(() => {
                    this.$router.push("/login");
                }, 3000);

            } catch (error) {
                this.errormessage = "An unexpected error occurred. Please try again.";
                console.error("Sign-up error:", error);
            }
        },

        async checkAvailability() {
            this.usernameMessage = null;
            if (!this.username.trim()) {
                this.usernameMessage = "Please enter a username first.";
                return;
            }

            try {
                const response = await fetch(`/api/signup/${this.username}`, {
                    method: "GET",
                    headers: { "Content-Type": "application/json" },
                });

                const data = await response.json();

                if (response.ok) {
                    this.usernameMessage = "Username is available!";
                } else {
                    this.usernameMessage = "Sorry, this username is already taken.";
                }
            } catch (error) {
                this.usernameMessage = "Error checking username availability.";
                console.error("Check availability error:", error);
            }
        },
    },
};
</script>

<style>
.logup-card {
    width: 400px;
    padding: 30px;
    border-radius: 12px;
    background: white;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
}

</style>
