var panel = document.getElementById("panel");
var paramA = document.getElementById("paramA");
var paramB = document.getElementById("paramB");
var paramC = document.getElementById("paramC");
var toggleNotification = document.getElementById("toggleNotification");
var toggleImage = document.getElementById("toggleImage"); // Add this line for the "影像" toggle button

paramA.addEventListener("input", function () {
    updateValue("valueA", paramA.value);
});

paramB.addEventListener("input", function () {
    updateValue("valueB", paramB.value);
});

paramC.addEventListener("input", function () {
    updateValue("valueC", paramC.value);
});

toggleNotification.addEventListener("change", function () {
    if (toggleNotification.checked) {
        // Toggle button is checked, handle the notification logic here
        alert("通知已啟用"); // You can replace this with your notification logic
    } else {
        // Toggle button is unchecked
    }
});

toggleImage.addEventListener("change", function () {
    if (toggleImage.checked) {
        // Toggle button is checked, handle the image logic here
        alert("影像已啟用"); // You can replace this with your image-related logic
    } else {
        // Toggle button is unchecked
    }
});

function updateValue(elementId, value) {
    document.getElementById(elementId).textContent = value;
}

// 监听鼠标移入面板时，將面板展开
panel.addEventListener("mouseenter", function () {
    panel.style.left = "0";
});

// 监听鼠标离开面板时，将面板收回到左侧屏幕外
panel.addEventListener("mouseleave", function () {
    panel.style.left = "-320px"; // 隐藏面板在左侧屏幕外
});