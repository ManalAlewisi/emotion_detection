import cv2
from deepface import DeepFace
import os

def draw_emotion_bars(frame, emotions, x, y, w, h):
    bar_x = x + w + 10
    bar_y = y
    for i, (emotion, score) in enumerate(emotions.items()):
        bar_width = int(score * 1.5)
        color = (0, 255, 0) if score == max(emotions.values()) else (200, 200, 200)
        cv2.rectangle(frame, (bar_x, bar_y + i*25), 
                      (bar_x + bar_width, bar_y + i*25 + 18), color, -1)
        cv2.putText(frame, f"{emotion}: {score:.1f}%", 
                    (bar_x, bar_y + i*25 + 14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)

def analyze_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not load image.")
        return

    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
    emotion = result[0]['dominant_emotion']
    emotions = result[0]['emotion']
    region = result[0]['region']

    x, y, w, h = region['x'], region['y'], region['w'], region['h']

    # Draw face rectangle
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Draw dominant emotion label
    cv2.putText(img, f"Emotion: {emotion.upper()}", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Add sidebar with same background color
    sidebar_width = 220
    avg_color = img[0:10, 0:10].mean(axis=(0,1)).astype(int)
    sidebar = img[0:img.shape[0], 0:sidebar_width].copy()
    avg_color = tuple(int(c) for c in img.mean(axis=(0,1))[:3])
    sidebar = [[avg_color] * sidebar_width] * img.shape[0]
    sidebar = cv2.copyMakeBorder(img, 0, 0, 0, sidebar_width, 
                                  cv2.BORDER_CONSTANT, value=avg_color)

    # Draw emotion bars on sidebar
    bar_x = img.shape[1] + 10
    for i, (emo, score) in enumerate(emotions.items()):
        bar_width = int(score * 1.8)
        color = (0, 255, 0) if emo == emotion else (180, 180, 180)
        cv2.rectangle(sidebar, (bar_x, 20 + i*35),
                      (bar_x + bar_width, 20 + i*35 + 22), color, -1)
        cv2.putText(sidebar, f"{emo}: {score:.1f}%",
                    (bar_x, 20 + i*35 + 16),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    print(f"\nDominant Emotion: {emotion.upper()}")
    print("\nAll Emotions:")
    for e, score in emotions.items():
        bar = "█" * int(score / 5)
        print(f"  {e:10s}: {bar} {score:.2f}%")

    output_path = os.path.join(os.path.dirname(image_path), "result.jpg")
    cv2.imwrite(output_path, sidebar)
    print(f"\nResult saved to: {output_path}")

    cv2.imshow("Emotion Detection", sidebar)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def analyze_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Press 'q' to quit | Press 's' to save screenshot")
    screenshot_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(frame, actions=['emotion'],
                                      enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            emotions = result[0]['emotion']
            region = result[0]['region']
            x, y, w, h = region['x'], region['y'], region['w'], region['h']

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{emotion.upper()}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            draw_emotion_bars(frame, emotions, x, y, w, h)

        except:
            cv2.putText(frame, "No face detected", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Real-Time Emotion Detection", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('s'):
            screenshot_count += 1
            filename = f"screenshot_{screenshot_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Screenshot saved: {filename}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("=" * 40)
    print("   Emotion Detection System")
    print("=" * 40)
    print("1. Analyze an image")
    print("2. Real-time camera")
    choice = input("\nEnter choice (1 or 2): ")

    if choice == "1":
        while True:
            path = input("\nEnter image path (or 'q' to quit): ")
            if path.lower() == 'q':
                print("Goodbye!")
                break
            analyze_image(path)
    elif choice == "2":
        analyze_camera()
    else:
        print("Invalid choice.")