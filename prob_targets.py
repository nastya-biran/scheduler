from pulp import *
import numpy as np
import pandas as pd
from prob_variables import *



def teacher_preferences(prob):
    #Совпадения с предпочтениями преподавателей
    prob += lpSum([pref_table[k, l, m] * teacher_has_class[(j, k, l, m)]
                for j in range(len(all_subjects))
                for k in range(len(all_teachers)) 
                for l in range(len(all_days)) 
                for m in range(len(all_slots))])== tgt1



def windows_for_students(prob):
    #Минимизация окон для студентов
    initialise_windows(prob)
    prob += lpSum([windows[(i, l)]
                for i in range(len(all_groups))
                for l in range(len(all_days))]) == tgt2




def study_days(prob):
    #Минимизация количества учебных дней
    prob += lpSum([has_classes[(i, l)] 
                for i in range(len(all_groups))
                for l in range(len(all_days))]) == tgt3




def online_days(prob):
    #Минимизация количества дней, в которых есть хотя бы одна онлайн пара
    initialise_has_online_classes(prob)
    prob += lpSum([has_online_classes[(i, l)] 
                for i in range(len(all_groups))
                for l in range(len(all_days))]) == tgt4



def study_saturdays(prob):
    #Отсутствие пар в субботу
    prob += lpSum([has_classes[(i, 5)] 
                for i in range(len(all_groups))]) == tgt5


def elective_classes(prob):
    #Количество пар, в которые стоит хотя бы один элективный предмет
    initialise_group_has_elective(prob)
    prob += lpSum([group_has_elective[(i, l, m)]
                    for i in range(len(all_groups))
                    for l in range(len(all_days))
                    for m in range(len(all_slots))]) == tgt6


def build_targets():
    teacher_preferences(prob)
    windows_for_students(prob)
    study_days(prob)
    online_days(prob)
    study_saturdays(prob)
    elective_classes(prob)
