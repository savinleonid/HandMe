function openNav() {
    document.getElementById("mySidenav").style.width = "250px"; // Open the side navigation
    document.body.style.overflow = "hidden"; // Prevent background scroll
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0"; // Hide the side navigation
    document.body.style.overflow = ""; // Restore background scroll
}
