from utils import adb_utils
import os
import re

"""
获取芯片
"""
def get_device_chip_for_adb():
    adb_info = adb_utils.shell("getprop ro.build.skymid").stdout.read()
    chip = adb_info.decode().replace('\n', '').replace('\r', '').strip()
    #out, err = adb_info.communicate()
    #out_info = out.decode('unicode-escape')
    return chip

"""
获取机芯
"""
def get_device_type_for_adb():
    adb_info = adb_utils.shell("getprop ro.build.skytype").stdout.read()
    type = adb_info.decode().replace('\n', '').replace('\r', '').strip()
    #out, err = adb_info.communicate()
    #out_info = out.decode('unicode-escape')
    return type

"""
获取机型
"""
def get_device_model_for_adb():
    # utils.shell("getprop ro.product.model").stdout.read().decode()
    adb_info = adb_utils.shell("getprop ro.build.skymodel").stdout.read()
    model = adb_info.decode().replace('\n', '').replace('\r', '').strip()
    #out, err = adb_info.communicate()
    #out_info = out.decode('unicode-escape')
    return model

if __name__ == "__main__":
    """
    d = u2.connect()
    output, exit_code = d.shell("busybox top -n 1", timeout=60)
    print(f'uiautomator2 adb cmd: output={output}')
    """

