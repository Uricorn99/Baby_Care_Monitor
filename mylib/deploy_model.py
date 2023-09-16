import cv2
import os
from yolo import darknet


class OpenCV_DNN:
    def __init__(self, weights_path: str, cfg_path: str) -> None:
        """
        Using OpenCV DNN Deploy YOLOv4 Darknet Model

        Parameters:

        weightsPath: 權重檔案路徑/檔名.weights

        cfgPath: 模型參數檔案路徑/檔名.cfg
        """
        self.__weights_path = weights_path
        self.__cfg_path = cfg_path

    @property
    def WeighstPath(self) -> str:
        return self.__weights_path

    @WeighstPath.setter
    def WeighstPath(self, path: str):
        """
        權重檔案路徑
        """
        self.__weights_path = path

    @property
    def CfgPath(self) -> str:
        return self.__cfg_path

    @CfgPath.setter
    def CfgPath(self, path: str):
        """
        模型參數檔案路徑
        """
        self.__cfg_path = path

    def detection(self, img: cv2.Mat, confidence_threshold: float = 0.5) -> tuple:
        """
        物件偵測

        parameters:

        img_path: 圖像路徑/檔名

        return:

        (classes: 類別, scores: 信任分數, boxes: [圖像x, 圖像y, 圖像w, 圖像h])
        """
        NMS_THRESHOLD = 0.4
        # net = cv2.dnn.readNet(self.__weights_path, self.__cfg_path) # OpenCV 深度學習模組
        net = cv2.dnn.readNetFromDarknet(
            cfgFile=self.__cfg_path, darknetModel=self.__weights_path
        )
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)
        classes, scores, boxes = model.detect(img, confidence_threshold, NMS_THRESHOLD)
        return classes, scores, boxes


class Yolo:
    def __init__(self, config_file: str, data_file: str, weights: str) -> None:
        """
        YOLOv4 Darknet Object Detection

        Parameters:

        config_file:模型配置文件

        data_file:資料集文件

        weights:模型權重文件
        """
        if not os.path.exists(config_file):
            raise (".cfg檔案路徑錯誤")

        if not os.path.exists(data_file):
            raise (".data檔案路徑錯誤")

        if not os.path.exists(weights):
            raise (".weights檔案路徑錯誤")

        # Load Network
        self.__network, self.__class_names, self.__class_colors = darknet.load_network(
            config_file, data_file, weights, batch_size=1
        )

        # 取得神經網路的輸入維度(寬,高)
        self.__network_width = darknet.network_width(self.__network)
        self.__network_height = darknet.network_height(self.__network)

    @property
    def Network_Width(self):
        """
        取得神經網路的輸入(寬)
        """
        return self.__network_width

    @property
    def Network_Height(self):
        """
        取得神經網路的輸入(高)
        """
        return self.__network_height

    def Object_Detect(
        self, image_rgb: cv2.Mat, thresh: float = 0.5, show_coordinates: bool = True
    ):
        """
        物件偵測

        Parameter:

        image_rgb: 待偵測圖像(RGB)

        thresh: 準確度門檻值

        show_coordinates: 資訊顯示在終端機上

        Returns:

        物件偵測圖像(RGB), 偵測物件列表
        """
        # Resize to model dimensions
        image_resized = cv2.resize(
            image_rgb, (self.__network_width, self.__network_height)
        )

        # convert to darknet format, save to “ darknet_image “
        darknet_image = darknet.make_image(
            self.__network_width, self.__network_height, 3
        )
        darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())

        # inference
        detections = darknet.detect_image(
            self.__network, self.__class_names, darknet_image, thresh=thresh
        )
        darknet.print_detections(detections, show_coordinates)  # 將資訊顯示在終端機上
        darknet.free_image(darknet_image)  # 將圖片給清除

        # draw bounding box
        image_detections = darknet.draw_boxes(
            detections, image_resized, self.__class_colors
        )
        return cv2.cvtColor(image_detections, cv2.COLOR_BGR2RGB), detections
