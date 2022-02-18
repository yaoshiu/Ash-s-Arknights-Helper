import os
import random


__adb = os.path.abspath('platform-tools/adb.exe')
__arknights = 'com.hypergryph.arknights/com.u8.sdk.U8UnityContext'
__max0035, __max0036 = 0, 0


def devices() -> list[str]:
    """Returns a list of attached devices' serial numbers."""
    connected = os.popen(__adb + ' devices').read()
    return connected.splitlines()[1:-1]


def connect(method: str = '-e', serial_number: str = '') -> None:
    """Connect to a device.

    Args:
        * `method`: The method to connect.
            Avaliable method:
            * `-d`: Connect to the only device attached by USB.
            * `-e`: Connect to the only emulator.
            * `-s`: Connect to a specified device.
        * `serial_number`: The serial number of  device to be connected.
    """
    os.system(__adb + ' ' + method + ' ' + serial_number)


def wm_size() -> int and int:
    """Returns the size of the screen resolution of the connected device.

    Returns:
        * The horizontal resolution of the screen.
        * The vertical resolution of the screen.
    """
    content = os.popen(__adb + ' shell wm size').read()
    resolution = content.split()[2]
    return map(int, resolution.split('x'))


def wm_density() -> int:
    """Returns the screen density of the connected device"""
    return int(os.popen(__adb + ' shell wm density').read().split()[2])


def start_arknights() -> None:
    """Start Arknights on the connected device"""
    os.system(__adb + ' shell am start -n ' + __arknights)


def pull(device_path: str, computer_path: str) -> None:
    """Copy files from device to computer.

    Copy the file in the specified path on the device to the specified path on the computer.

    Args:
        `device_path`: The path of the file to be copied.
        `computer_path`: The path of to be copied to.
    """
    os.system(__adb + ' pull ' + device_path + ' ' + computer_path)


def push(computer_path: str, device_path: str) -> None:
    """Copy files from computer to device.

    Copy the file in the specified path on the computer to the specified path on the device.

    Args:
        `computer_path`: The path of the file to be copied.
        `device_path`: The path of the file to be copied to.
    """
    os.system(__adb + ' push ' + computer_path + ' ' + device_path)


def tap(x: int, y: int) -> None:
    """Tap the device with the specified coordinates.

    Args:
        `x`: The x coordinate of the tap point.
        `y`: The y coordinate of the tap point.
    """
    os.system(__adb + ' shell input tap ' + str(x) + ' ' + str(y))


def swipe(x1: int, y1: int, x2: int, y2: int) -> None:
    """Swipe the screen of the device connected with the specified coordinates.

    Args:
        `x1`: The start x coordinate of the swipe.
        `y1`: The start y coordinate of the swipe.
        `x2`: The end x coordinate of the swipe.
        `y2`: The end y coordinate of the swipe.
    """
    os.system(__adb + ' shell input swipe ' + str(x1) +
              ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2))


def home() -> None:
    """Push the home botton of the connected device."""
    os.system(__adb + ' shell input keyevent 3')


def __make_max() -> int and int:
    """Get the maximum size of the coordinates.

    Returns:
        The maximum size of the horizontal coordinate.
        The maximum size of the vertical coordinate.
    """
    global __max0035, __max0036
    contents = os.popen(__adb + ' shell getevent -p').read()
    abs0003 = contents.find('ABS')
    __max0035 = contents.find('0035', abs0003)
    __max0035 = contents.find('max', __max0035)
    end0035 = contents.find(',', __max0035)
    __max0036 = contents.find('0036', abs0003)
    __max0036 = contents.find('max', __max0036)
    end0036 = contents.find(',', __max0036)
    __max0035, __max0036 = int(
        contents[__max0035 + 4: end0035]), int(contents[__max0036 + 4: end0036])
    return __max0035, __max0036


def get_max_x() -> int:
    """Get the maximum size of the x coordinate.

    Returns:
        A int indicating the maximum size of the x coordinate.
    """
    if __max0035 == 0:
        __make_max()
    return __max0035


def get_max_y() -> int:
    """Get the maximum size of the y coordinate.

    Returns:
        A int indicating the maximum size of the y coordinate.
    """
    if __max0036 == 0:
        __make_max()
    return __max0036


def __main() -> int:
    for device in devices():
        print(device)
    # serial_number = input('请输入要连接的设备:')
    connect()
    horizontal, vertical = wm_size()
    print('该设备分辨率为:', horizontal, 'x', vertical)
    print('该设备ppi为为:', wm_density())
    print('0035max:', get_max_x())
    print('0036max:', get_max_y())
    tap(random.randint(1125, 1443) * __max0035 / 1920,
        random.randint(633, 779) * __max0036 / 1080)


if __name__ == '__main__':
    __main()
