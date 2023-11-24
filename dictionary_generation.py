import pymongo as py
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]
#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]
#---------------------------------------------------------------------------
def dict_generation(consent_uuids):
    #preparing the demographic data to be displayed:
    gender=[]

    cursor_demog = demographic_data_coll.find({"uuid": {"$in": consent_uuids}})
    for demographic_doc in cursor_demog:
        #if demographic_doc["uuid"] in consent_uuids:
        gender.append(demographic_doc["demographic data"]["details"]["items"][3]["value"]["value"])

    #gender = gender[1:] + [gender[0]]

    #preparing the medical data to be displayed:
    age=[]
    vital_status=[]
    symptoms=[]

    anaemia=[]
    diabetes=[]
    frailty=[]
    heart_failure=[]
    established_CVD=[]
    hepatic_steatosis=[]
    strokes=[]

    hypertension=[]
    hypercholesterolemia=[]
    albuminuria=[]
    smoking=[]
    early_CVD=[]


    cursor_med_data=medical_data_coll.find({"uuid": {"$in": consent_uuids}})
    for med_data_doc in cursor_med_data:
        try:
            age.append(med_data_doc["age"]["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"])
        except:
            age.append("Unknown")
        try:
            vital_status.append(med_data_doc["vital status"]["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"])
        except:
            vital_status.append("Unknown")
        try:
            symptoms.append(med_data_doc["symptoms"]["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"])
        except:
            symptoms.append("Unknown")

        anaemia.append("NO")
        diabetes.append("NO")
        frailty.append("NO")
        heart_failure.append("NO")
        established_CVD.append("NO")
        hepatic_steatosis.append("NO")
        strokes.append("NO")

        try:
            problem_list=list(med_data_doc["problem list"])
            for problem in problem_list:
                problem_name=problem["content"][0]["items"][0]["data"]["items"][0]["value"]["value"]
                if problem_name==("anaemia").upper():
                    anaemia[-1]="YES"
                if problem_name==("diabetes").upper():
                    diabetes[-1]="YES"
                if problem_name==("frailty").upper():
                    frailty[-1]="YES"
                if problem_name==("heart_failure").upper():
                    heart_failure[-1]="YES"
                if problem_name==("established_CVD").upper():
                    established_CVD[-1]="YES"
                if problem_name==("hepatic_steatosis").upper():
                    hepatic_steatosis[-1]="YES"
                if problem_name==("strokes").upper():
                    strokes[-1]="YES"
        except:
            pass

        hypertension.append("NO")
        hypercholesterolemia.append("NO")
        albuminuria.append("NO")
        smoking.append("NO")
        early_CVD.append("NO")

        try:
            risk_factors=list(med_data_doc["risk factors"])
            for cvrf in risk_factors:
                cvrf_name=cvrf["content"][0]["data"]["items"][1]["items"][0]["value"]["value"]
                
                if cvrf_name==("High_blood_pressure").upper():
                    hypertension[-1]="YES"
                if cvrf_name==("hypercholesterolemia").upper():
                    hypercholesterolemia[-1]="YES"
                if cvrf_name==("albuminuria").upper():
                    albuminuria[-1]="YES"
                if cvrf_name==("smoking").upper():
                    smoking[-1]="YES"
                if cvrf_name==("family history of early CVD").upper():
                    early_CVD[-1]="YES"

        except:
            pass

        
    #preparing the medical history to be displayed:
    height=[]
    weight=[]
    bmi=[]
    hba1c=[]
    egfr=[]
    uacr=[]
    creatinine_phosphokinase=[]
    ejection_fraction=[]
    platelets=[]
    serum_creatinine=[]
    serum_sodium=[]
    
    cursor_med_hist=medical_hist_coll.find({"uuid": {"$in": consent_uuids}})
    for med_hist_doc in cursor_med_hist:
        try:
            height.append(med_hist_doc["analytics"][1]["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"])
        except:
            height.append("Unknown")
        try:
            weight.append(med_hist_doc["analytics"][1]["content"][1]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"])
        except:
            weight.append("Unknown")
        try:
            bmi.append(med_hist_doc["analytics"][1]["content"][2]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"])
        except:
            bmi.append("Unknown")
        
        hba1c.append("Unknown")
        egfr.append("Unknown")
        uacr.append("Unknown")
        creatinine_phosphokinase.append("Unknown")
        ejection_fraction.append("Unknown")
        platelets.append("Unknown")
        serum_creatinine.append("Unknown")
        serum_sodium.append("Unknown")

        try:
            analytics=list(med_hist_doc["analytics"][0])
            for test in analytics:
                test_name=test["content"][0]["data"]["events"][0]["data"]["items"][0]["value"]["value"]
                test_result=test["content"][0]["data"]["events"][0]["data"]["items"][6]["items"][2]["value"]["magnitude"]
                if test_name==("egfr").upper():
                    egfr[-1]=test_result
                if test_name==("uacr").upper():
                    uacr[-1]=test_result
                if test_name==("hba1c").upper():
                    hba1c[-1]=test_result
                if test_name==("creatinine_phosphokinase").upper():
                    creatinine_phosphokinase[-1]=test_result
                if test_name==("ejection_fraction").upper():
                    ejection_fraction[-1]=test_result
                if test_name==("platelets").upper():
                    platelets[-1]=test_result
                if test_name==("serum_creatinine").upper():
                    serum_creatinine[-1]=test_result
                if test_name==("serum_sodium").upper():
                    serum_sodium[-1]=test_result

        except:
            pass

    #Putting data to be displayed in a dictionary:
    csv_dict={  "Gender":gender,
                "Age":age,
                "Vital Status":vital_status,
                "Symptoms":symptoms,

                "Anaemia":anaemia,
                "Diabetes":diabetes,
                "Frailty":frailty,
                "Heart Failure":heart_failure,
                "Established CVD":established_CVD,
                "Hepatic Steatosis":hepatic_steatosis,
                "Strokes":strokes,

                "Smoking":smoking,
                "High Blood Pressure":hypertension,
                "Albuminuria":albuminuria,
                "Hypercholesterolemia":hypercholesterolemia,
                "Family History Of Early CVD":early_CVD,

                "Height": height,
                "Weight": weight,
                "BMI": bmi,

                "HbA1c": hba1c,
                "eGFR": egfr,
                "UACR": uacr,
                "Creatinine_Phosphokinase": creatinine_phosphokinase,
                "ejection_Fraction": ejection_fraction,
                "Platelets": platelets,
                "Serum_Creatinine":serum_creatinine,
                "Serum_sodium":serum_sodium
                }

    return csv_dict