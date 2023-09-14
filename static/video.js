// Function to update the video stream
$(document).ready(function() {
    function updateVideoStream() {
        const video = $('#video-stream');
        video.attr('src', '/mp4/video_feed/'); // Replace with the correct URL for your video feed view
        video.on('error', function(e) {
        console.error('Error loading video:', e);
        });

        // Hide the loading elements
        const loadingElements = $('.loading');
        loadingElements.css('display', 'none');
    }

    // Call the updateVideoStream function when the page loads
    $(window).on('load', function() {
        updateVideoStream();
    });
});


// Function to update the video stream
$(document).ready(function() {
    function updateVideoStream() {
        const video = $('#webcam-video-stream');
        video.attr('src', '/webcam/video/'); // Replace with the correct URL for your video feed view
        video.on('error', function(e) {
        console.error('Error loading video:', e);
        });

        // Hide the loading elements
        const loadingElements = $('.loading');
        loadingElements.css('display', 'none');
    }

    // Call the updateVideoStream function when the page loads
    $(window).on('load', function() {
        updateVideoStream();
    });
});



$(document).ready(function() {
    var panel = $("#panel");
    var paramA = $("#paramA");
    var paramB = $("#paramB");
    var paramC = $("#paramC");
    var toggleNotification = $("#toggleNotification");
    var toggleImage = $("#toggleImage"); 
  });
  

$(document).ready(function () {
    // Event listeners for paramA, paramB, and paramC
    $("#paramA").on("click", function () {
        updateValue("valueA", $(this).val());
    });

    $("#paramB").on("click", function () {
        updateValue("valueB", $(this).val());
    });

    $("#paramC").on("click", function () {
        updateValue("valueC", $(this).val());
    });

    // Event listener for toggleNotification
    $("#toggleNotification").on("change", function () {
        if ($(this).is(":checked")) {
            alert("通知已啟用"); // You can replace this with your notification logic
        } else {
            // Toggle button is unchecked
        }
    });

    // Event listener for toggleImage
    $("#toggleImage").on("change", function () {
        if ($(this).is(":checked")) {
            alert("影像已啟用"); // You can replace this with your image-related logic
        } else {
            // Toggle button is unchecked
        }
    });

    // Event listener for panel mouseenter
    $("#panel").on("mouseenter", function () {
        $(this).css("left", "0");
    });

    // Event listener for panel mouseleave
    $("#panel").on("mouseleave", function () {
        $(this).css("left", "-320px"); // 隐藏面板在左侧屏幕外
    });

    // Function to update value
    function updateValue(elementId, value) {
        $("#" + elementId).text(value);

    // Event listeners for paramA, paramB, and paramC
    $('#paramA, #paramB, #paramC').on('click', sendParamBackEnd);

    // Event listeners for toggleNotification and toggleImage
    $('#toggleNotification, #toggleImage').on('change', sendParamBackEnd);
    

    }
});


function sendParamBackEnd() {
    let paramAValue = $('#paramA').val();
    let paramBValue = $('#paramB').val();
    let paramCValue = $('#paramC').val();
    let toggleNotificationValue = $('#toggleNotification').is(':checked');
    let toggleImageValue = $('#toggleImage').is(':checked');

    let url = "http://127.0.0.1:8000/api/";

    axios.get(url, {
        params: {
            param_a: paramAValue,
            param_b: paramBValue,
            param_c: paramCValue,
            toggle_notification: toggleNotificationValue,
            toggle_image: toggleImageValue
        }
    }).then((response) => {
        console.log(response.data); // 成功处理后端响应
    }).catch((error) => {
        console.log(error); // 发送失败时处理错误
    });
}
