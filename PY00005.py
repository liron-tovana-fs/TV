import pandas as pd
import FS_Shared as FS
import sys 


"""
Multiple Visits is almost 70% dependent on/correlated with XXX

"""


def main():
    NumOfArguments = len(sys.argv) 
    print(NumOfArguments)
    if NumOfArguments != 6:
        print ("Received wrong number of arguments")
    else:
        QuestionID = sys.argv[1]
        UserID = sys.argv[2]

        Activities = FS.get_dataframe(QuestionID)
        dimName = FS.get_question_parameters(QuestionID).get("dimension_id")
        Dates = FS.get_date_period(int(sys.argv[3]), int(sys.argv[4]), sys.argv[5].lower())

        #Multiple visit is defined by having several activities with different arrival dates
        #Prepare the data -filter by open date
        Mask =  (Activities['ArriveDateTime'].notnull()) & (Activities['CaseCreationDateTime'].between(Dates[0], Dates[1]))
        Cases = Activities[Mask].groupby(['CaseID', 'ArriveDateTime'], as_index=False).count().groupby('CaseID')['CaseID'].count().to_frame(name = 'Count').reset_index()
        Cases["MultipleVisits"] = Cases["Count"] > 1
        
        #KPI calculation
        merged = pd.merge(left=Activities, right=Cases, how='left', left_on='CaseID', right_on='CaseID')
        merged.sort_values("CaseID", inplace = True) 
        merged.drop_duplicates(subset ="CaseID", keep = "first", inplace = True)

        merged['dim_cat']=merged[dimName].astype('category').cat.codes
        merged['MultipleVisits_cat']=merged['MultipleVisits'].astype('category').cat.codes
        merged[["MultipleVisits", "dim_cat"]].corr()


                  
        result = FS.Result(QuestionID, UserID)
        element = FS.Element(FS.Element.ElementType.List, pd_top)
        result.add_element(element)

        element = FS.Element(FS.Element.ElementType.Sentence,None,dimName,None, FS.get_kpi_title(QuestionID),None, sys.argv[5].lower() , None, FS.FilterCase.get_filter_case_name(FS.FilterCase.Top), 3 )
        result.add_element(element)

        result.save()



if __name__ == "__main__":
    main()