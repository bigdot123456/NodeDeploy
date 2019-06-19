# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""


def JudgeStr2Float(value):
    valueStr = str(value)
    if valueStr.isdigit() is True:
        # 仅仅针对整型，str.isdigit是字符串自带函数
        return True
    else:
        try:
            # 针对浮点型的尝试
            float(valueStr)
        except ValueError:
            return False
        except TypeError:
            return False
        else:
            return True


def JudgeStr2Int(value):
    valueStr = str(value)
    if valueStr.isdigit() is True:
        # 仅仅针对整型，str.isdigit是字符串自带函数
        return True
    else:
        return False


if __name__ == "__main__":
    year = input("输入:")  # 输入 , 默认是字符串

    # if  year.isdigit ( ): # 检测字符串是否由数字组成
    if JudgeStr2Float(year):  # 检测字符串是否由数字组成
        year = int(year)  # 转换成数字

    else:

        exit("invalid year , only accept number")  # 退出并输出 "无效年份,只接受数字"
