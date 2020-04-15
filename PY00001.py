import pandas as pd
import sys
import operator
import FS_Shared


def calculate_ratio(df):
    resolved_by_action_group = {}
    calls_by_action_group = {}
    close_ratio_by_action_group = {}

    for index, row in df.iterrows():
        if row['CaseResolvedDateTime'] is not pd.NaT:
            resolved_by_action_group[row['TeamID']] = resolved_by_action_group.get(row['TeamID'], 0) + 1

    print ('@@PY00001:resolved_by_action_group', len(resolved_by_action_group))

    for index, row in df.iterrows():
        calls_by_action_group[row['TeamID']] = calls_by_action_group.get(row['TeamID'], 0) + 1

    print ('@@PY00001:calls_by_action_group', len(calls_by_action_group))

    for key in calls_by_action_group:
        #if calls_by_action_group[key] > 50:
        if key in resolved_by_action_group:
            ratio = float(resolved_by_action_group[key]) / float(calls_by_action_group[key]) * 100
            close_ratio_by_action_group[key] = ratio

    print ('@@PY00001:close_ratio_by_action_group', len(close_ratio_by_action_group))

    if len(close_ratio_by_action_group) == 0:
        return None

    return sorted(close_ratio_by_action_group.items(), key=operator.itemgetter(1),
                                                reverse=False)


def main():

    num_of_arguments = len(sys.argv) - 1
    if num_of_arguments != 5:
        print ("@@PY00001:received wrong number of arguments:", num_of_arguments)
    else:

        question_id = sys.argv[1]
        user_id = sys.argv[2]
        date_from = int(sys.argv[3])
        date_to = int(sys.argv[4])
        date_unit = sys.argv[5].lower()

        print ("@@PY00001:received parameters:", question_id, user_id, date_from, date_to, date_unit)

        (start_date, end_date) = FS_Shared.get_date_period(date_from, date_to, date_unit)

        dimension = FS_Shared.get_question_parameters(question_id)['dimension_id']

        filter = "WHERE CaseCreationDateTime between '" + start_date + "' and '" + end_date + "' and " + dimension + " <> -1"

        df = FS_Shared.get_dataframe(question_id, filter)

        number_of_records = len(df)

        print ("@@PY00001:number of records:", number_of_records)

        if number_of_records == 0:
            exit()

        (dimension_member_id, dimension_member_id_ratio) = calculate_ratio(df)[0]

        print ('@@PY00001:' + dimension, dimension_member_id, dimension_member_id_ratio)

        number_of_iteration = 0
        if date_unit == 'y':
            if date_to == date_from:
                number_of_iteration = 12
            else:
                number_of_iteration = (date_to - date_from) * 12
        elif date_unit == 'm':
            if date_to == date_from:
                number_of_iteration = 52
            else:
                number_of_iteration = (date_to - date_from) * 52
        elif date_unit == 'd':
            if date_to == date_from:
                number_of_iteration = 1
            else:
                number_of_iteration = (date_to - date_from)

        elements = []

        for delta in range(number_of_iteration):
            (s_date, e_date) = FS_Shared.get_date_slicer(start_date, delta, date_unit)

            filter = "WHERE CaseCreationDateTime between '" + s_date + "' and '" + e_date + \
                     "' and TeamID = '" + str(dimension_member_id) + "'"

            df = FS_Shared.get_dataframe(question_id, filter)

            ratio_result = calculate_ratio(df)

            if ratio_result is not None:
                (dimension_member_id, ratio) = ratio_result[0]
                element_dict = {dimension: dimension_member_id,
                                FS_Shared.get_kpi_title(question_id).replace(" ", ""): "{0:.2f}".format(ratio),
                                "Month": FS_Shared.get_month_name(s_date)}
                elements.append(element_dict)

        df = pd.DataFrame(elements)

        result = FS_Shared.Result(question_id, user_id)

        element = FS_Shared.Element(FS_Shared.Element.ElementType.List, df)

        result.add_element(element)

        element = FS_Shared.Element(FS_Shared.Element.ElementType.Sentence,
                                    None,
                                    dimension,
                                    dimension_member_id,
                                    FS_Shared.get_kpi_title(question_id),
                                    FS_Shared.AggregateFunction.get_aggregate_function_name(FS_Shared.AggregateFunction.Average),
                                    FS_Shared.get_date_relative_text(date_from, date_to, date_unit),
                                    "{0:.2f}".format(dimension_member_id_ratio)
                                    )

        result.add_element(element)

        result.save()


if __name__ == "__main__":
    main()
