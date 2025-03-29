<template>
    <nav class="navbar navbar-dark bg-dark px-3 d-flex justify-content-between">
        <router-link v-if = "isuser"class="nav-link" to="/dashboard"><img src="@/assets/quizicon.jpg" alt="Quiz Icon" width="40" height="40"  /></router-link>
        <router-link v-if = "isadmin"class="nav-link " to="/admindashboard"><img src="@/assets/quizicon.jpg" alt="Quiz Icon" width="40" height="40"  /></router-link>
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
                <a class="nav-link text-warn" href="#" @click="export_scv">Export CSV</a>
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

                const is_admin = JSON.parse(atob(token.split(".")[1])).sub.is_admin;
                
                this.isadmin = is_admin;
                this.isuser = !is_admin;
                // const response = await fetch("/api/login", {
                //     method: "GET",
                //     headers: { Authorization: `Bearer ${token}` },
                // });

                // const data = await response.json();
                // console.log("User data:", data);
                // this.isadmin = data.isadmin;
                // this.isuser = !data.isadmin;
            } catch (error) {
                console.error("Error fetching user role:", error);
                this.isadmin = false;
                this.isuser = false;
            }
        },
        toggleMenu() {
            this.menuVisible = !this.menuVisible;
        },
        export_scv() {
            console.log("Exporting CSV...");
            const token = localStorage.getItem("usertoken");

            fetch('/api/export', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.id) {
                        console.log("Waiting for 3 seconds before downloading...");
                        setTimeout(() => {
                            window.location.href = `/api/csv_result/${data.id}`;
                        }, 3000);
                    } else {
                        alert("Error: " + data.message);
                    }
                })
                .catch(error => {
                    console.error("Error downloading CSV:", error);
                    alert("An error occurred while downloading the CSV file.");
                });
        },
        logout() {
            console.log("Logging out...");
            localStorage.removeItem("admintoken");
            localStorage.removeItem("usertoken");

            this.role = null;
            this.isadmin = false;
            this.isuser = false;
            this.menuVisible = false; 

            this.$router.push("/"); 
        },
    },
};
</script>

<style scoped>
/* Align items properly */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Add styles for menu alignment */
.navbar-nav {
    display: flex;
    flex-direction: column;
    /* Makes menu vertical */
    position: absolute;
    top: 50px;
    /* Adjust based on navbar height */
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
