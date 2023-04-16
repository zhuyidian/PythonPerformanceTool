from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator


class AnalyseResourceImage:
    def __init__(self,path):
        self.path = path

    def do_cpuinfo_image(self,name,label,x_list,y_list,min,max,average):
        file_name = str(name).replace(' ','').replace(':', '').replace('\\', '').replace('/', '')

        # 根据数据绘制图形,
        # plt.figure(figsize=(15, 7.5), dpi=600)
        plt.figure(figsize=(15, 7.5), dpi=80)
        # 生成网格
        # plt.grid()
        plt.grid(axis="y")
        # 折线图
        # if package_name[0] == 'com.oneapp.max.security.pro.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="PPP")
        # elif package_name[0] == 'com.oneapp.max.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Opt1.6.1")
        # elif package_name[0] == 'com.boost.clean.coin.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Fastclear")
        # elif package_name[0] == 'com.walk.sports.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Walk")
        # elif package_name[0] == 'com.diamond.coin.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Amber")
        # elif package_name[0] == 'com.oneapp.max.cleaner.booster.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Space")
        # else:
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label=row_name)
        plt.plot(x_list, y_list, "c-", linewidth=1, label=label)
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.xlabel('time(H:Min:S)', fontsize=16)
        plt.ylabel("cpu_realtime(%)", fontsize=16)
        # plt.title("cpu real time line chart", fontsize=24)
        plt.title(f'min({min}) max({max}) average({average})', fontsize=24)
        plt.legend()
        # 横坐标显示间隔
        if len(x_list) <= 15:
            pass
        else:
            t = int(len(x_list) / 15)
            plt.xticks(range(0, len(x_list), t))

        # 设置横纵坐标格式
        y_major_locator = MultipleLocator(5)  # 把y轴的刻度间隔设置为10，并存在变量里
        ax = plt.gca()  #ax为两条坐标轴的实例
        ax.yaxis.set_major_locator(y_major_locator)  # 把y轴的主刻度设置为10的倍数
        plt.ylim(0, 100)  #把y轴的刻度范围设置为0到100，同理，0不会标出来，但是能看到一点空白

        # 旋转日期
        plt.gcf().autofmt_xdate()
        # path = performance_child_dir + row_name + ".jpg"
        # print(f"path: {path}")
        plt.savefig(f'{self.path}/{file_name}')
        plt.close()

    def do_meminfo_image(self,name,label,x_list,y_list,min,max,average):
        file_name = str(name).replace(' ','').replace(':', '').replace('\\', '').replace('/', '')

        # 根据数据绘制图形,
        # plt.figure(figsize=(15, 7.5), dpi=600)
        plt.figure(figsize=(15, 7.5), dpi=80)
        # 生成网格
        # plt.grid()
        plt.grid(axis="y")
        # 折线图
        # if package_name[0] == 'com.oneapp.max.security.pro.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="PPP")
        # elif package_name[0] == 'com.oneapp.max.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Opt1.6.1")
        # elif package_name[0] == 'com.boost.clean.coin.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Fastclear")
        # elif package_name[0] == 'com.walk.sports.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Walk")
        # elif package_name[0] == 'com.diamond.coin.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Amber")
        # elif package_name[0] == 'com.oneapp.max.cleaner.booster.cn':
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Space")
        # else:
        #     plt.plot(wights, highs_float, "c-", linewidth=1, label=row_name)
        plt.plot(x_list, y_list, "c-", linewidth=1, label=label)
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.xlabel('time(H:Min:S)', fontsize=16)
        plt.ylabel("Number(Mb)", fontsize=16)
        # plt.title("cpu real time line chart", fontsize=24)
        plt.title(f'min({min})MB max({max})MB average({average})MB', fontsize=24)
        plt.legend()
        # 横坐标显示间隔
        if len(x_list) <= 15:
            pass
        else:
            t = int(len(x_list) / 15)
            plt.xticks(range(0, len(x_list), t))

        # 设置横纵坐标格式
        # y_major_locator = MultipleLocator(10)  # 把y轴的刻度间隔设置为10，并存在变量里
        # ax = plt.gca()  #ax为两条坐标轴的实例
        # ax.yaxis.set_major_locator(y_major_locator)  # 把y轴的主刻度设置为10的倍数
        # plt.ylim(0, 500)  #把y轴的刻度范围设置为0到100，同理，0不会标出来，但是能看到一点空白

        # 旋转日期
        plt.gcf().autofmt_xdate()
        # path = performance_child_dir + row_name + ".jpg"
        # print(f"path: {path}")
        plt.savefig(f'{self.path}/{file_name}')
        plt.close()