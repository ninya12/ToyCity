# -*- coding: utf-8 -*- # 한글 주석쓰려면 이거 해야함
import cv2  # opencv 사용
import numpy as np


def grayscale(img):  # 흑백이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def canny(img, low_threshold, high_threshold):  # Canny 알고리즘
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):  # 가우시안 필터
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  # ROI 셋팅

    mask = np.zeros_like(img)  # mask = img와 같은 크기의 빈 이미지

    if len(img.shape) > 2:  # Color 이미지(3채널)라면 :
        color = color3
    else:  # 흑백 이미지(1채널)라면 :
        color = color1

    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움
    cv2.fillPoly(mask, vertices, color)

    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):  # 선 그리기
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def draw_fit_line(img, lines, color=[0, 0, 255], thickness=10):  # 대표선 그리기
    cv2.line(img, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):  # 허프 변환
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    #  line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    #  draw_lines(line_img, lines)

    return lines


def weighted_img(img, initial_img, α=1, β=1., λ=0.):  # 두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, α, img, β, λ)


def get_fitline(img, f_lines):  # 대표선 구하기
    lines = np.squeeze(f_lines)
    if len(lines.shape) > 1:
        lines = lines.reshape(lines.shape[0]*2, 2)
        rows, cols = img.shape[:2]
        output = cv2.fitLine(lines, cv2.DIST_L2, 0, 0.01, 0.01)
        vx, vy, x, y = output[0], output[1], output[2], output[3]
        if not np.isnan(vx):
            x1, y1 = int(((img.shape[0]-1)-y)/vy*vx + x), img.shape[0]-1
            x2, y2 = int(((img.shape[0]/2+50)-y)/vy*vx + x), int(img.shape[0]/2+50)
            result = [x1, y1, x2, y2]
            print(x1, y1, x2, y2)
            return result


def getIntersection(x1, x2, x3, x4):
    # 두 점을 지나는 직선 끼리의 교점을 찾는 함수.
    # 평행 여부 확인
    parallel1 = (x1.x == x2.x)
    parallel2 = (x3.x == x4.x)
    # result init
    result = cv2.Point()

    # 직선 1이 y축에 평행한 경우
    if(parallel1):
        sameValue1 = x1.x
    else:
        increase1 = (x2.y - x1.y)/(x2.x - x1.x)  # 직선 1의 기울기
        constant1 = x1.y - increase1 * x1.x  # 직선 1의 y절편

    # 직선 2가 y축에 평행한 경우
    if(parallel2):
        sameValue2 = x3.x
    else:
        increase2 = (x4.y - x3.y)/(x4.x - x3.x)  # 직선 2의 기울기
        constant2 = x3.y - increase2 * x3.x  # 직선 2의 y절편

    # 두 직선이 평행한 경우 교점 없음. return None
    if(parallel1 and parallel2):
        return None

    # 직선 1이 y축에 평행한 경우 직선 1의 직선 위에 교점의 x값이 존재.
    # 직선 2의 y = ax + b 함수에 x값을 넣어 y값을 구함.
    if(parallel1):
        result = cv2.Point(sameValue1, increase2 * sameValue1 + constant2)
    # 직선 2가 y축에 평행한 경우 직선 2의 직선 위에 교점의 x값이 존재.
    # 직선 1의 y = ax + b 함수에 x값을 넣어 y값을 구함.
    elif(parallel2):
        result = cv2.Point(sameValue2, increase1 * sameValue2 + constant1)
    # y축에 평행한 직선이 없는 경우
    # x = -(b1 - b2)/(a1 - a2) 를 이용하여 x를 구하고 직선 1에 x값을 대입하여 y를 구함.
    else:
        result.x = -(constant1 - constant2)/(increase1 - increase2)
        result.y = increase1 * result.x + constant1
    return result


# image = cv2.imread('slope_test.jpg')  # 이미지 읽기
cap = cv2.VideoCapture(-1)
cap.set(3, 320)
cap.set(4, 240)
while(cap.isOpened()):
    image = cap.read()[1]

    height, width = image.shape[:2]  # 이미지 높이, 너비
    # print(height, width)

    gray_img = grayscale(image)  # 흑백이미지로 변환

    blur_img = gaussian_blur(gray_img, 3)  # Blur 효과

    canny_img = canny(blur_img, 70, 210)  # Canny edge 알고리즘

    vertices = np.array([[(0, height), (width/2-100, height/2), (width/2+100, height/2), (width, height)]], dtype=np.int32)
    ROI_img = region_of_interest(canny_img, vertices)  # ROI 설정
    # print(ROI_img)

    line_arr = hough_lines(ROI_img, 1, 1 * np.pi/180, 30, 10, 20)  # 허프 변환
    temp = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    if line_arr is not None:
        line_arrsq = np.squeeze(line_arr)  # 기울기 구하기
        if len(line_arrsq.shape) > 1:
            try:
                slope_degree = (np.arctan2(line_arrsq[:, 1] - line_arrsq[:, 3], line_arrsq[:, 0] - line_arrsq[:, 2]) * 180) / np.pi
                # 수평 기울기 제한
                line_arrsq = line_arrsq[np.abs(slope_degree) < 160]
                slope_degree = slope_degree[np.abs(slope_degree) < 160]
                # 수직 기울기 제한
                line_arrsq = line_arrsq[np.abs(slope_degree) > 95]
                slope_degree = slope_degree[np.abs(slope_degree) > 95]
                # 필터링된 직선 버리기
                L_lines, R_lines = line_arrsq[(slope_degree > 0), :], line_arrsq[(slope_degree < 0), :]
                L_lines, R_lines = L_lines[:, None], R_lines[:, None]
                # 왼쪽, 오른쪽 각각 대표선 구하기
                left_fit_line = get_fitline(image, L_lines)
                right_fit_line = get_fitline(image, R_lines)
                # 대표선 그리기
                if(left_fit_line is not None):
                    draw_fit_line(temp, left_fit_line)
                if(right_fit_line is not None):
                    draw_fit_line(temp, right_fit_line)
                point1 = cv2.Point(left_fit_line[0], left_fit_line[1])
                point2 = cv2.Point(left_fit_line[2], left_fit_line[3])
                point3 = cv2.Point(right_fit_line[0], right_fit_line[1])
                point4 = cv2.Point(right_fit_line[2], right_fit_line[3])
                interPoint = getIntersection(point1, point2, point3, point4)
            except Exception as e:
                print(e)

    result = weighted_img(temp, image)  # 원본 이미지에 검출된 선 overlap
    cv2.imshow('result', result)  # 결과 이미지 출력
    if(cv2.waitKey(30) & 0xFF == 27):
        break

cap.release()
cv2.destroyAllWindows()
