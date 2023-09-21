// sidebar.js

// JavaScript to control sidebar behavior
const sidebar = document.getElementById('sidebar');
//const content = document.getElementById('content');
let cornerWidth = 5; // Adjust as needed (corner width where sidebar appears)
const sidebarWidth = 50; // Adjust as needed (desired sidebar width)

// Function to show the sidebar
function showSidebar() {
    sidebar.style.width = `${sidebarWidth}px`;
    //content.style.marginLeft = `${sidebarWidth}px`;
}

// Function to hide the sidebar
function hideSidebar() {
    sidebar.style.width = '5px';
    //content.style.marginLeft = '0';
}

// Event listener for mouse movements
document.addEventListener('mousemove', (e) => {
    const mouseX = e.clientX;
    const mouseY = e.clientY;
    
    // Check if the mouse is in the top-left corner (adjust the cornerWidth)
    if (mouseX <= cornerWidth) {
        showSidebar();
        cornerWidth = sidebarWidth;
    } else {
        hideSidebar();
        cornerWidth = 5;
    }
});