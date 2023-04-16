import numpy as np
import cv2
import matplotlib.pyplot as plt
# 원본 이미지
cap = cv2.VideoCapture("test1.mp4")


while 1:
    _, frame = cap.read()
    cv2.resize(frame,(600,400))
    width, height = frame.shape[:2]
    p1 =  [(width//2+250, 121*4+10)]
    p2 =  [(195*4+100, 121*4+10)]
    p3 =  [(64*4, 176*4)]
    p4 = [(275*4+100, 174*4)]
    # 좌표 순서 - 상단왼쪽 끝, 상단오른쪽 끝, 하단왼쪽 끝, 하단오른쪽 끝
    pts1 = np.float32([p1,p2,p3,p4]) #위치 설정
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    M = cv2.getPerspectiveTransform(pts1,pts2) #변환을 위함
    M2 = cv2.getPerspectiveTransform(pts2, pts1) #역변환을 위함
    img_result = cv2.warpPerspective(frame, M, (width,height)) #변환
    ii = img_result.copy() #변환된 결과


    HlS = cv2.cvtColor(ii, cv2.COLOR_BGR2HLS)
    yello = cv2.inRange(HlS, (70, 150, 20), (255,255,255)) #(HlS, (190, 200, 20), (195,255,255))
    white = cv2.inRange(HlS, (0, 85, 81), (190, 255, 255))
    mask = cv2.bitwise_or(yello, white) #특정 영역 추출 (색 선택)
    cv2.imshow("result1", mask)
    cv2.imshow("asd",HlS)


    histogram = np.sum(mask[mask.shape[0]//2:,:], axis=0)
    mid = int(histogram.shape[0]//2)
    left = np.argmax(histogram[:mid])
    right = np.argmax(histogram[mid:]) +mid #히스토그램, 오른쪽 왼쪽 판별

    k = "mid"
    if right >= 700 or right <= 360 or left >= 120 :
        k = "right"
    if left <= 40 or left >= 200:
      k = "left"
        
    cv2.putText(img_result, "{}".format(k), (width//2-20, height), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) #이미지 넣기
    dst2 = cv2.warpPerspective(img_result, M2, (height, width)) #역변환
    #cv2.imshow('transform2', dst2)
    l = cv2.add(frame, dst2)
    cv2.imshow("asdasd",l)
    if cv2.waitKey(10) == 27:
        break

cap.release()  # 사용한 자원 해제
cv2.destroyAllWindows()
cv2.waitKey(0)
cv2.destroyAllWindows()