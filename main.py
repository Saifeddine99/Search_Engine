from demographic_queries import demographic_queries_list
from medical_data_queries import med_data_queries_list
from medical_history_queries import med_hist_queries_list

from common_uuids import extract_common_elements,create_csv_and_display

# Import time module
import time
# record start time
start = time.time()
import pymongo as py
#-----------------------------------------------------------------------------
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]

#Consents collection:
consents_coll=myclient["Consents"]["Consents Collection"]
#-----------------------------------------------------------------------------
import streamlit as st
st.set_page_config(page_title="Search engine", page_icon=":bar_chart:", layout="centered")
#-----------------------------------------------------------------------------
values_strings_demographics=["Name","Surname","DNI","Gender","Country of birth","Province of birth","Town of birth","Street name","Postal Code","Country","Province","Town"]
values_dates_demographics=["Birth date",]
values_floats_demographics=["Street N°",]

all_demog_values_list= values_strings_demographics+values_dates_demographics+values_floats_demographics

chosen_parameters_demog=st.multiselect(
    'Choose demographic conditions combo:',
    (all_demog_values_list)
)

st.write("#")
clinical_data_list=["Age","Vital status","Symptoms", "Clinical desease", "cardiovascular risk factors"]
chosen_parameters_med_data=st.multiselect(
    'Choose medical data conditions combo:',
    (clinical_data_list)
)

st.write("#")
analytics_med_hist=["HbA1c", "UACR", "eGFR", "Height", "Weight", "BMI", "Creatinine_Phosphokinase", "Ejection_fraction", "Platelets", "Serum_Creatinine", "Serum_Sodium"]
chosen_parameters_med_hist=st.multiselect(
    'Choose medical history conditions combo:',
    (analytics_med_hist)
)

chosen_parameters = chosen_parameters_demog + chosen_parameters_med_data + chosen_parameters_med_hist

#query_demog_list is a list of all demographic queries
query_demog_list= demographic_queries_list(chosen_parameters_demog)

#query_med_data_list is a list of all medical data queries
query_med_data_list= med_data_queries_list(chosen_parameters_med_data)

#query_med_hist_list is a list of all medical history queries
query_med_hist_list= med_hist_queries_list(chosen_parameters_med_hist)

if (len(chosen_parameters)):
    st.write("#")
    st.write("#")

    #Adding a button to launch search engine once clicked.
    col1, col2, col3 = st.columns([4,2,3])
    with col2:
        get_result = st.button('See result')

    if get_result:

        #Querying the demographic data based on conditions:
        query_demog={}
        if len(query_demog_list):
            query_demog={"$and": query_demog_list}

        cursor_demog = demographic_data_coll.find(query_demog)

        query_demog_result=[]
        for doc in cursor_demog:
            query_demog_result.append(doc["uuid"])
        #st.write("The number of demographic docs satisfying these conditions is: ",len(query_demog_result))


        #Querying the medical data based on conditions:
        query_med_data={}
        if len(query_med_data_list):
            query_med_data={"$and": query_med_data_list}

        cursor_med_data = medical_data_coll.find(query_med_data)

        query_med_data_result=[]
        for doc in cursor_med_data:
            query_med_data_result.append(doc["uuid"])
        #st.write("The number of medical data docs satisfying these conditions is: ",len(query_med_data_result))
    

        #Querying the medical history data based on conditions:
        query_med_hist={}
        if len(query_med_hist_list):
            query_med_hist={"$and": query_med_hist_list}

        cursor_med_hist = medical_hist_coll.find(query_med_hist)

        query_med_hist_result=[]
        for doc in cursor_med_hist:
            query_med_hist_result.append(doc["uuid"])
        #st.write("The number of medical hist docs satisfying these conditions is: ",len(query_med_hist_result))

        consents_cursor=consents_coll.find({})
        consent_uuids=[]
        for doc in consents_cursor:
            consent_uuids.append(doc["uuid"])

        #Matching "uuid":
        common_uuid=extract_common_elements(query_demog_result,query_med_data_result,query_med_hist_result,consent_uuids)
        
        st.write("#")
        #st.write("total number of common data: ",len(common_uuid))

        if common_uuid:

            #preparing the demographic data to be displayed:
            gender=[]

            cursor_demog = demographic_data_coll.find({"uuid": {"$in": common_uuid}})
            for demographic_doc in cursor_demog:
                if demographic_doc["uuid"] in common_uuid:
                    gender.append(demographic_doc["demographic data"]["details"]["items"][0]["items"][4]["value"]["value"])

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


            cursor_med_data=medical_data_coll.find({"uuid": {"$in": common_uuid}})
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
            
            cursor_med_hist=medical_hist_coll.find({"uuid": {"$in": common_uuid}})
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
            csv_dict={"Gender":gender,
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
            create_csv_and_display(csv_dict)


        else:
            st.error("No result found for this query")


else:
    st.warning("You need to choose a variable to create a condition")