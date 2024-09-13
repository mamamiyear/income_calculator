# -*- coding: utf-8 -*-
__author__ = "mamamiyear"

import sys
import math
import argparse
from collections import OrderedDict

month_map = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "1": "Jan",
    "2": "Feb",
    "3": "Mar",
    "4": "Apr",
    "5": "May",
    "6": "Jun",
    "7": "Jul",
    "8": "Aug",
    "9": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
    "bo": "Bonus"
}


def calculate_tax(year_taxed_income):
    """
    按新税法计税
    """
    is_print = False
    if year_taxed_income <= 0:
        if is_print:
            print("year_taxed_income(%9.2f), ratio: 0.00 - 0" % year_taxed_income)
        return 0
    elif year_taxed_income <= 36000:   # (0, 36000]
        if is_print:
            print("year_taxed_income(%9.2f), ratio: 0.03 - 0" % year_taxed_income)
        return round(year_taxed_income * 0.03, 2)
    elif year_taxed_income <= 144000:  # (36000, 144000]
        if is_print:
            print("year_taxed_income(%9.2f), ratio: 0.10 - 2520" % year_taxed_income)
        return round(year_taxed_income * 0.1 - 2520, 2)
    elif year_taxed_income <= 300000:  # (144000, 300000]
        if is_print:
            print("year_taxed_income(%9.2f), ratio: 0.20 - 16920" % year_taxed_income)
        return round(year_taxed_income * 0.2 - 16920, 2)
    elif year_taxed_income <= 420000:  # (300000, 420000]
        if is_print:
            print("year_taxed_income(%9.2f), ratio: 0.25 - 31920" % year_taxed_income)
        return round(year_taxed_income * 0.25 - 31920, 2)
    elif year_taxed_income <= 660000:  # (420000, 660000]
        if is_print:
            print("year_taxed_income(%9.2f), ratio: 0.30 - 52920" % year_taxed_income)
        return round(year_taxed_income * 0.3 - 52920, 2)
    elif year_taxed_income <= 960000:  # (660000, 960000]
        if is_print:
            print("year_taxed_income(%9.2f), ratio: 0.35 - 85920" % year_taxed_income)
        return round(year_taxed_income * 0.35 - 85920, 2)
    else:                              # (960000, max)
        if is_print:
            print("year_taxed_income(%9.2f), ratio: 0.45 - 181920" % year_taxed_income)
        return round(year_taxed_income * 0.45 - 181920, 2)
    pass


def calculate_tax_for_bonus(bonus):
    """
    按新税法计税单独计税
    """
    month_avg_bonus = bonus / 12

    if month_avg_bonus <= 0:
        return 0
    elif month_avg_bonus <= 3000:
        return bonus * 0.03
    elif month_avg_bonus <= 12000:
        return bonus * 0.1 - 210
    elif month_avg_bonus <= 25000:
        return bonus * 0.2 - 1410
    elif month_avg_bonus <= 35000:
        return bonus * 0.25 - 2660
    elif month_avg_bonus <= 55000:
        return bonus * 0.3 - 4410
    elif month_avg_bonus <= 80000:
        return bonus * 0.35 - 7160
    else:
        return bonus * 0.45 - 15160
    pass


def calculate_insurance(old, medical, unemployed):
    """
    计算五险
    """
    is_print = False
    feed_old_insurance = 0.08 * old
    medical_insurance = 0.02 * medical
    unemployed_insurance = 0.004 * unemployed
    if is_print:
        print("feed_old(%0.2f/%0.2f), medical(%0.2f/%0.2f), unemployed(%0.2f/%0.2f)" %
             (feed_old_insurance, old, medical_insurance, medical, unemployed_insurance, unemployed))
    return round(feed_old_insurance + medical_insurance + unemployed_insurance, 2)


def calculate_housing_foundation(housing_base_income, ratio):
    """
    计算一金
    """
    housing_foundation = ratio * housing_base_income
    #print(round(housing_foundation, 2), ratio, housing_foundation)
    return round(housing_foundation, 2)


