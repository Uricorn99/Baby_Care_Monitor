$(document).ready(function () {
    // const video1 = $('#video-stream');
    // const video2 = $('#webcam-video-stream');

    // if (video1.length > 0) {
    //     updateVideoStream1(video1);
    // } else if (video2.length > 0) {
    //     updateVideoStream2(video2);
    // }

    // 定义 sendParamBackEnd 函数
    function sendParamBackEnd() {
        // 获取参数的值
        let accValue = $('#acc').val();
        let dangertimeValue = $('#dangertime').val();
        let warningtimeValue = $('#warningtime').val();
        let toggleNotificationValue = $('#toggleNotification').is(':checked');
        

        // 发送到后端的逻辑
        let url = "http://127.0.0.1:8000/api/";

        axios.get(url, {
            params: {
                acc: accValue,
                dangertime: dangertimeValue,
                warningtime: warningtimeValue,
                toggle_notification: toggleNotificationValue,
                
            }
        }).then((response) => {
            console.log(response.data); // 成功处理后端响应
        }).catch((error) => {
            console.log(error); // 发送失败时处理错误
        });
    }

    // 绑定事件监听器以跟踪参数的更改
    $('#acc, #dangertime, #warningtime').on('input', function () {
        // 更新相应参数的值
        if (this.id === 'acc' || this.id === 'dangertime' || this.id === 'warningtime') {
            updateValue('value_' + this.id, $(this).val());
        }
    });

    // 绑定事件调用 sendParamBackEnd 函数
    $('#acc, #dangertime, #warningtime, #toggleNotification').on('change', function () {
     
        sendParamBackEnd();
    });

    
    // 函数来更新值
    function updateValue(elementId, value) {
        $("#" + elementId).text(value);
    }

    // 面板功能
    $("#panel").on("mouseenter", function () {
        $(this).css("left", "0");
    });

    $("#panel").on("mouseleave", function () {
        $(this).css("left", "-320px"); // 隐藏面板在左侧屏幕外
    });


    function loadStreams() {
        const originalStreamElement = $("#original-stream");
        const mediapipeStreamElement = $("#mediapipe-stream");
        const source = new EventSource("/mediapipe_feed/"); // 使用EventSource从服务器获取流

        source.onmessage = function(event) {
            const frames = event.data.split("||");
            if (frames.length === 2) {
                originalStreamElement.attr("src", "data:image/jpeg;base64," + frames[0]);
                mediapipeStreamElement.attr("src", "data:image/jpeg;base64," + frames[1]);
            }
        };
    }

    // 调用函数来加载两个流
    loadStreams();
});

