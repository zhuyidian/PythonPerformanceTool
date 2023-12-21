
from utils.resource_utils import get_sdk_version, push_shell_to_device

if __name__ == "__main__":
    push_shell_to_device('shell/fps_info.sh')
    push_shell_to_device('shell/cpu_usage_test.sh')