def calculate_housing_foundation_taxed_income(housing, base):
    """
    计算公积金高出3倍平均月薪部分的应税额度
    """
    taxed_income = housing * 2 - base * 3 * 0.24
    tmp = "%9.2f" % taxed_income
    taxed_income = float(tmp) if base != -1.0 else 0
    taxed_income = 0 if taxed_income <= 0 else taxed_income
    #print("%0.2f housing found taxed income: %0.2f" % (housing, taxed_income))
    return taxed_income


if __name__ == "__main__":
    parser = argparse.ArgumentParser("help of a calculator for your income")
    parser.add_argument("--income", type=str, default="./income.csv", required=False, help="income data file")
    parser.add_argument("--simple", action="store_true", default=False, required=False, help="use simple mode to output")
    args = parser.parse_args()

    income_file_handle = open(args.income, 'r', encoding="UTF-8")
    simple = args.simple

    # 读取数据
    # month_income_map = OrderedDict()
    month_income_list = list()
    bonus = list();
    is_include_bonus = False
    bonus_num = 0
    for line in income_file_handle.readlines():
        content = line.strip().split("#")[0].strip()
        if not content: continue
        income_info = content.split(',')

        if income_info[0].strip("\n").strip().startswith("bo"):
            bonus_num += 1
            bonus_income = income_info[1].strip("\n").strip()
            if bonus_income == "" or not (type(eval(bonus_income)) == int or type(eval(bonus_income)) == float):
                print("ERROR: bonus_income input error.")
                exit(1)
            bonus_tax = income_info[2].strip("\n").strip()
            if bonus_tax == "" or not (type(eval(bonus_tax)) == int or type(eval(bonus_tax)) == float):
                print("ERROR: bonus_tax input error.")
                exit(1)
            bonus_month = income_info[3].strip("\n").strip()
            if bonus_month == "" or not (type(eval(bonus_month)) == int) or bonus_month not in month_map:
                print("ERROR: bonus_month input error.")
                exit(1)
            bonus_single_tax = income_info[4].strip("\n").strip()
            if bonus_single_tax != 'y' and bonus_single_tax != 'n':
                print("ERROR: bonus_single_tax input error.")
                exit(1)
            bonus_name = month_map[bonus_month] + "'s"
            bonus.append((bonus_name, float(bonus_income), float(bonus_tax), int(bonus_month), bonus_single_tax == "y"))
            is_include_bonus = True
        else:
            it = 0
            month_number = income_info[it].strip("\n").strip()
            if month_number not in month_map:
                print("ERROR: month input error.")
                exit(1)
            it += 1
            income = income_info[it].strip("\n").strip()
            if income == "" or not (type(eval(income)) == int or type(eval(income)) == float):
                print("ERROR: income input error.")
                exit(1)
            it += 1
            only_taxed_income = income_info[it].strip("\n").strip()
            if only_taxed_income == "" or not (type(eval(only_taxed_income)) == int or type(eval(only_taxed_income)) == float):
                print("ERROR: only_taxed_income input error.")
                exit(1)
            it += 1
            old_base = income_info[it].strip("\n").strip()
            if old_base == "" or not (type(eval(old_base)) == int or type(eval(old_base)) == float):
                print("ERROR: old insurance base input error.")
                exit(1)
            it += 1
            medical_base = income_info[it].strip("\n").strip()
            if medical_base == "" or not (type(eval(medical_base)) == int or type(eval(medical_base)) == float):
                print("ERROR: medical insurance base input error.")
                exit(1)
            it += 1
            unemployed_base = income_info[it].strip("\n").strip()
            if unemployed_base == "" or not (type(eval(unemployed_base)) == int or type(eval(unemployed_base)) == float):
                print("ERROR: unemployed insurance base input error.")
                exit(1)
            it += 1
            housing_base = income_info[it].strip("\n").strip()
            if housing_base == "" or not (type(eval(housing_base)) == int or type(eval(housing_base)) == float):
                print("ERROR: housing foundation base input error.")
                exit(1)
            it += 1
            housing_ratio = income_info[it].strip("\n").strip()
            if housing_ratio == "" or not (type(eval(housing_ratio)) == int or type(eval(housing_ratio)) == float):
                print("ERROR: housing foundation ratio input error.")
                exit(1)
            it += 1
            ava_income = income_info[it].strip("\n").strip()
            if ava_income == "" or not (type(eval(ava_income)) == int or type(eval(ava_income)) == float):
                print("ERROR: ava_income input error.")
                exit(1)
            it += 1
            extra = income_info[it].strip("\n").strip()
            if extra == "" or not (type(eval(extra)) == int or type(eval(extra)) == float):
                print("ERROR: extra input error.")
                exit(1)
            it += 1
            logic_clear_flag = income_info[it].strip("\n").strip()
            if logic_clear_flag != "y" and logic_clear_flag != "n":
                print("ERROR: logic_clear_flag input error.")
                exit(1)
            it += 1
            avoid_repetitive_base_free = income_info[it].strip("\n").strip()
            if avoid_repetitive_base_free != "y" and avoid_repetitive_base_free != "n":
                print("ERROR: avoid_repetitive_base_free input error.")
                exit(1)
            it += 1
            free_taxed_income = income_info[it].strip("\n").strip()
            if free_taxed_income == "" or not (
                    type(eval(free_taxed_income)) == int or type(eval(free_taxed_income)) == float):
                print("ERROR: free_taxed_income input error.")
                exit(1)
            it += 1

            month_income_list.append((month_number,
                                      float(income),
                                      float(only_taxed_income),
                                      float(old_base),
                                      float(medical_base),
                                      float(unemployed_base),
                                      float(housing_base),
                                      float(housing_ratio),
                                      float(ava_income),
                                      float(extra),
                                      logic_clear_flag == "y",
                                      avoid_repetitive_base_free == "y",
                                      float(free_taxed_income)))

    income_file_handle.close()

    # 历史税前总收入
    history_income = 0

    # 新税法下的统计
    message_list = []
    history_taxed_income = 0  # 历史应税所得额
    history_real_income = 0  # 历史税后收入
    history_tax = 0  # 历史纳税总额
    history_insurace = 0
    history_housing = 0

    # 算税用的逻辑统计
    logic_history_taxed_income = 0
    logic_history_tax = 0

    for (mon,
        income,
        _only_taxed_income,
        _old_insurance_base_income,
        _medical_insurance_base_income,
        _unemployed_insurance_base_income,
        _housing_base_income,
        _housing_ratio,
        _ava_income,
        _extra_spend,
        _logic_clear,
        _avoid_base_free,
        month_free_taxed) in month_income_list:
        # 扣除的三险一金和月免税额度
        current_month_outlay = 0
        current_month_insurance = calculate_insurance(_old_insurance_base_income, _medical_insurance_base_income, _unemployed_insurance_base_income)
        exact_current_month_housing = calculate_housing_foundation(_housing_base_income, _housing_ratio)
        current_month_housing = math.ceil(exact_current_month_housing)
        current_month_free_tax_income = month_free_taxed
        current_month_outlay += current_month_insurance
        current_month_outlay += current_month_housing

        # 个税起征点
        current_month_free_tax_base = 5000 if not _avoid_base_free else 0

        # 历史税前总收入
        history_income += income
        history_income += _only_taxed_income

        # 新税法计税
        current_month_taxed_income = income + _only_taxed_income - current_month_outlay - current_month_free_tax_income - current_month_free_tax_base  # 当月应税额度
        current_month_taxed_income += calculate_housing_foundation_taxed_income(exact_current_month_housing, _ava_income)
        current_month_taxed_income = 0 if current_month_taxed_income <= 0 else current_month_taxed_income
        history_taxed_income += current_month_taxed_income  # 历史应税总收入
        # print(history_taxed_income)
        if _logic_clear:
            logic_history_taxed_income = 0
            logic_history_tax = 0
        logic_history_taxed_income += current_month_taxed_income  # 算税用的逻辑历史应税总收入
        tax = calculate_tax(logic_history_taxed_income) - logic_history_tax  # 当月税额
        # print("%f - %f - %f = %f" % (income, tax, current_month_outlay, income - tax - current_month_outlay))
        real_income = income - tax - current_month_outlay - _extra_spend  # 当月税后收入
        history_tax += tax  # 历史纳税总额
        logic_history_tax += tax  # 算税用的逻辑历史纳税总额
        history_real_income += real_income  # 历史税后收入总额
        history_insurace += current_month_insurance
        history_housing += current_month_housing

        message = "| %s's | income %9.2f | taxed income %9.2f | real income %9.2f | tax %9.2f | insurace %8.2f | housing %8.2f |" % \
                  (month_map[mon], income, current_month_taxed_income, real_income, tax, current_month_insurance, current_month_housing)
        if simple:
            message = "| %s's | income %9.2f | real income %9.2f | housing %8.2f |" % (month_map[mon], income, real_income, current_month_housing)
        message_list.append(message)

        pass

    wage_message = "| Wages | income %9.2f | taxed income %9.2f | real income %9.2f | tax %9.2f | insurace %8.2f | housing %8.2f |" % \
                   (history_income, history_taxed_income, history_real_income, history_tax, history_insurace, history_housing)
    if simple:
        wage_message = "| Wages | income %9.2f | real income %9.2f | housing %8.2f |" % (history_income, history_real_income, history_housing)

    # 年终奖
    bonus_total_message = ""
    bonus_total_income = 0
    bonus_total_tax = 0
    bonus_total_real_income = 0
    bonus_message_list = list()
    if is_include_bonus:
        #print(split_line)
        for (bonus_name, bonus_income, bonus_tax, bonus_month, single_taxed) in bonus:
            bonus_tax = 0
            if single_taxed:
                bonus_tax = calculate_tax_for_bonus(bonus_income) if bonus_tax <= 0 else bonus_tax  # 采用计算结果而非数据结果
            else:
                history_taxed_income += bonus_income
                pass  # TODO: 实现年终奖合并计税
            bonus_real_income = bonus_income - bonus_tax
            bonus_total_income += bonus_income
            bonus_total_tax += bonus_tax
            bonus_total_real_income += bonus_real_income
            history_income += bonus_income
            history_taxed_income += bonus_income  # 历史应税总收入
            history_real_income += bonus_real_income
            history_tax += bonus_tax
            message = "| %s | income %9.2f | taxed income %9.2f | real income %9.2f | tax %9.2f |                   |                  |" % \
                      (bonus_name, bonus_income, bonus_income, bonus_real_income, bonus_tax)
            if simple:
                message = "| %s | income %9.2f | real income %9.2f |                  |" % (bonus_name, bonus_income, bonus_real_income)
            bonus_message_list.append(message)
            pass
        bonus_total_message = "| Bonus | income %9.2f | taxed income %9.2f | real income %9.2f | tax %9.2f |                   |                  |" % \
                  (bonus_total_income, bonus_total_income, bonus_total_real_income, bonus_total_tax)
        if simple:
            bonus_total_message = "| Bonus | income %9.2f | real income %9.2f |                  |" % (bonus_total_income, bonus_total_real_income)

    static_message = "| Total | income %9.2f | taxed income %9.2f | real income %9.2f | tax %9.2f | insurace %8.2f | housing %8.2f |" % \
                     (history_income, history_taxed_income, history_real_income, history_tax, history_insurace, history_housing)
    if simple:
        static_message = "| Total | income %9.2f | real income %9.2f | housing %8.2f |" % (history_income, history_real_income, history_housing)

    total_cash_income = history_real_income + history_housing * 2
    total_cash_message = " TOTAL CASH: %9.2f = %9.2f + %9.2f * 2 (include housing foundation)" % (total_cash_income, history_real_income, history_housing)
    if simple:
        total_cash_message = " TOTAL CASH: %9.2f = %9.2f +%9.2f * 2" % (total_cash_income, history_real_income, history_housing)
    total_cash_blanks = "".join(' ' for _ in range(len(static_message) - len(total_cash_message) - 2))

    # 打印分割线
    split_line = "".join(['-' for _ in range(len(static_message))])
    split_double_line = "".join(['=' for _ in range(len(static_message))])

    print(split_double_line)
    for message in message_list:
        print(message)
    if len(bonus_message_list) > 0:
        print(split_line)
        print(wage_message)
    print(split_line)
    if len(bonus_message_list) > 1:
        for message in bonus_message_list:
            print(message)
        print(split_line)
    if len(bonus_message_list) > 0:
        print(bonus_total_message)
        print(split_double_line)
    print(static_message)
    print(split_line)
    print("|%s%s|" % (total_cash_message, total_cash_blanks))
    print(split_double_line)
