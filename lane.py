import cv2
import numpy as np

# ================= GLOBAL ================= #
prev_lines = None   # for smoothing

# ================= CANNY ================= #
def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Adaptive contrast (works in shadows/night)
    gray = cv2.equalizeHist(gray)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive Canny thresholds
    median = np.median(gray)
    lower = int(max(0, 0.66 * median))
    upper = int(min(255, 1.33 * median))

    return cv2.Canny(blur, lower, upper)

# ================= ROI ================= #
def roi(image):
    height, width = image.shape[:2]

    polygon = np.array([[
        (int(0.1 * width), height),
        (int(0.9 * width), height),
        (int(0.55 * width), int(0.6 * height)),
        (int(0.45 * width), int(0.6 * height))
    ]])

    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygon, 255)

    return cv2.bitwise_and(image, mask)

# ================= DISPLAY ================= #
def display_lines(image, lines):
    line_image = np.zeros_like(image)

    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 8)

    return line_image

# ================= COORDINATES ================= #
def make_coordinates(image, line_params):
    slope, intercept = line_params

    y1 = image.shape[0]
    y2 = int(y1 * 0.6)

    if slope == 0:
        slope = 0.1

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return [x1, y1, x2, y2]

# ================= AVERAGE ================= #
def average_slope_intercept(image, lines):
    global prev_lines

    left_fit = []
    right_fit = []

    if lines is None:
        return prev_lines

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)

        # Skip vertical lines
        if x1 == x2:
            continue

        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope, intercept = parameters

        # Remove noise
        if abs(slope) < 0.5:
            continue

        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    lines_output = []

    if len(left_fit) > 0:
        left_avg = np.average(left_fit, axis=0)
        lines_output.append(make_coordinates(image, left_avg))

    if len(right_fit) > 0:
        right_avg = np.average(right_fit, axis=0)
        lines_output.append(make_coordinates(image, right_avg))

    if len(lines_output) == 0:
        return prev_lines

    # Smoothing (VERY IMPORTANT)
    if prev_lines is not None:
        lines_output = np.array(lines_output)
        prev_lines = 0.8 * prev_lines + 0.2 * lines_output
    else:
        prev_lines = np.array(lines_output)

    return prev_lines.astype(int)

# ================= MAIN ================= #
cap = cv2.VideoCapture("nD_11.mp4")  # change video here

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Standardize size
    frame = cv2.resize(frame, (1280, 720))

    canny_image = canny(frame)
    cropped = roi(canny_image)

    lines = cv2.HoughLinesP(
        cropped,
        2,
        np.pi / 180,
        100,
        np.array([]),
        minLineLength=40,
        maxLineGap=50
    )

    averaged_lines = average_slope_intercept(frame, lines)

    line_image = display_lines(frame, averaged_lines)

    final = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    cv2.imshow("Lane Detection", final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()