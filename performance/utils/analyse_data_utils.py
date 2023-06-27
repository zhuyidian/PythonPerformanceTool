
"""
从浮点类型的列表中计算最小值，最大值，平均值
"""
def analyse_min_max_average(highs_float):
    # 输出最低值和最高值
    highs_hl = sorted(highs_float)
    low_value = highs_hl[0]
    # print(f"最低值：{low_value}")
    high_value = highs_hl[len(highs_hl) - 1]
    # print(f"最高值：{high_value}")
    # 输出平均值
    total = 0
    for value in highs_float:
        total += value
    average_value = round(total / len(highs_float), 2)
    # print(f"平均值：{average_value}")
    return low_value,high_value,average_value

"""
判断字符串是否是浮点数
"""
def analyse_str_is_float(value_str):
    value_str = str(value_str)
    if value_str.count('.') == 1:
        new_s = value_str.split('.')
        left_num = new_s[0]
        right_new = new_s[1]
        if right_new.isdigit():
            if left_num.isdigit(): #正小数
                return True
            elif left_num.count('-') == 1 and left_num.startswith('-'): #负小数
                temp_num = left_num.split('-')[-1]
                if temp_num.isdigit():
                    return True
    return False

"""
判断字符串是否是整数
"""
def analyse_str_is_int(value_str):
    value_str = str(value_str)
    if value_str.count('.') == 0:  # 整数
        if value_str.isdigit():
            return True
        elif value_str.count('-') == 1 and value_str.startswith('-'):  # 负整数
            ss = value_str.split('-')[-1]
            if ss.isdigit():
                return True
    return False

"""
判断字符串是否是浮点数或整数
"""
def analyse_str_is_float_or_int(value_str):
    value_str = str(value_str)
    if value_str.count('.') == 1:  # 浮点数
        new_s = value_str.split('.')
        left_num = new_s[0]
        right_new = new_s[1]
        if right_new.isdigit():
            if left_num.isdigit(): #正小数
                return True
            elif left_num.count('-') == 1 and left_num.startswith('-'): #负小数
                temp_num = left_num.split('-')[-1]
                if temp_num.isdigit():
                    return True
    elif value_str.count('.') == 0:  # 整数
        if value_str.isdigit():
            return True
        elif value_str.count('-')==1 and value_str.startswith('-'):  # 负整数
            ss = value_str.split('-')[-1]
            if ss.isdigit():
                return True

    return False

