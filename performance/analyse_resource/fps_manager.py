from analyse_resource.bean.process_cpuinfo_bean import ProcessCpuinfoBean
from analyse_resource.bean.system_cpuinfo_bean import SystemCpuinfoBean
from analyse_resource.excel.analyse_resource_excel import AnalyseResourceExcel
from analyse_resource.excel.analyse_resource_excel_data import AnalyseResourceExcelData
from analyse_resource.image.analyse_resource_image import AnalyseResourceImage
from analyse_resource.process_manager import ProcessManager
from utils import resource_utils, adb_utils
from utils import file_utils
from utils.analyse_data_utils import analyse_min_max_average, analyse_str_is_float, analyse_str_is_float_or_int
import time
import psutil
from utils.resource_utils import get_current_package_for_adb, get_sdk_version, get_focused_window


class FpsManager:
    def __init__(self,total,path_name):
        self.total = total
        self.path_name = path_name
        self.device_info_list = []

    def run_fps_sh(self):
        version = int(get_sdk_version())
        print(f"sdk version: {version}, type:{type(version)}")
        if version >= 23:
            print(f"sdk version >= 23")
            cmd = "sh /data/local/tmp/fps_info.sh {0} {1} {2} {3}".format(self.total,
                                                                              "/data/local/tmp/" + self.path_name,
                                                                              "com.tianci.movieplatform", "0")

        else:
            print(f"sdk version < 23")
            cmd = "sh /data/local/tmp/fps_info.sh {0} {1} {2} {3}".format(self.total,
                                                                              "/data/local/tmp/" + self.path_name,
                                                                              get_focused_window(),"1")

        print(f"run fps sh start......")
        adb_utils.shell(cmd).wait()
        print(f"run fps sh end")

    def write_deviceinfo_to_file(self):
        file_utils.save_str_list_to_file(self.path_name, self.device_info_list, "a+")

if __name__ == "__main__":
    device_manager = FpsManager(1,'AppFps')
    device_manager.run_fps_sh()

