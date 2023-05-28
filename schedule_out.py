import numpy as np
import pandas as pd
from schedule_functions import *

def write_res_for_groups(prob_res):
  res_groups = np.chararray((len(all_groups), len(all_slots), len(all_days)), itemsize=1000, unicode=True).astype(str)
  res_groups[:] = ""
  for i in range(len(all_groups)):
    print(f"\nГруппа:{all_groups[i]}")
    for l in range(len(all_days)):
      for m in range(len(all_slots)):
        for k in range(len(all_teachers)):
          for j in range(len(all_subjects)):
              if prob_res[f"x_({i},_{j},_{k},_{l},_{m})"].value() == 1:
                format = get_format(all_teachers[k], all_subjects[j])
                res_groups[i, m, l] += all_subjects[j] +", " + all_teachers[k] + ", " + format + "; "
        if (len(res_groups[i, m, l]) > 0):
          print(f"{all_days[l]} {all_slots[m]}  {res_groups[i, m, l]}")

  with pd.ExcelWriter("Groups_schedule.xlsx") as writer:
    for i in range(len(all_groups)):
      data =  pd.DataFrame(res_groups[i], columns=all_days, index=all_slots)
      data.to_excel(writer, sheet_name=f"{all_groups[i]}")
      worksheet = writer.sheets[f"{all_groups[i]}"]
      workbook=writer.book
      format = workbook.add_format({'text_wrap': True})
      worksheet.set_column(0, 0, 20, format)
      for j, col in enumerate(data.columns):
        worksheet.set_column(j + 1, j + 1, 50, format)
      worksheet.set_column(3, 4, 20, format)

def write_res_for_teachers(prob_res):
  res = np.chararray((len(all_teachers), len(all_slots), len(all_days)), itemsize=200, unicode=True).astype(str)
  res[:] = ""
  for k in range(len(all_teachers)):
    print(f"\nПреподаватель:{all_teachers[k]}")
    for l in range(len(all_days)):
      for m in range(len(all_slots)):
        subjects = set()
        for j in range(len(all_subjects)):
          for i in range(len(all_groups)):
            if prob_res[f"x_({i},_{j},_{k},_{l},_{m})"].value() == 1:
              subjects.add(all_subjects[j])
              res[k, m, l] += str(all_groups[i]) + ','
        if len(res[k, m, l]) > 0:
          res[k, m, l] += str(list(subjects))
          format = get_format(all_teachers[k], str(list(subjects)[0]))
          res[k, m, l] += ", " + format
          for q in range(len(all_auds)):
            for j in range(len(all_subjects)):
              if prob_res[f"a_({j},_{k},_{l},_{m},_{q})"].value() == 1:
                res[k, m, l] += ", " + all_auds[q]
          print(f"{all_days[l]} {all_slots[m]}  {res[k, m, l]}")


  with pd.ExcelWriter("Teachers_schedule.xlsx") as writer:
    for k in range(len(all_teachers)):
        data = pd.DataFrame(res[k], columns=all_days, index=all_slots)
        data.to_excel(writer, sheet_name=f"{all_teachers[k]}")
        worksheet = writer.sheets[f"{all_teachers[k]}"]
        workbook=writer.book
        format = workbook.add_format({'text_wrap': True})
        worksheet.set_column(0, 0, 20, format)
        for j, col in enumerate(data.columns):
          worksheet.set_column(j + 1, j + 1, 30, format)
