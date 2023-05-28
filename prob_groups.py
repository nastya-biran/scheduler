from pulp import *
import numpy as np
import pandas as pd
from prob_variables import *


def comleteness_for_groups(prob):
    for i in range(len(all_groups)):
        needed_subjects = get_subjects_by_group(all_groups[i])
        for j in needed_subjects:
            #Группа должна посещать указанное количество лекций/семинаров каждого нужного предмета у кого-то из учителей, которые ведут этот предмет
            available_teachers = get_teachers_by_subject(all_subjects[j])
            num = groups_data[groups_data["Номер группы"] == all_groups[i]][all_subjects[j]].iloc[0]
            prob += lpSum([attends[(i, j, k, l, m)]
                        for k in available_teachers
                        for l in range(len(all_days))
                        for m in range(len(all_slots))]) == num
            #Нельзя ходить на лекцию/семинар к учителю, который не ведет этот предмет
            unavailable_teachers = list(set(range(len(all_teachers))) - set(available_teachers))
            prob += lpSum([attends[(i, j, k, l, m)]
                        for k in unavailable_teachers
                        for l in range(len(all_days))
                        for m in range(len(all_slots))]) == 0
        #Нельзя ходить на ненужные предметы
        unneeded_subjects = list(set(range(len(all_subjects))) - set(needed_subjects))
        for j in unneeded_subjects:
            prob += lpSum([attends[(i, j, k, l, m)]
                        for k in range(len(all_teachers))
                        for l in range(len(all_days))
                        for m in range(len(all_slots))]) == 0




def no_conflicts_between_subjects(prob):
    #Два основных предмета не могут стоять одновременно
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            for m in range(len(all_slots)):
                prob += lpSum([attends[(i, j, k, l, m)]
                                for j in all_base_ind
                                for k in get_teachers_by_subject(all_subjects[j])]) <= 1

        #Элективные предметы могут стоять одновременно
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            for m in range(len(all_slots)):
                prob += lpSum([attends[(i, j, k, l, m)]
                                for j in all_electives_ind
                                for k in get_teachers_by_subject(all_subjects[j])]) <= len(all_electives)

    #Семинар и лекция по одному элективному предмету не могут стоять одновременно
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            for m in range(len(all_slots)):
                for subject in all_electives:
                    if "Лекции" in subject:
                        prob += lpSum([attends[(i, j, k, l, m)]
                                    for j in get_elective_seminar_by_elective_lecture(subject)
                                    for k in get_teachers_by_subject(all_subjects[j])]) <= 1


    #Группе назначается не более одного преподавателя на каждый слот
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            for m in range(len(all_slots)):
                for j in get_subjects_by_group(all_groups[i]):
                    prob += lpSum([attends[(i, j, k, l, m)]
                                for k in get_teachers_by_subject(all_subjects[j])]) <= 1

    #Основной предмет не может стоять одновременно с элективным
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            for m in range(len(all_slots)):
                prob += lpSum([attends[(i, j, k, l, m)]
                                for j in all_base_ind
                                for k in get_teachers_by_subject(all_subjects[j])]) * len(all_electives) + lpSum([attends[(i, j, k, l, m)]
                                                                                    for j in all_electives_ind
                                                                                    for k in get_teachers_by_subject(all_subjects[j])]) <= len(all_electives)







def no_classes_on_special_slots(prob):
    for i in range(len(all_groups)):
        #В день майнора и военки основных пар не должно быть
        has_minor, has_military_day = check_for_minor_and_military_day(all_groups[i])
        if has_minor == 1:
            prob += lpSum([attends[(i, j, k, 2, m)] 
                            for j in get_subjects_by_group(all_groups[i])
                            for k in get_teachers_by_subject(all_subjects[j])
                            for m in range(len(all_slots))]) == 0
        if has_military_day == 1:
            prob += lpSum([attends[(i, j, k, 3, m)] 
                            for j in get_subjects_by_group(all_groups[i])
                            for k in get_teachers_by_subject(all_subjects[j])
                            for m in range(len(all_slots))]) == 0
        #Нельзя ставить пары в слоты английского  
        english_slots = get_english_slots(all_groups[i])
        if len(english_slots) > 0:
            for day_and_slots in english_slots:
                prob += lpSum([attends[(i, j, k, day_and_slots[0], m)]
                                for j in get_subjects_by_group(all_groups[i])
                                for k in get_teachers_by_subject(all_subjects[j])
                                for m in day_and_slots[1:]]) == 0

#Условие 2.5
#Каждый предмет у группы не больше пары в день
def not_more_than_one_class_for_each_subject_per_day(prob):
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            for j in get_subjects_by_group(all_groups[i]):
                prob += lpSum([attends[(i, j, k, l, m)]
                                for k in get_teachers_by_subject(all_subjects[j])
                                for m in range(len(all_slots))]) <= 1



def no_more_than_four_classes_per_day(prob):
    initialise_group_has_class(prob)
    #В день не больше 4 пар
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            prob += lpSum([group_has_class[(i, l, m)]
                            for m in range(len(all_slots))]) <= 4

def build_constraits_for_groups():
    comleteness_for_groups(prob)
    no_conflicts_between_subjects(prob)
    no_classes_on_special_slots(prob)
    not_more_than_one_class_for_each_subject_per_day(prob)
    no_more_than_four_classes_per_day(prob)