from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import numpy as np

def parse_css_color_to_rgb(color_str):
    color_str = color_str.strip()
    color_str = color_str.replace("rgba", "").replace("rgb", "")
    color_str = color_str.strip("() ")
    parts = color_str.split(",")
    r = int(float(parts[0]))
    g = int(float(parts[1]))
    b = int(float(parts[2]))
    return (r, g, b)

def main():
    driver = webdriver.Chrome()
    driver.get("https://5jqdmjxdwavv.trickle.host")

    time.sleep(3)

    print("You can now start the game")
    input("When the game is ready, press ENTER to continue...")

    while True:
        squares = driver.find_elements(By.CSS_SELECTOR, "div.grid-cell")
        if not squares:
            print("No elements found with CSS selector 'div.grid-cell'. Exiting...")
            break

        colors = []
        for sq in squares:
            bg = sq.value_of_css_property("background-color")
            colors.append(bg)

        rgb_values = [parse_css_color_to_rgb(c) for c in colors]

        arr = np.array(rgb_values, dtype=np.float32)
        mean_color = np.mean(arr, axis=0)

        def color_distance(c1, c2):
            return np.linalg.norm(c1 - c2)

        max_dist = -1
        diff_idx = -1
        for i, rgb in enumerate(rgb_values):
            dist = color_distance(rgb, mean_color)
            if dist > max_dist:
                max_dist = dist
                diff_idx = i

        if diff_idx == -1:
            print("No different color found. Exiting...")
            break

        squares[diff_idx].click()
        print(f"Clic on square #{diff_idx} with color {colors[diff_idx]}")

        # Wait for next grid
        time.sleep(0.5)

    driver.quit()

if __name__ == "__main__":
    main()

# :D
