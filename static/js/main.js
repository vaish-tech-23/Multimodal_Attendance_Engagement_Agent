// Multimodal Attendance & Engagement Agent - Frontend Scripts

document.addEventListener("DOMContentLoaded", () => {
    // 1. Dynamic Camera HUD Clock
    const hudTimestamp = document.getElementById("hudTimestamp");
    if (hudTimestamp) {
        setInterval(() => {
            const now = new Date();
            const timeStr = now.toLocaleTimeString();
            hudTimestamp.textContent = `FPS: 30 • TIME: ${timeStr} • RESOLUTION: 1080P`;
        }, 1000);
    }

    // 2. Auto-fade flash alert banners after 4 seconds
    const alerts = document.querySelectorAll(".alert");
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.style.transition = "opacity 0.6s ease, transform 0.6s ease";
                alert.style.opacity = "0";
                alert.style.transform = "translateY(-10px)";
                setTimeout(() => alert.remove(), 600);
            });
        }, 4000);
    }
});
