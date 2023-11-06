import streamlit as st
from paths import parameter_to_directory

analytics_med_hist=["HbA1c", "UACR", "eGFR", "Height", "Weight", "BMI", "Creatinine_Phosphokinase", "Ejection_fraction", "Platelets", "Serum_Creatinine", "Serum_Sodium"]

def med_hist_queries_list(chosen_parameters_med_hist):
    #query_med_hist_list is a list of all medical history queries
    query_med_hist_list=[]
    if len(chosen_parameters_med_hist)>0:
        for value in chosen_parameters_med_hist:
            st.header(value.upper()+":")
            query_med_hist={}

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
                        min_value=lower_value
                        )
                else:
                    input_value = st.number_input(
                        "Value of "+value+":"
                        )
            
            if value in ["Height", "Weight", "BMI"]:
                if selected=="equal":
                    query_med_hist={parameter_to_directory(value): input_value}
                elif selected== "not equal":
                    query_med_hist={parameter_to_directory(value): {"$ne": input_value}}
                elif selected== "greater":
                    query_med_hist={parameter_to_directory(value): {"$gt": input_value}}
                elif selected== "greater or equal":
                    query_med_hist={parameter_to_directory(value): {"$gte": input_value}}
                elif selected== "lower":
                    query_med_hist={parameter_to_directory(value): {"$lt": input_value}}
                elif selected== "lower or equal":
                    query_med_hist={parameter_to_directory(value): {"$lte": input_value}}
                elif selected=="between":
                    query_med_hist={"$and":[{parameter_to_directory(value): {"$gte": lower_value}},
                                {parameter_to_directory(value): {"$lte": higher_value}}
                                ]
                        }

            else:
                
                if selected== "equal":
                    query_med_hist={"analytics.0": {"$elemMatch":{
                        parameter_to_directory("laboratory test name"): {'$regex':  f'^{value}$', '$options': 'i'},
                        parameter_to_directory("laboratory test result"): input_value}
                    }}

                elif selected== "not equal":
                    query_med_hist={"$or":[{"analytics.0":
                    {"$elemMatch":
                       {parameter_to_directory("laboratory test name"): {'$regex':  f'^{value}$', '$options': 'i'},
                        parameter_to_directory("laboratory test result"): {"$ne": input_value}}
                    }},
                    {"analytics.0"+"."+parameter_to_directory("laboratory test name"):{"$not":{'$regex':  f'^{value}$', '$options': 'i'}}}
                    ]}

                elif selected== "greater":
                    query_med_hist={"analytics.0": {"$elemMatch":{
                        parameter_to_directory("laboratory test name"): {'$regex':  f'^{value}$', '$options': 'i'},
                        parameter_to_directory("laboratory test result"): {"$gt": input_value}}
                    }}

                elif selected== "greater or equal":
                    query_med_hist={"analytics.0": {"$elemMatch":{
                        parameter_to_directory("laboratory test name"): {'$regex':  f'^{value}$', '$options': 'i'},
                        parameter_to_directory("laboratory test result"): {"$gte": input_value}}
                    }}

                elif selected== "lower":
                    query_med_hist={"analytics.0": {"$elemMatch":{
                        parameter_to_directory("laboratory test name"): {'$regex':  f'^{value}$', '$options': 'i'},
                        parameter_to_directory("laboratory test result"): {"$lt": input_value}}
                    }}

                elif selected== "lower or equal":
                    query_med_hist={"analytics.0": {"$elemMatch":{
                        parameter_to_directory("laboratory test name"): {'$regex':  f'^{value}$', '$options': 'i'},
                        parameter_to_directory("laboratory test result"): {"$lte": input_value}}
                    }}

                elif selected=="between":
                    query_med_hist={"analytics.0": {"$elemMatch":{
                        parameter_to_directory("laboratory test name"): {'$regex':  f'^{value}$', '$options': 'i'},
                        "$and":[{parameter_to_directory("laboratory test result"): {"$gte": lower_value}},
                                {parameter_to_directory("laboratory test result"): {"$lte": higher_value}}
                                ]
                        
                    }}}
                
            #Here we gonna add the specific query related to this chosen condition to the list of queries           
            query_med_hist_list.append(query_med_hist)

    return(query_med_hist_list)