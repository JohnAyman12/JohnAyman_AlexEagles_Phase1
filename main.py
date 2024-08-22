import cv2
import cv2 as cv

ideal = cv.imread('img/ideal.jpg')
# cv.imshow('ideal', ideal)

sample = cv.imread('img/sample6.jpg')
cv.imshow('sample', sample)

diffr2 = cv.bitwise_xor(ideal, sample)
# cv.imshow('differences', diffr2)

diffr2_gray = cv.cvtColor(diffr2, cv.COLOR_BGR2GRAY)
# cv.imshow("differences in gray", diffr2_gray)

_, diffr2_bin = cv.threshold(diffr2_gray, 155, 255, cv.THRESH_BINARY)
# cv.imshow("differences in binary", diffr2_bin)

contours, hierarchy = cv2.findContours(diffr2_bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

i = 0
radius_change = False
worn = 0
broken = 0
for contour in contours:
    if i == 0:
        i = 1
        continue
    epsilon = 0.01*cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)

    area = cv.contourArea(contour)
    if area > 600:
        radius_change = True
        cv.drawContours(sample, [contour], 0, (255, 0, 0), 3)
    elif area > 400:
        broken = broken + 1
        cv.drawContours(sample, [contour], 0, (0, 255, 0), 3)
    elif area > 100:
        worn = worn + 1
        cv.drawContours(sample, [contour], 0, (0, 0, 255), 3)

cv.imshow("final", sample)

print("change in diameter: " + str(radius_change))
print("worn: " + str(worn))
print("broken: " + str(broken))

cv.waitKey(0)
