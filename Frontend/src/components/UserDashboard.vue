<template>
    <div class="container">
        <div v-if="scores.length" class="average-score-card">
            <div class="card bg-info text-white text-center p-3">
                <h4>Average Score</h4>
                <h2>{{ averageScore.toFixed(2) }}%</h2>
            </div>
        </div>

        <h2 class="text-center mt-4">User Quiz Scores</h2>

        <table class="table">
            <thead>
                <tr>
                    <th>Quiz</th>
                    <th>Topic</th>
                    <th>Score</th>
                    <th>Attempt</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="score in scores" :key="score.id">
                    <td>{{ score.quiz_id }}</td>
                    <td>{{ score.quiz_name }}</td>
                    <td>{{ score.score.toFixed(2) }}</td>
                    <td>{{ score.attempt }}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" @click="deleteScore(score.id)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <canvas id="scoreChart"></canvas>

        <div class="text-center mt-4">
            <button class="btn btn-primary btn-lg" @click="goToSubjects">Let's See Subjects</button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            scores: [],
            chart: null,
            chartData: {}
        };
    },
    computed: {
        averageScore() {
            if (this.scores.length === 0) return 0;
            const total = this.scores.reduce((sum, score) => sum + score.score, 0);
            return total / this.scores.length;
        }
    },
    mounted() {
        this.fetchScores();
    },
    methods: {
        async fetchScores() {
            const token = localStorage.getItem("usertoken");
            if (!token) return;

            try {
                const userId = JSON.parse(atob(token.split(".")[1])).sub.user_id;
                const response = await fetch(`/api/sco/${userId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (!response.ok) throw new Error("Failed to fetch scores");
                const scoreData = await response.json();

                const quizRequests = scoreData.map(score =>
                    fetch(`/api/quiz/${score.quiz_id}`, {
                        headers: { Authorization: `Bearer ${token}` }
                    }).then(res => res.json())
                );

                const quizzes = await Promise.all(quizRequests);

                this.scores = scoreData.map((score, index) => ({
                    ...score,
                    quiz_name: quizzes[index].topic || `Quiz ${score.quiz_id}`
                }));

                this.chartData = this.scores.reduce((acc, score) => {
                    acc[score.quiz_name] = (acc[score.quiz_name] || 0) + score.score;
                    return acc;
                }, {});

                this.renderChart();
            } catch (error) {
                console.error(error);
            }
        },

        async deleteScore(scoreId) {
            const token = localStorage.getItem("usertoken");
            if (!token) return;

            try {
                await fetch(`/api/score/${scoreId}`, {
                    method: "DELETE",
                    headers: { Authorization: `Bearer ${token}` }
                });

                this.fetchScores();
            } catch (error) {
                console.error(error);
            }
        },

        renderChart() {
            if (this.chart) this.chart.destroy();

            const labels = Object.keys(this.chartData); 
            const data = Object.values(this.chartData); 

            setTimeout(() => {
                const ctx = document.getElementById("scoreChart").getContext("2d");
                this.chart = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels,
                        datasets: [{
                            label: "Scores",
                            data,
                            backgroundColor: "rgba(54, 162, 235, 0.6)"
                        }]
                    },
                    options: { responsive: true }
                });
            }, 500);
        },

        goToSubjects() {
            this.$router.push("/subject"); 
        }
    }
};
</script>

<style scoped>
.container {
    max-width: 700px;
    margin: auto;
    padding: 20px;
}

h2 {
    font-weight: bold;
    margin-bottom: 20px;
}

.table {
    margin-bottom: 20px;
}

.btn-lg {
    width: 80%;
    font-size: 1.2rem;
    padding: 12px;
}

.average-score-card {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.card {
    width: 100%;
    max-width: 300px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(33, 30, 30, 0.1);
}
/* again a commit for milestone 5 */
</style>
