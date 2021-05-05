#version1.0.0
import pandas as pd
import numpy as np

required_dict = {"ガード性能":3,"ガード強化":2,"攻めの守勢":2,"回避距離UP":1}


def is_required_satisfied(skill_df,required_dict):
    required_satisfied = True
    for skill in required_dict.keys():
        required_satisfied = required_satisfied and skill_df[skill] >= required_dict[skill]
    return required_satisfied        
basic_column = ["helm","mail","arm","coil","greave","def_sum","slot_large","slot_mid","slot_small"]
required_skill_column = ["required Skill " + str(i+1) for i in range(len(required_dict))]
skill_column = ["Skill " + str(i+1) for i in range(10)]

df = pd.read_csv('MHR_skillsheat0505.csv',encoding = "SHIFT-JIS").fillna(0)
result_df = pd.DataFrame(columns = basic_column + required_skill_column + skill_column)
#print(result_df.columns)

for skill in required_dict.keys():
    if skill not in df.columns:
        print("UNEXIST SKILL NAME!: "+ skill)
        exit()

helm_df = df[df["部位"] == 1]
mail_df = df[df["部位"] == 2]
arm_df = df[df["部位"] == 3]
coil_df = df[df["部位"] == 4]
greave_df = df[df["部位"] == 5]

for i in range(int(len(helm_df))):
    for j in range(int(len(mail_df))):
        for k in range(int(len(arm_df))):
            for l in range(int(len(coil_df))):
                for m in range(int(len(greave_df))):
                    skill_df = helm_df.iloc[i,6:] + mail_df.iloc[j,6:] + arm_df.iloc[k,6:] + coil_df.iloc[l,6:] + greave_df.iloc[m,6:]
                    required_satisfied = is_required_satisfied(skill_df,required_dict)
                    if required_satisfied:
                        equipname_list = [ helm_df.iloc[i,0], mail_df.iloc[j,0], arm_df.iloc[k,0], coil_df.iloc[l,0], greave_df.iloc[m,0] ]
                        
                        def_sum = helm_df.iloc[i,2] + mail_df.iloc[j,2] + arm_df.iloc[k,2] + coil_df.iloc[l,2] + greave_df.iloc[m,2]
                        slot_list = (helm_df.iloc[i,3:6] + mail_df.iloc[j,3:6] + arm_df.iloc[k,3:6] + coil_df.iloc[l,3:6] + greave_df.iloc[m,3:6]).values.tolist()
                        required_skill_list = [ skill + " (Lv." + str(int(skill_df[skill])) + ")" for skill in required_dict.keys()]
                        activated_skill_df = skill_df[skill_df > 0].sort_values(ascending = False)
                        nonrequired_activated_skill_list = []
                        for activated_skill in activated_skill_df.index:
                            if activated_skill not in required_dict.keys():
                                nonrequired_activated_skill_list.append(activated_skill + " (Lv." + str(int(skill_df[activated_skill])) + ")")
            
                        equip_list = equipname_list + [def_sum] + slot_list + required_skill_list + nonrequired_activated_skill_list
                        equip_list = equip_list + [np.nan for _ in range(len(result_df.columns)-len(equip_list))]
            
                        equip_df = pd.DataFrame(columns = result_df.columns)
                        equip_df.loc[1] = equip_list
                        result_df = pd.concat([result_df, equip_df],ignore_index = True)
result_df = result_df.sort_values(ascending = False,by = "def_sum")
result_df.to_csv("equiplist_test1.csv",encoding = "SHIFT-JIS")


        