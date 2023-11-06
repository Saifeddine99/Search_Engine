import streamlit as st
from paths import parameter_to_directory

clinical_data_list=["Clinical desease","cardiovascular risk factors"]
vital_status_age_symptoms=["Vital status", "Age","Symptoms"]

def med_data_queries_list(chosen_parameters_med_data):
    #query_med_data_list is a list of all demographic queries
    query_med_data_list=[]

    if len(chosen_parameters_med_data)>0:
        for value in chosen_parameters_med_data:
            st.header(value.upper()+":")
            query_med_data={}

            #If the value is a string:
            if value in clinical_data_list:
                col01,col02,col03 = st.columns([1.25,.25,2])
                with col01:
                    selected=st.selectbox(
                        "Condition for "+value+" :",
                        ("equal","different")
                    )
                with col03:
                    input_value= st.text_input("Value of " + value + ":")

                key="problem list"
                if value=="cardiovascular risk factors":
                    key="risk factors"

                if selected=="equal":
                    query_med_data={key:{"$elemMatch":{
                        parameter_to_directory(value): {'$regex':  f'^{input_value}$', '$options': 'i'}}
                    }}

                else:
                    query_med_data={"$or":[{key+"."+parameter_to_directory(value):{
                        "$not":{'$regex':  f'^{input_value}$', '$options': 'i'}}
                    },
                    {key: []}]
                    }

            #If the value is a string:
            elif value in vital_status_age_symptoms :
                if value=="Age":
                    col01,col02,col03 = st.columns([1.25,.25,2])
                    with col01:
                        selected=st.selectbox(
                            "Condition for "+value+" :",
                            ("equal","not equal","greater","lower","greater or equal","lower or equal", "between")
                        )
                    with col03:
                        if selected=="between":
                            lower_value = st.number_input(
                                "Lower value of "+value+":"
                                )
                            
                            higher_value = st.number_input(
                                "Higher value of "+value+":",
                                )

                        else:
                            input_value = st.number_input(
                                "Value of "+value+":"
                                )

                    if selected=="equal":
                        query_med_data={parameter_to_directory(value): input_value}
                    elif selected== "not equal":
                        query_med_data={parameter_to_directory(value): {"$ne": input_value}}
                    elif selected== "greater":
                        query_med_data={parameter_to_directory(value): {"$gt": input_value}}
                    elif selected== "greater or equal":
                        query_med_data={parameter_to_directory(value): {"$gte": input_value}}
                    elif selected== "lower":
                        query_med_data={parameter_to_directory(value): {"$lt": input_value}}
                    elif selected== "lower or equal":
                        query_med_data={parameter_to_directory(value): {"$lte": input_value}}
                    elif selected=="between":
                        query_med_data={"$and":[{parameter_to_directory(value): {"$gte": lower_value}},
                                    {parameter_to_directory(value): {"$lte": higher_value}}
                                    ]
                            }

                else:
                    col01,col02,col03 = st.columns([1.25,.25,2])
                    with col01:
                        selected=st.selectbox(
                            "Condition for "+value+" :",
                            ("equal","different")
                        )
                    with col03:
                        input_value=(st.text_input("Value of " + value + ":"))
                    if selected=="equal":
                        query_med_data={parameter_to_directory(value): {'$regex':  f'^{input_value}$', '$options': 'i'}}
                    else:
                        query_med_data={parameter_to_directory(value): {'$not': {'$regex': f'^{input_value}$', '$options': 'i'}}}
                    
            #Here we gonna add the specific query related to this chosen condition to the list of queries           
            query_med_data_list.append(query_med_data)
    
    return(query_med_data_list)