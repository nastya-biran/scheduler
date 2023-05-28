from pulp import *
import numpy as np
import pandas as pd
from prob_variables import *


def class_may_be_assigned_only_to_one_free_aud(prob):
    #Количество пар в аудитории не больше, чем свободность аудитории
    for l in range(len(all_days)):
        for m in range(len(all_slots)):
            for q in range(len(all_auds)):
                prob += lpSum([a[(j, k, l, m, q)]
                                for k in range(len(all_teachers))
                                for j in range(len(all_subjects))]) <= auds_free[(q, l, m)]


def every_offline_class_should_be_assigned_to_aud(prob):
    #Каждому преподавателю нужна подходящая аудитория, если стоит пара
    for l in range(len(all_days)):
        for m in range(len(all_slots)):
            for k in range(len(all_teachers)):
                for j in range(len(all_subjects)):
                    if is_offline(all_teachers[k], all_subjects[j]):
                        available_auds, unavailable_auds = get_available_and_unavailable_auds(all_subjects[j])
                        prob += lpSum([a[(j, k, l, m, q)]
                                        for q in available_auds]) == teacher_has_class[(j, k, l, m)]
                        prob += lpSum([a[(j, k, l, m, q)]
                                        for q in unavailable_auds]) == 0
                    else:
                        prob += lpSum([a[(j, k, l, m, q)]
                                        for q in range(len(all_auds))]) == 0

#Условие 5.3
aud_capacities = list(auds_data["Вместимость"])
def aud_capacity_is_more_than_students_amount(prob):
    #Вместимость аудитории не меньше, чем количество студентов на занятии
    for l in range(len(all_days)):
        for m in range(len(all_slots)):
            for k in range(len(all_teachers)):     
                prob += lpSum([a[(j, k, l, m, q)] * aud_capacities[q]
                                    for j in range(len(all_subjects))
                                    for q in get_available_and_unavailable_auds(all_subjects[j])[0]]) - lpSum([attends[(i, j, k, l, m)] * get_group_size(all_groups[i], all_subjects[j])*is_offline(all_teachers[k], all_subjects[j])
                                                                                        for i in range(len(all_groups))
                                                                                        for j in range(len(all_subjects))]) >= 0

def build_constraits_for_auds():
    class_may_be_assigned_only_to_one_free_aud(prob)
    every_offline_class_should_be_assigned_to_aud(prob)
    aud_capacity_is_more_than_students_amount(prob)

