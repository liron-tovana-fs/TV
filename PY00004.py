import pandas as pd
import FS_Shared as FS
import sys 


"""
The 3 products with the highest multiple visits in the last week are:
*  X with 100.0  % of multiple visits
*  Y with 50.0  % of multiple visits
*  Z with 33.33  % of multiple visits
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

        # number of dim on multi visit set
        Mask = merged["MultipleVisits"] == True
      
        # number of dim on full set
        GroupByDim = merged.groupby([dimName])[dimName].count().to_frame(name = 'Num1')
        MultiVisitGroupByDim = merged[Mask].groupby([dimName])[dimName].count().to_frame(name = 'Num2')
     
        NewMerged = pd.merge(left=GroupByDim, right=MultiVisitGroupByDim, how='left', left_on=dimName,right_on=dimName)
     
        Mask = (NewMerged["Num2"].isnull() == False)
        NewMerged = NewMerged[Mask]
         
        NewMerged["Precent"] = round ((NewMerged["Num2"] * 100)/NewMerged["Num1"],2)
        pd_top = NewMerged.sort_values(by='Precent', ascending=False).head(3)
           
        result = FS.Result(QuestionID, UserID)

        element = FS.Element(FS.Element.ElementType.List, pd_top)
        result.add_element(element)

        element = FS.Element(FS.Element.ElementType.Sentence,None,dimName,None, FS.get_kpi_title(QuestionID),None, sys.argv[5].lower() , None, FS.FilterCase.get_filter_case_name(FS.FilterCase.Top), 3 )
        result.add_element(element)

        result.save()



if __name__ == "__main__":
    main()