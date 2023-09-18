$(document).ready(function () {
    const video1 = $('#video-stream');
    const video2 = $('#webcam-video-stream');

    if (video1.length > 0) {
        updateVideoStream1(video1);
    } else if (video2.length > 0) {
        updateVideoStream2(video2);
    }
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

    function updateVideoStream1() {
        const video = $('#video-stream');
        const loadingElement = $('.loading'); // 获取loading元素   
        video.attr('src', '/mp4/video_feed/'); // 替换为你的第一个视频URL
        video.on('error', function (e) {
            console.error('Error loading video:', e);
            loadingElement.css('display', 'block'); // 显示loading，在视频加载错误时
        });
    
        video.on('load', function () {
            loadingElement.css('display', 'none'); // 隐藏loading，当视频成功加载时
        });
    }
    
    function updateVideoStream2() {
        const video = $('#webcam-video-stream');
        const loadingElement = $('.loading'); // 获取loading元素
        video.attr('src', '/webcam/video/'); // 替换为你的第二个视频URL
        video.on('error', function (e) {
            console.error('Error loading video:', e);
            loadingElement.css('display', 'block'); // 显示loading，在视频加载错误时
        });
    
        video.on('load', function () {
            loadingElement.css('display', 'none'); // 隐藏loading，当视频成功加载时
        });
    }
});
