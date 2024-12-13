from machine import Pin
import Waveshare_driver
import time

Vbat_Pin = 29


# Draw line and show
def Touch_HandWriting():
    x = y = data = 0
    color = 0
    Touch.Flgh = 0
    Touch.Flag = 0
    Touch.Mode = 1
    Touch.Set_Mode(Touch.Mode)

    LCD.fill(LCD.white)
    LCD.rect(0, 0, 35, 208, LCD.red, True)
    LCD.rect(0, 0, 208, 35, LCD.green, True)
    LCD.rect(205, 0, 240, 240, LCD.blue, True)
    LCD.rect(0, 205, 240, 240, LCD.brown, True)
    LCD.show()

    Touch.tim.init(period=1, callback=Touch.Timer_callback)
    try:
        while True:
            if Touch.Flgh == 0 and Touch.X_point != 0:
                Touch.Flgh = 1
                x = Touch.X_point
                y = Touch.Y_point

            if Touch.Flag == 1:
                if (Touch.X_point > 34 and Touch.X_point < 205) and (
                    Touch.Y_point > 34 and Touch.Y_point < 205
                ):
                    Touch.Flgh = 3
                else:
                    if (Touch.X_point > 0 and Touch.X_point < 33) and (
                        Touch.Y_point > 0 and Touch.Y_point < 208
                    ):
                        color = LCD.red

                    if (Touch.X_point > 0 and Touch.X_point < 208) and (
                        Touch.Y_point > 0 and Touch.Y_point < 33
                    ):
                        color = LCD.green

                    if (Touch.X_point > 208 and Touch.X_point < 240) and (
                        Touch.Y_point > 0 and Touch.Y_point < 240
                    ):
                        color = LCD.blue

                    if (Touch.X_point > 0 and Touch.X_point < 240) and (
                        Touch.Y_point > 208 and Touch.Y_point < 240
                    ):
                        LCD.fill(LCD.white)
                        LCD.rect(0, 0, 35, 208, LCD.red, True)
                        LCD.rect(0, 0, 208, 35, LCD.green, True)
                        LCD.rect(205, 0, 240, 240, LCD.blue, True)
                        LCD.rect(0, 205, 240, 240, LCD.brown, True)
                        LCD.show()
                    Touch.Flgh = 4

                if Touch.Flgh == 3:
                    time.sleep(0.001)  # Prevent disconnection
                    if Touch.l < 25:
                        Touch.Flag = 0
                        LCD.line(x, y, Touch.X_point, Touch.Y_point, color)
                        LCD.Windows_show(x, y, Touch.X_point, Touch.Y_point)
                        Touch.l = 0
                    else:
                        Touch.Flag = 0
                        LCD.pixel(Touch.X_point, Touch.Y_point, color)
                        LCD.Windows_show(x, y, Touch.X_point, Touch.Y_point)
                        Touch.l = 0

                    x = Touch.X_point
                    y = Touch.Y_point
    except KeyboardInterrupt:
        pass


# Gesture
def Touch_Gesture():
    Touch.Mode = 0
    Touch.Set_Mode(Touch.Mode)
    LCD.fill(LCD.white)
    #     LCD.show()
    LCD.write_text("Gesture test", 70, 90, 1, LCD.black)
    LCD.write_text("Complete as prompted", 35, 120, 1, LCD.black)
    LCD.show()
    time.sleep(1)
    LCD.fill(LCD.white)
    while Touch.Gestures != 0x01:
        LCD.fill(LCD.white)
        LCD.write_text("UP", 100, 110, 3, LCD.black)
        LCD.show()
        time.sleep(0.1)

    while Touch.Gestures != 0x02:
        LCD.fill(LCD.white)
        LCD.write_text("DOWN", 70, 110, 3, LCD.black)
        LCD.show()
        time.sleep(0.1)

    while Touch.Gestures != 0x03:
        LCD.fill(LCD.white)
        LCD.write_text("LEFT", 70, 110, 3, LCD.black)
        LCD.show()
        time.sleep(0.1)

    while Touch.Gestures != 0x04:
        LCD.fill(LCD.white)
        LCD.write_text("RIGHT", 60, 110, 3, LCD.black)
        LCD.show()
        time.sleep(0.1)

    while Touch.Gestures != 0x0C:
        LCD.fill(LCD.white)
        LCD.write_text("Long Press", 40, 110, 2, LCD.black)
        LCD.show()
        time.sleep(0.1)

    while Touch.Gestures != 0x0B:
        LCD.fill(LCD.white)
        LCD.write_text("Double Click", 25, 110, 2, LCD.black)
        LCD.show()
        time.sleep(0.1)


def DOF_READ():
    qmi8658 = Waveshare_driver.QMI8658()
    Vbat = Waveshare_driver.ADC(Pin(Vbat_Pin))
    Touch.Mode = 0
    Touch.Set_Mode(Touch.Mode)

    while True:
        # read QMI8658
        xyz = qmi8658.Read_XYZ()

        LCD.fill(LCD.white)

        LCD.fill_rect(0, 0, 240, 40, LCD.red)
        LCD.text("Waveshare", 80, 25, LCD.white)

        LCD.fill_rect(0, 40, 240, 40, LCD.blue)
        # LCD.text("Long Press to Quit",20,57,LCD.white)
        LCD.write_text("Long Press to Quit", 50, 57, 1, LCD.white)

        LCD.fill_rect(0, 80, 120, 120, 0x1805)
        LCD.text("ACC_X={:+.2f}".format(xyz[0]), 20, 100 - 3, LCD.white)
        LCD.text("ACC_Y={:+.2f}".format(xyz[1]), 20, 140 - 3, LCD.white)
        LCD.text("ACC_Z={:+.2f}".format(xyz[2]), 20, 180 - 3, LCD.white)

        LCD.fill_rect(120, 80, 120, 120, 0xF073)
        LCD.text("GYR_X={:+3.2f}".format(xyz[3]), 125, 100 - 3, LCD.white)
        LCD.text("GYR_Y={:+3.2f}".format(xyz[4]), 125, 140 - 3, LCD.white)
        LCD.text("GYR_Z={:+3.2f}".format(xyz[5]), 125, 180 - 3, LCD.white)

        LCD.fill_rect(0, 200, 240, 40, 0x180F)
        reading = Vbat.read_u16() * 3.3 / 65535 * 3
        LCD.text("Vbat={:.2f}".format(reading), 80, 215, LCD.white)

        LCD.show()
        if Touch.Gestures == 0x0C:
            break


if __name__ == "__main__":

    LCD = Waveshare_driver.LCD_1inch28()
    LCD.set_bl_pwm(65535)

    Touch = Waveshare_driver.Touch_CST816T(mode=1, LCD=LCD)

    DOF_READ()

    Touch_Gesture()

    Touch_HandWriting()
