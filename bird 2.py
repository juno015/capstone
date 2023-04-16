import numpy as np
import cv2

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
    #cv2.imshow("resulasdt1", img_result)
    #t = cv2.cvtColor(ii,cv2.COLOR_BGR2HSV) #변환 후 처리
    #cv2.imshow("result1", t)
    ii = cv2.cvtColor(ii, cv2.COLOR_BGR2GRAY)
    ii = cv2.blur(ii, (7,7))
    ii = cv2.Canny(ii, 50,cv2.THRESH_OTSU)
    lines = cv2.HoughLinesP(ii, 1, np.pi / 180, 30, maxLineGap=250)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img_result, (x1, y1), (x2, y2), (0, 255, 0), 3)
    k = "asd"
    if cv2.waitKey(10) == ord('l'):
        k = "asd123"
    cv2.putText(ii, "{}".format(k), (width//2-20, height), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) #이미지 넣기
    dst2 = cv2.warpPerspective(img_result, M2, (height, width)) #역변환
    #cv2.imshow('transform2', dst2)
    l = cv2.add(frame, dst2)
    cv2.imshow('transformasd2', l)
    cv2.imshow('ASD', ii)
    if cv2.waitKey(10) == 27:
        break

cap.release()  # 사용한 자원 해제
cv2.destroyAllWindows()
cv2.waitKey(0)
cv2.destroyAllWindows()