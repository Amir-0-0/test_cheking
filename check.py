import cv2
import imutils


# Функция принимает название файла с фото теста, затем возращает словарь с результатами теста
def check(image_name: str) -> list:
    result = []
    photo_name = 'new_img.jpg'

    img = cv2.imread(image_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    edges = cv2.Canny(gray, 50, 150)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for cnt in cnts:
        p = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.01 * p, True)

        if len(approx) == 4 and 100 < p < 700:
            answer = img[approx[0, 0, 1]: approx[2, 0, 1], approx[1, 0, 0]: approx[3, 0, 0]]
            summa = answer.sum()
            count = 1
            for i in answer.shape:
                count *= i
            mid = summa / count
            if mid > 125:
                cv2.drawContours(img, [approx], -1, (255, 0, 255), 4)
                result.append(0)
            else:
                cv2.drawContours(img, [approx], -1, (255, 255, 0), 4)
                result.append(1)

    cv2.imwrite(photo_name, img)

    return [result[::-1], photo_name]
