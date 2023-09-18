from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

class MediapipeDetector:

    def __init__(self):
        '''
        初始化 MP_Detector 類別。

        初始化模型參數並創建臉部和姿勢偵測器。

        參數:
        無

        返回:
        無
        '''
        # 初始化函式，設置模型參數
        self.input_image_width, self.input_image_height = 1, 1
        self.input_image = None
        # 建立臉部偵測器
        base_options_face = python.BaseOptions(model_asset_path='task/face_landmarker.task')
        options_face = vision.FaceLandmarkerOptions(base_options=base_options_face,
                                                    output_face_blendshapes=True,
                                                    output_facial_transformation_matrixes=True,
                                                    num_faces=1)
        self.detector_face = vision.FaceLandmarker.create_from_options(options_face)

        # 建立姿勢偵測器
        base_options_pose = python.BaseOptions(model_asset_path='task/pose_landmarker_heavy.task')
        options_pose = vision.PoseLandmarkerOptions(
            base_options=base_options_pose,
            output_segmentation_masks=True)
        self.detector_pose = vision.PoseLandmarker.create_from_options(options_pose)

    def draw_face_landmarks_on_image(self, input_image, detection_result: str):
        '''
        在圖像上繪製臉部標誌點。

        在輸入圖像上繪製臉部標誌點。

        參數:
        input_image (numpy.ndarray): 要繪製標誌點的輸入圖像。
        detection_result (str): 包含臉部標誌點的偵測結果。

        返回:
        numpy.ndarray: 帶有繪製臉部標誌點的圖像。
        '''
        # 繪製臉部關鍵點於圖像上
        face_landmarks_list = detection_result.face_landmarks

        for idx in range(len(face_landmarks_list)):
            face_landmarks = face_landmarks_list[idx]

            face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            face_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
            ])

            solutions.drawing_utils.draw_landmarks(
                image=input_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style())
            solutions.drawing_utils.draw_landmarks(
                image=input_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style())
            solutions.drawing_utils.draw_landmarks(
                image=input_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style())

        return input_image

    def draw_pose_landmarks_on_image(self, input_image, detection_result):
        '''
        在圖像上繪製姿態標誌點。

        在輸入圖像上繪製姿態標誌點。

        參數:
        input_image (numpy.ndarray): 要繪製標誌點的輸入圖像。
        detection_result (str): 包含姿態標誌點的偵測結果。

        返回:
        numpy.ndarray: 帶有繪製姿態標誌點的圖像。
        '''
        # 繪製姿勢關鍵點於圖像上
        pose_landmarks_list = detection_result.pose_landmarks

        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
                input_image,
                pose_landmarks_proto,
                solutions.pose.POSE_CONNECTIONS,
                solutions.drawing_styles.get_default_pose_landmarks_style())

        return input_image

    def run_all(self, input_image):
        '''
        在輸入圖像上運行臉部和姿態偵測。

        在提供的輸入圖像上運行臉部和姿態偵測。

        參數:
        input_image (numpy.ndarray): 進行偵測的輸入圖像。

        返回:
        tuple: 包含兩個元素的元組 - 臉部識別座標信息和姿態識別座標信息。
        '''
        # 執行所有偵測
        ImageFormat = mp.solutions.mediapipe.ImageFormat.SRGB
        image_file = mp.Image(image_format=ImageFormat.SRGB, data=input_image)
        detection_result_face = self.detector_face.detect(image_file)
        detection_result_pose = self.detector_pose.detect(image_file)
        self.input_image_width, self.input_image_height = input_image.shape[1], input_image.shape[0]
        self.input_image = input_image
        return detection_result_face, detection_result_pose

    def run_pose(self, input_image):
        '''
        在輸入圖像上運行姿態偵測。

        在提供的輸入圖像上運行姿態偵測。

        參數:
        input_image (numpy.ndarray): 進行偵測的輸入圖像。

        返回:
        str: 姿態識別座標信息。
        '''
        # 執行姿勢偵測
        ImageFormat = mp.solutions.mediapipe.ImageFormat.SRGB
        image_file = mp.Image(image_format=ImageFormat.SRGB, data=input_image)
        detection_result_pose = self.detector_pose.detect(input_image)
        self.input_image_width, self.input_image_height = input_image.shape[1], input_image.shape[0]
        self.input_image = input_image
        return detection_result_pose

    def run_face(self, input_image):
        '''
        在輸入圖像上運行臉部偵測。

        在提供的輸入圖像上運行臉部偵測。

        參數:
        input_image (numpy.ndarray): 進行偵測的輸入圖像。

        返回:
        str: 臉部識別座標信息。
        '''
        # 執行臉部偵測
        ImageFormat = mp.solutions.mediapipe.ImageFormat.SRGB
        image_file = mp.Image(image_format=ImageFormat.SRGB, data=input_image)
        detection_result_face = self.detector_face.detect(self.input_image)
        self.input_image_width, self.input_image_height = input_image.shape[1], input_image.shape[0]
        self.input_image = input_image
        return detection_result_face

    def draw_blank(self, face, pose):
        '''
        在空白圖像上繪製標誌點。

        在具有相同尺寸的空白圖像上繪製標誌點，尺寸與輸入圖像相同。

        參數:
        face (str): 臉部識別座標信息。
        pose (str): 姿態識別座標信息。

        返回:
        numpy.ndarray: 帶有繪製標誌點的空白圖像。
        '''
        # 繪製空白圖像並添加關鍵點
        input_image_width, input_image_height = self.input_image_width, self.input_image_height
        blank_image = np.zeros((input_image_height, input_image_width, 3), dtype=np.uint8)
        blank_image_with_landmarks = self.draw_pose_landmarks_on_image(blank_image, pose)
        blank_image_with_landmarks = self.draw_face_landmarks_on_image(blank_image_with_landmarks, face)
        return blank_image_with_landmarks

    def draw_overlay(self, face, pose):
        '''
        在原始圖像上疊加標誌點。

        在原始輸入圖像上疊加標誌點。

        參數:
        face (str): 臉部識別座標信息。
        pose (str): 姿態識別座標信息。

        返回:
        numpy.ndarray: 帶有疊加標誌點的原始圖像。
        '''
        # 將關鍵點添加到原始圖像上
        image_with_landmarks = self.draw_pose_landmarks_on_image(self.input_image, pose)
        image_with_landmarks = self.draw_face_landmarks_on_image(image_with_landmarks, face)
        return image_with_landmarks

    def draw_both(self, face, pose):
        '''
        在空白和原始圖像上繪製標誌點。

        在空白圖像和原始輸入圖像上繪製標誌點。

        參數:
        face (str): 臉部識別座標信息。
        pose (str): 姿態識別座標信息。

        返回:
        tuple: 包含兩個元素的元組 - 帶有繪製標誌點的空白圖像和帶有繪製標誌點的原始圖像。
        '''
        # 繪製空白圖像和原始圖像上的關鍵點
        input_image_width, input_image_height = self.input_image_width, self.input_image_height
        blank_image = np.zeros((input_image_height, input_image_width, 3), dtype=np.uint8)
        blank_image_with_landmarks = self.draw_pose_landmarks_on_image(blank_image, pose)
        blank_image_with_landmarks = self.draw_face_landmarks_on_image(blank_image_with_landmarks, face)
        image_with_landmarks = self.draw_pose_landmarks_on_image(self.input_image, pose)
        image_with_landmarks = self.draw_face_landmarks_on_image(image_with_landmarks, face)
        return blank_image_with_landmarks, image_with_landmarks
