<template>
    <div class="container">
        <h2 class="text-center">Admin Dashboard</h2>

        <div class="row">
            <div class="col-md-6">
                <div class="card text-white bg-primary mb-3">
                    <div class="card-body text-center">
                        <h5 class="card-title">Total Users</h5>
                        <p class="card-text display-4">{{ totalUsers }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card text-white bg-success mb-3">
                    <div class="card-body text-center">
                        <h5 class="card-title">Total Quizzes Attempted</h5>
                        <p class="card-text display-4">{{ totalAttempts }}</p>
                    </div>
                </div>
            </div>
        </div>

        <h3>User List</h3>
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Username</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.username }}</td>
                    <td>
                        <button class="btn btn-primary btn-sm" @click="viewUserDetails(user.id)">
                            View Details
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <h3>Users vs. Quizzes Attempted</h3>
        <canvas id="userChart"></canvas>
    </div>
</template>

<script>
export default {
    data() {
        return {
            users: [],
            scores: [],
            userQuizCount: {},
            totalUsers: 0,
            totalAttempts: 0,
            chart: null
        };
    },
    mounted() {
        this.fetchUsers();
        this.fetchScores();
    },
    methods: {
        async fetchUsers() {
            const token = localStorage.getItem("admintoken");
            if (!token) return;

            try {
                const response = await fetch("/api/user", {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (!response.ok) throw new Error("Failed to fetch users");
                const allUsers = await response.json();

                this.users = allUsers.filter(user => !user.is_admin);
                this.totalUsers = this.users.length;
            } catch (error) {
                console.error(error);
            }
        },

        async fetchScores() {
            const token = localStorage.getItem("admintoken");
            if (!token) return;

            try {
                const response = await fetch("/api/score", {
                    headers: { Authorization: `Bearer ${token}` }
                });
                if (!response.ok) throw new Error("Failed to fetch scores");
                this.scores = await response.json();

                this.totalAttempts = this.scores.length;

                this.userQuizCount = {};
                this.scores.forEach(score => {
                    if (!this.userQuizCount[score.username]) {
                        this.userQuizCount[score.username] = new Set();
                    }
                    this.userQuizCount[score.username].add(score.quiz_id);
                });

                Object.keys(this.userQuizCount).forEach(user => {
                    this.userQuizCount[user] = this.userQuizCount[user].size;
                });

                this.renderChart();
            } catch (error) {
                console.error(error);
            }
        },

        viewUserDetails(userId) {
            this.$router.push(`/adminuser/${userId}`);
        },

        renderChart() {
            if (this.chart) this.chart.destroy();

            const labels = Object.keys(this.userQuizCount);
            const data = Object.values(this.userQuizCount);

            setTimeout(() => {
                const ctx = document.getElementById("userChart").getContext("2d");
                this.chart = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels,
                        datasets: [{
                            label: "Quizzes Attempted",
                            data,
                            backgroundColor: "rgba(75, 192, 192, 0.6)"
                        }]
                    },
                    options: { responsive: true }
                });
            }, 500);
        }
    }
};
</script>

<style scoped>
.container {
    max-width: 900px;
    margin: auto;
    padding: 20px;
}

h2,
h3 {
    font-weight: bold;
    margin-bottom: 20px;
}

.card {
    border-radius: 10px;
    padding: 20px;
    text-align: center;
}

.card-title {
    font-size: 1.2rem;
    font-weight: bold;
}

.display-4 {
    font-size: 2.5rem;
    font-weight: bold;
}

.table {
    margin-bottom: 20px;
}
</style>
