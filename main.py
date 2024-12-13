from machine import Pin
import Waveshare_driver
import time
import math

Vbat_Pin = 29

small_blind = 50
big_blind = 100


def draw_ticker_lines(LCD):
    center_x = 120
    center_y = 120
    radius = 110
    for hour in range(12):
        angle = math.radians(hour * 30)
        start_x = int(center_x + radius * math.cos(angle))
        start_y = int(center_y - radius * math.sin(angle))
        end_x = int(center_x + (radius - 10) * math.cos(angle))
        end_y = int(center_y - (radius - 10) * math.sin(angle))
        LCD.line(start_x, start_y, end_x, end_y, LCD.black)


def draw_countdown_indicator(LCD, progress):
    center_x = 120
    center_y = 120
    radius = 100
    angle = math.radians(
        360 * progress - 90
    )  # Adjust angle to start at 12 o'clock
    end_x = int(center_x + radius * math.cos(angle))
    end_y = int(center_y + radius * math.sin(angle))
    for i in range(-1, 2):  # Draw three lines to make the indicator thicker
        LCD.line(center_x + i, center_y, end_x + i, end_y, LCD.blue)


def countdown_timer(LCD, target_secs):
    global small_blind, big_blind
    elapsed_secs = target_secs
    update_interval = 0.1  # Update every 100 milliseconds

    while True:  # Keep repeating countdown loops
        while elapsed_secs >= 0:  # One loop of the countdown
            minutes = math.ceil(elapsed_secs // 60)
            seconds = math.ceil(elapsed_secs % 60)
            time_str = "{:02}:{:02}".format(minutes, seconds)

            LCD.fill(LCD.white)
            draw_ticker_lines(LCD)
            progress = (target_secs - elapsed_secs) / target_secs
            draw_countdown_indicator(LCD, progress)
            text_width = (
                8 * 5 * 3
            )  # 5 characters, 8 pixels per character, size 3
            x = (240 - text_width) // 2
            LCD.write_text(time_str, x, 90, 3, LCD.black)

            LCD.write_text(f"Small: {small_blind}", 40, 150, 2, LCD.black)
            LCD.write_text(f"Big: {big_blind}", 50, 180, 2, LCD.black)
            LCD.show()

            time.sleep(update_interval)
            elapsed_secs -= update_interval

        # Double the blinds and reset the countdown
        small_blind *= 2
        big_blind *= 2
        elapsed_secs = target_secs


if __name__ == "__main__":
    LCD = Waveshare_driver.LCD_1inch28()
    LCD.set_bl_pwm(65535)

    Touch = Waveshare_driver.Touch_CST816T(mode=1, LCD=LCD)

    countdown_timer(LCD, 12)  # 12 seconds countdown
