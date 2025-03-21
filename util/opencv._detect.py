import cv2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gradio_ui.tools.screen_capture import get_screenshot

def detect_and_draw_edges():
    # Read the image
    screenshot, path = get_screenshot(is_cursor=False)
    img = cv2.imread(path)
    if img is None:
        print("Error: Could not read the image.")
        return
    
    # Create a copy for drawing contours later
    original = img.copy()
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detect edges using Canny algorithm
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours from the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw all detected contours
    cv2.drawContours(original, contours, -1, (0, 255, 0), 2)
    
    print(f"Found {len(contours)} contours in the image")
    
    # Display results
    # cv2.imshow("Original Image", img)
    cv2.imshow("Edges", edges)
    # cv2.imshow("Contours", original)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return original, contours

# Example usage
if __name__ == "__main__":
    result_image, detected_contours = detect_and_draw_edges()
