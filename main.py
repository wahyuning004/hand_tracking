import cv2
import numpy as np
import time
import math

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

# ==========================================================
# TREND JARI CAMERA - EKA WAHYUNING TIYASA
# ==========================================================
# Aturan Ketat:
# 1. Kotak HANYA MUNCUL jika Telunjuk & Jempol KEDUA TANGAN TERBUKA.
# 2. Jika jari diarahkan ke bawah -> JANGAN ADA KOTAK, HANYA PETIR!
# 3. Sentuh Jempol & Kelingking -> Ganti Filter.
# ==========================================================

class EkaCameraStrictBoxApp:
    def __init__(self):
        if MEDIAPIPE_AVAILABLE:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                model_complexity=0,
                min_detection_confidence=0.55,
                min_tracking_confidence=0.55
            )
        else:
            self.mp_hands = None
            self.hands = None

        self.FILTER_MODES = ["THERMAL", "INFERNO", "GLITCH", "NEON_MATRIX"]
        self.current_filter_idx = 0
        self.last_switch_time = 0

    def dist(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def is_thumb_index_open(self, pts):
        wrist = pts[0]
        hand_size = self.dist(pts[0], pts[9])
        i_open = self.dist(pts[8], wrist) > self.dist(pts[6], wrist) * 1.15
        t_open = self.dist(pts[4], pts[2]) > hand_size * 0.35
        return i_open and t_open

    def is_five_fingers_down(self, pts):
        wrist_y = pts[0][1]
        tips_y = [pts[4][1], pts[8][1], pts[12][1], pts[16][1], pts[20][1]]
        mcps_y = [pts[2][1], pts[5][1], pts[9][1], pts[13][1], pts[17][1]]
        down_count = sum(1 for i in range(5) if tips_y[i] > mcps_y[i] and tips_y[i] > wrist_y * 0.95)
        return down_count >= 4

    def draw_downward_lightning(self, frame, tips, time_val):
        h, w, _ = frame.shape
        colors = [(230, 255, 0), (119, 0, 255), (136, 255, 0), (0, 255, 255), (255, 0, 112)]
        for idx, tip in enumerate(tips):
            sx, sy = tip
            color = colors[idx % len(colors)]
            cur_x, cur_y = sx, sy
            segments = 8
            step_y = (h - sy) / segments
            pts = [(cur_x, cur_y)]
            for s in range(1, segments + 1):
                cur_y += int(step_y)
                cur_x += int((math.sin(time_val * 10 + s + idx) * 12) + np.random.uniform(-14, 14))
                pts.append((cur_x, min(h - 1, cur_y)))

            for i in range(len(pts) - 1):
                cv2.line(frame, pts[i], pts[i + 1], color, 2, cv2.LINE_AA)
            cv2.circle(frame, (sx, sy), 6, (255, 255, 255), -1, cv2.LINE_AA)

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            return

        cv2.namedWindow("Eka Wahyuning Tiyasa - Camera", cv2.WINDOW_AUTOSIZE)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (720, 540))
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            now = time.time()

            portal_polygon = None

            if MEDIAPIPE_AVAILABLE and self.hands:
                results = self.hands.process(rgb_frame)
                if results.multi_hand_landmarks:
                    num_hands = len(results.multi_hand_landmarks)
                    all_hands = [[(int(p.x * w), int(p.y * h)) for p in hlms.landmark] 
                                 for hlms in results.multi_hand_landmarks]

                    any_hand_down = False
                    for pts in all_hands:
                        # Ganti filter: jempol & kelingking
                        hand_size = self.dist(pts[0], pts[9])
                        touch_ratio = self.dist(pts[4], pts[20]) / max(30.0, hand_size)
                        if touch_ratio < 0.45:
                            if now - self.last_switch_time > 0.7:
                                self.current_filter_idx = (self.current_filter_idx + 1) % len(self.FILTER_MODES)
                                self.last_switch_time = now

                        # Petir saat tangan ke bawah
                        if self.is_five_fingers_down(pts):
                            any_hand_down = True
                            tips = [pts[4], pts[8], pts[12], pts[16], pts[20]]
                            self.draw_downward_lightning(frame, tips, now)

                    # KOTAK HANYA MUNCUL JIKA KEDUA TANGAN MEMBUKA TELUNJUK & JEMPOL, DAN TIDAK SEDANG MENUNJUK KE BAWAH!
                    if num_hands >= 2 and not any_hand_down:
                        h1, h2 = all_hands[0], all_hands[1]
                        if self.is_thumb_index_open(h1) and self.is_thumb_index_open(h2):
                            portal_polygon = np.array([h1[8], h2[8], h2[4], h1[4]], dtype=np.int32)

            output = frame.copy()

            # Render Filter di Kotak 4 Jari
            if portal_polygon is not None:
                x_coords = [p[0] for p in portal_polygon]
                y_coords = [p[1] for p in portal_polygon]
                min_x, max_x = max(0, min(x_coords)), min(w, max(x_coords))
                min_y, max_y = max(0, min(y_coords)), min(h, max(y_coords))

                if max_x > min_x + 5 and max_y > min_y + 5:
                    crop = frame[min_y:max_y, min_x:max_x]
                    mode = self.FILTER_MODES[self.current_filter_idx]

                    if mode == "THERMAL":
                        gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                        filtered_crop = cv2.applyColorMap(gray_crop, cv2.COLORMAP_JET)
                    elif mode == "INFERNO":
                        gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                        filtered_crop = cv2.applyColorMap(gray_crop, cv2.COLORMAP_INFERNO)
                    elif mode == "GLITCH":
                        b, g, r = cv2.split(crop)
                        shift = 12
                        b_s = np.zeros_like(b)
                        b_s[:, :-shift] = b[:, shift:]
                        filtered_crop = cv2.merge([b_s, g, r])
                    else:
                        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
                        hsv[:, :, 0] = (hsv[:, :, 0] + 60) % 180
                        filtered_crop = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

                    mask_crop = np.zeros((max_y - min_y, max_x - min_x), dtype=np.uint8)
                    poly_offset = portal_polygon - [min_x, min_y]
                    cv2.fillPoly(mask_crop, [poly_offset], 255)

                    blended_crop = np.where(mask_crop[:, :, None] == 255, filtered_crop, crop)
                    output[min_y:max_y, min_x:max_x] = blended_crop

                cv2.polylines(output, [portal_polygon], True, (0, 255, 230), 3, cv2.LINE_AA)
                for pt in portal_polygon:
                    cv2.circle(output, tuple(pt), 6, (255, 0, 119), -1, cv2.LINE_AA)

            # Bingkai Nama Eka Wahyuning Tiyasa
            cv2.rectangle(output, (0, 0), (w, 36), (15, 15, 25), -1)
            cv2.putText(output, "EKA WAHYUNING TIYASA - CAMERA", (20, 24),
                        cv2.FONT_HERSHEY_DUPLEX, 0.55, (0, 255, 230), 1, cv2.LINE_AA)

            cv2.imshow("Eka Wahyuning Tiyasa - Camera", output)
            if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = EkaCameraStrictBoxApp()
    app.run()
