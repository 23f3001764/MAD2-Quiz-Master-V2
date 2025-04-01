<template>
    <nav class="navbar navbar-dark bg-dark px-3 d-flex justify-content-between">
        <router-link v-if="isuser" class="nav-link" to="/dashboard">
            <img src="@/assets/quizicon.jpg" alt="Quiz Icon" width="40" height="40" />
        </router-link>
        <router-link v-if="isadmin" class="nav-link" to="/admindashboard">
            <img src="@/assets/quizicon.jpg" alt="Quiz Icon" width="40" height="40" />
        </router-link>
        <a class="navbar-brand fw-bold text-white" href="#">Quiz Master App</a>
        <button class="navbar-toggler" type="button" @click="toggleMenu">☰</button>

        <ul v-if="menuVisible && isuser" class="navbar-nav ml-auto">
            <li class="nav-item">
                <router-link class="nav-link" to="/subject">Subject</router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
            </li>
            <li class="nav-item">
                <button class="btn btn-info" @click="generateCsv">Generate CSV</button>
            </li>
            <li class="nav-item">
                <button class="btn btn-info" @click="downloadCsv">Download CSV</button>
            </li>
            <li class="nav-item">
                <a class="nav-link text-danger" href="#" @click="logout">Logout</a>
            </li>
        </ul>

        <ul v-if="menuVisible && isadmin" class="navbar-nav ml-auto">
            <li class="nav-item">
                <router-link class="nav-link" to="/admindashboard">Dashboard</router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/adminsubject">Subjects</router-link>
            </li>
            <li class="nav-item">
                <a class="nav-link text-danger" href="#" @click="logout">Logout</a>
            </li>
        </ul>
    </nav>
</template>

<script>
export default {
    data() {
        return {
            menuVisible: false,
            isadmin: false,
            isuser: false,
            csvTaskId: null,  // Store task ID for downloading
        };
    },
    created() {
        this.fetchUserRole();
    },
    methods: {
        async fetchUserRole() {
            try {
                const token = localStorage.getItem("admintoken") || localStorage.getItem("usertoken");
                if (!token) {
                    this.isadmin = false;
                    this.isuser = false;
                    return;
                }

                const response = await fetch("/api/login", {
                    method: "GET",
                    headers: { Authorization: `Bearer ${token}` },
                });

                const data = await response.json();
                console.log("User data:", data);
                this.isadmin = data.isadmin;
                this.isuser = !data.isadmin;
            } catch (error) {
                console.error("Error fetching user role:", error);
                this.isadmin = false;
                this.isuser = false;
            }
        },
        toggleMenu() {
            this.menuVisible = !this.menuVisible;
        },

        async generateCsv() {
            console.log("Generating CSV...");
            const token = localStorage.getItem("usertoken");
            if (!token) {
                alert("You need to log in to generate CSV.");
                return;
            }

            try {
                const response = await fetch('/api/export', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                const data = await response.json();
                console.log("CSV generation response:", data);

                if (data.id) {
                    this.csvTaskId = data.id; 
                    alert("CSV generated successfully. Click 'Download CSV' to get the file.");
                } else {
                    alert("Error generating CSV: " + (data.message || "Unknown error"));
                }
            } catch (error) {
                console.error("Error generating CSV:", error);
                alert("An error occurred while generating CSV.");
            }
        },

        async downloadCsv() {
            if (!this.csvTaskId) {
                alert("First, generate the CSV file.");
                return;
            }

            console.log(`Downloading CSV with ID: ${this.csvTaskId}...`);
            try {
                window.location.href = `/api/csv_result/${this.csvTaskId}`;
            } catch (error) {
                console.error("Error downloading CSV:", error);
                alert("Failed to download CSV.");
            }
        },

        logout() {
            console.log("Logging out...");
            localStorage.removeItem("admintoken");
            localStorage.removeItem("usertoken");

            this.isadmin = false;
            this.isuser = false;
            this.menuVisible = false;

            this.$router.push("/login");
        },
    },
};
</script>

<style scoped>
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.navbar-nav {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 50px;
    right: 20px;
    background: #212529;
    padding: 10px;
    border-radius: 5px;
}

.navbar-toggler {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: white;
}

.nav-link {
    color: white;
    text-decoration: none;
    padding: 8px 12px;
}

.nav-link:hover {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}
</style>