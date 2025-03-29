<template>
    <div class="container-fluid d-flex align-items-center justify-content-center" style="height: 100vh;">
        <div class="row w-75">
            <!-- Image Section -->
            <div class="col-md-6 d-flex align-items-center justify-content-center">
                <img src="@/assets/quiz.jpg" alt="Quiz" class="img-fluid rounded-circle"
                    style="max-height: 300px; width: 300px; object-fit: cover;">
            </div>
            <!-- Text & Button Section -->
            <div class="col-md-6 d-flex align-items-center">
                <div class="card w-100">
                    <div class="card-header text-center">
                        <h1>Master any Subject with Quiz-Master</h1>
                    </div>
                    <div class="card-body text-center">
                        <router-link to="/login" class="btn btn-primary me-2">Already a User</router-link>
                        <router-link to="/signup" class="btn btn-success">Join Us</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'HomeView',
};
</script>
