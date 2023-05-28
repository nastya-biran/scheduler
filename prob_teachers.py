from pulp import *
import numpy as np
import pandas as pd
from prob_variables import *


def group_limits_for_teachers(prob):
    #Преподаватель ведет семинар не более чем у одной группы одновременно, лекцию не более чем у количества групп, которые записаны
    for k in range(len(all_teachers)):
        for j in get_subjects_by_teacher(all_teachers[k]):
            num_classes = 1
            if ("Лекции" in all_subjects[j]) or (all_subjects[j] in all_electives):
                num_classes = len(get_groups_by_subject(all_subjects[j]))
            for l in range(len(all_days)):
                for m in range(len(all_slots)):
                    prob += lpSum([attends[(i, j, k, l, m)]
                                for i in range(len(all_groups))]) <= num_classes

    #Преподаватель ведет электив(семинар) не более, чем у 40 человек
    for k in range(len(all_teachers)):
        subjects_for_teacher = get_subjects_by_teacher(all_teachers[k])
        for subject in subjects_for_teacher:
            if (subject in all_electives_ind) and ("Семинары" in all_subjects[subject]):
                for l in range(len(all_days)):
                    for m in range(len(all_slots)):
                        prob += lpSum([attends[(i, subject, k, l, m)] * get_group_size(all_groups[i], all_subjects[subject])
                                        for i in range(len(all_groups))]) <= 40


def no_more_than_one_subject_for_each_slot(prob):
    #Каждый преподаватель ведет не более одного предмета одновременно
    initialise_teacher_has_class(prob)
    for k in range(len(all_teachers)):
        for l in range(len(all_days)):
            for m in range(len(all_slots)):
                prob += lpSum([teacher_has_class[(j, k, l, m)] for j in get_subjects_by_group(all_groups[i])]) <= 1


def all_groups_on_the_lecture(prob):
    #Если это лекция, то на ней должны присутствовать все записанные группы одновременно
    initialise_teacher_has_class(prob)
    for j in range(len(all_subjects)):
        if "Лекции" in all_subjects[j]:
            groups_num = len(get_groups_by_subject(all_subjects[j]))
            for k in range(len(all_teachers)):
                for l in range(len(all_days)):
                    for m in range(len(all_slots)):
                        prob += teacher_has_class[(j, k, l, m)] * groups_num == lpSum([attends[(i, j, k, l, m)] for i in range(len(all_groups))])   





      
def same_teacher_for_each_subject(prob):
    #Лекции/семинары должен вести один и тот же преподаватель
    initialise_is_teacher_for_this_subject_and_group(prob)
    for i in range(len(all_groups)):
        for j in range(len(all_subjects)):
            prob += lpSum([is_teacher_for_this_subject_and_group[(i, j, k)] for k in range(len(all_teachers))])  <= 1


def no_classes_on_required_days(prob):
    #Отсутствие пар в определенные дни
    for k in range(len(all_teachers)):
        forbidden_days_answer = teachers_data[teachers_data["Преподаватель"] == all_teachers[k]].iloc[0]["Дни без пар"]
        if pd.notna(forbidden_days_answer):
            forbidden_days = [all_days.index(day) for day in forbidden_days_answer.split(", ")]
            for l in forbidden_days:
                prob += lpSum([attends[(i, j, k, l, m)]
                                for i in range(len(all_groups))
                                for j in range(len(all_subjects))
                                for m in range(len(all_slots))]) == 0

    
def all_classes_on_one_day(prob):
    #Все пары в один день
    initialise_teacher_has_classes_for_day(prob)
    for k in range(len(all_teachers)):
        in_one_day_answer = teachers_data[teachers_data["Преподаватель"] == all_teachers[k]]
        if in_one_day_answer.iloc[0]["Все пары в один день"] == "Да": 
            prob += lpSum([teacher_has_classes_for_day[(k, l)] for l in range(len(all_days))]) == 1


def limits_for_classes_per_week(prob, classes_overall):
    #Ограничение по количеству пар для преподавателей
    for k in range(len(all_teachers)):
        mn, mx = get_classes_per_week_for_teacher(all_teachers[k])
        prob += mn <= lpSum([teacher_has_class[(j, k, l, m)]
                        for j in range(len(all_subjects))
                        for l in range(len(all_days))
                        for m in range(len(all_slots))]) <= mx
        classes_overall += mn

def build_constraits_for_teachers():
    group_limits_for_teachers(prob)
    no_more_than_one_subject_for_each_slot(prob)
    all_groups_on_the_lecture(prob)
    same_teacher_for_each_subject(prob)
    no_classes_on_required_days(prob)
    all_classes_on_one_day(prob)
    limits_for_classes_per_week(prob, classes_overall)
