import FS_Shared as FS
import sys 
import pandas as pd




def main():
    NumOfArguments = len(sys.argv) 
    if NumOfArguments != 6:
        print ("Received wrong number of arguments")
    else:
        QuestionID = sys.argv[1]
        UserID = sys.argv[2]
    
        Orders = FS.get_dataframe(QuestionID)
        dimName = FS.get_question_parameters(QuestionID)
        Dates = FS.get_date_period(int(sys.argv[3]), int(sys.argv[4]), sys.argv[5].lower())

        #KPI calculation
        #Closing ratio is defined by dividing the number of resolved calls by the number of opened calls in a given time

        #Prepare the data -filter by open date
        Mask =  (Orders['CaseCreationDateTime'].notnull()) & (Orders['CaseCreationDateTime'].between(Dates[0], Dates[1]))
        DimListOpen = Orders[Mask].groupby([dimName])["CaseCreationDateTime"].count()

        #Prepare the data -filter by Resolved Date
        Mask =  (Orders['CaseResolvedDateTime'].notnull()) & (Orders['CaseResolvedDateTime'].between(Dates[0], Dates[1]))
        DimListResolved= Orders[Mask].groupby([dimName])["CaseResolvedDateTime"].count()

        pd_conect = pd.concat([DimListOpen, DimListResolved], axis=1) 
        pd_conect["ClosingRatio"] = round(pd_conect["CaseResolvedDateTime"] / pd_conect["CaseCreationDateTime"],2)

        pd_conect.sort_values(by='ClosingRatio', ascending=False)

        pd_top = pd_conect.sort_values(by='ClosingRatio', ascending=False).head(3)
        pd_top.drop('CaseCreationDateTime', axis=1, inplace=True)
        pd_top.drop('CaseResolvedDateTime', axis=1, inplace=True)

           
        result = FS.Result(QuestionID, UserID)

        element = FS.Element(FS.Element.ElementType.List, pd_top)
        result.add_element(element)

        element = FS.Element(FS.Element.ElementType.Sentence,None,dimName,None, FS.get_kpi_title(QuestionID),None, "week" , None, FS.FilterCase.get_filter_case_name(FS.FilterCase.Top), 3 )
        result.add_element(element)

        result.save()


if __name__ == "__main__":
    main()

   


