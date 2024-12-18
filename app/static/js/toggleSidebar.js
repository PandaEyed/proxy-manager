document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleButton = document.getElementById("sidebarToggle");

    // Toggle sidebar on button click
    toggleButton.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");
    });

    // Expand sidebar on hover when collapsed
    sidebar.addEventListener("mouseenter", function () {
        if (sidebar.classList.contains("collapsed")) {
            sidebar.classList.remove("collapsed");
        }
    });

    // Collapse sidebar when mouse leaves
    sidebar.addEventListener("mouseleave", function () {
        if (!sidebar.classList.contains("expanded")) {
            sidebar.classList.add("collapsed");
        }
    });
});