<template>
    <Navbar />
    <div id="app" class="app-background">
        <router-view></router-view>
    </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";

export default {
    name: "App",
    components: {
        Navbar
    }
};
</script>

<style>
.app-background {
    background: radial-gradient(circle, #010125, #000000);
    color: white;
    min-height: 100vh;
    /* Use min-height instead of height */
    display: flex;
    align-items: center;
    justify-content: center;
}

body,
html {
    margin: 0;
    padding: 0;
}
</style>
