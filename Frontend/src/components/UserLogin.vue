<template>
  <div class="login-container">
    <div class="card login-card">
      <div class="card-body">
        <h2 class="text-center mb-4">Login</h2>
        <div v-if="errormessage" class="alert alert-danger text-center ">
          {{ errormessage }}
          <button @click="errormessage = null" class="btn-close" aria-label="Close"></button>
        </div>

        <form @submit.prevent="loginuser">
          <div class="mb-3">
            <label for="email" class="form-label">Email or Username</label>
            <input
              type="text"
              id="email"
              v-model="email"
              class="form-control"
              placeholder="Enter email or username"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              id="password"
              v-model="password"
              class="form-control"
              placeholder="Enter password"
              required
            />
          </div>
          <div class="text-center">
            <button type="submit" class="btn btn-primary w-100">Login</button>
          </div>
        </form>
        <p class="text-center mt-3">
          Don't have an account? <router-link to="/signup">Join Us</router-link>
        </p>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "LoginView",
  data() {
    return {
      email: "",
      password: "",
      errormessage: null, 
    };
  },
  methods: {
    async loginuser() {
      this.errormessage = null; 

      const payload = this.isEmail(this.email)
        ? { email: this.email, password: this.password }
        : { username: this.email, password: this.password };

      try {
        const response = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await response.json(); 

        if (!response.ok) {
          this.errormessage = data.message || "Login failed. Please try again.";
          console.error("Login failed:", data);
          return;
        }

        alert(`Logged in successfully! Welcome, ${data.username}`);

        if (data.isadmin) {
          localStorage.setItem("admintoken", data.token);
          this.$router.push("/admindashboard");
        } else {
          localStorage.setItem("usertoken", data.token);
          this.$router.push("/dashboard");
        }
        setTimeout(() => {
          window.location.reload();
        }, 100);

      } catch (error) {
        this.errormessage = "An unexpected error occurred. Please try again.";
        console.error("Login error:", error);
      }
    },

    isEmail(input) {
      return input.includes("@") && input.includes(".com");
    },
  },
};
</script>

<style>
.login-card {
  width: 400px;
  padding: 30px;
  border-radius: 12px;
  background: white;
  box-shadow: 0px 4px 20px rgba(255, 255, 255, 0.2);
}

</style>