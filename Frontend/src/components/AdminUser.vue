<template>
    <div class="container">
        <div v-if="scores.length" class="average-score-card">
            <div class="card bg-info text-white text-center p-3">
                <h4>Average Score</h4>
                <h2>{{ averageScore.toFixed(2) }}%</h2>
            </div>
        </div>
        <h2 class="text-center">User Quiz Scores</h2>

        <table class="table">
            <thead>
                <tr>
                    <th>Quiz</th>
                    <th>Topic</th>
                    <th>Score</th>
                    <th>Attempt</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="score in scores" :key="score.id">
                    <td>{{ score.quiz_id }}</td>
                    <td>{{ score.quiz_name }}</td>
                    <td>{{ score.score }}</td>
                    <td>{{ score.attempt }}</td>
                </tr>
            </tbody>
        </table>

        <canvas id="scoreChart"></canvas>
    </div>
</template>

<script>
export default {
    data() {
        return {
            scores: [],
            chart: null,
            userID: this.$route.params.uid, 
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
            const token = localStorage.getItem("admintoken");
            if (!token) return;
            this.userID = this.$route.params.uid;
            try {
                const response = await fetch(`/api/sco/${this.userID}`, {
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

        renderChart() {
            if (this.chart) this.chart.destroy();

            const labels = Object.keys(this.chartData); // Topics
            const data = Object.values(this.chartData); // Scores

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
</style>
