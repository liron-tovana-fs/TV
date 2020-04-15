#
# Copyright 2020 TOVANA-FS. All rights reserved.
#


"""
Core client functionality, common across all API requests (including performing
HTTP requests).
"""

import json
import enum
import FS_DatabaseManager
import FS_DateManager


class AggregateFunction(enum.Enum):
    Average = 1
    Count = 2
    Maximum = 3
    Median = 4
    Minimum = 5
    Mode = 6
    Range = 7
    Sum = 8
    Top = 9

    @staticmethod
    def get_aggregate_function_name(aggregate_function):
        print ("@@FS_shared.get_aggregate_function_name", aggregate_function)

        return aggregate_function.name


class FilterCase(enum.Enum):
    Top = 1
    EqualTo = 2
    NotEquals = 3
    GreaterThan = 4
    GreaterThanOrEqualTo = 5
    LessThan = 6
    LessThanOrEqualTo = 7

    @staticmethod
    def get_filter_case_name(filter_case):
        print ("@@FS_shared.get_filter_case_name", filter_case)

        return filter_case.name


def place_value(number):
    return ("{:,}".format(number))


def get_kpi_title(question_id):

    query = "select kpi_id from fs_questions where question_id ='" + question_id + "'"

    kpi_id = FS_DatabaseManager.execute_query(query)[0]

    print ("@@FS_shared.get_kpi_title", query)

    query = "select description from fs_kpis where kpi_id ='" + kpi_id + "'"

    kpi_title = FS_DatabaseManager.execute_query(query)[0]

    print ("@@FS_shared.get_kpi_title", kpi_title)

    return kpi_title


def get_date_slicer(start_date, delta, date_unit):
    return FS_DateManager.get_date_slicer(start_date, delta, date_unit)


def get_dataframe(question_id, filter=None):

    query = "select query from fs_questions where question_id ='" + question_id + "'"

    selected_query = FS_DatabaseManager.execute_query(query)[0]

    if filter is not None:
        selected_query += ' ' + filter

    print ("@@FS_shared.get_dataframe", selected_query)

    return FS_DatabaseManager.get_dataframe(selected_query)


def get_question_parameters(question_id):

    query = "select parameters from fs_questions where question_id ='" + question_id + "'"

    print ("@@FS_shared.get_question_parameters.query", query)

    parameters = json.loads(FS_DatabaseManager.execute_query(query)[0])#.replace('\'', '')

    print ("@@FS_shared.get_question_parameters.parameters", parameters)

    param_dict = {}
    for key in parameters:
        if key == 'parameters':
            print '@@@@@'
            for parameter in parameters[key]:
                for key_parameter in parameter:
                    param_dict[key_parameter] = parameter[key_parameter]

    print ("@@FS_shared.get_question_parameters.param_dict", param_dict)

    return param_dict


def get_answer_id(question_id):

    query = "select answer_id from fs_questions where question_id ='" + question_id + "'"

    answer_id = FS_DatabaseManager.execute_query(query)[0]

    print ("@@FS_shared.get_answer_id", answer_id)

    return answer_id


def get_date_period(date_from, date_to, date_unit):
    return FS_DateManager.get_date_period(date_from, date_to, date_unit.lower())


def get_date_relative_text(date_from, date_to, date_unit):
    return FS_DateManager.get_date_relative_text(date_from, date_to, date_unit.lower())


def get_month_name(date):
    return FS_DateManager.get_month_name(date)


class Element:

    element_type = None

    class ElementType(enum.Enum):
        Sentence = 1
        List = 2

    class SubElementType(enum.Enum):
        Declarative = 1
        Exclamatory = 2
        Table = 3
        Bullet = 4

    def __init__(self, element_type, df, dimension_name="", dimension_member_name="", kpi_title="",
                 aggregate_function="", date_period="", data_value="", filter_case="", filter_case_value=""):
        self.element_type = element_type
        self.dimension_name = dimension_name
        self.kpi_title = kpi_title
        self.date_period = date_period
        self.dimension_member_name = dimension_member_name
        self.aggregate_function = aggregate_function
        self.filter_case = filter_case
        self.filter_case_value = filter_case_value
        self.data_value = data_value
        if df is not None:
            self.list = df.reset_index()


class Result:

    def __init__(self, question_id, user_id):
        self.sentenceElements = []
        self.listElements = []
        self.question_id = question_id
        self.user_id = user_id

    def add_element(self, element):
        if element.element_type == Element.ElementType.Sentence:
            self.sentenceElements.append(element)
        elif element.element_type == Element.ElementType.List:
            self.listElements.append(element)

    def save(self):
        json_string = "{\"result\":["
        sentence = {}
        index = 0
        for element in self.sentenceElements:
            sentence['<dimension-name_' + str(index) + '>'] = element.dimension_name
            sentence['<dimension-member-name_' + str(index) + '>'] = element.dimension_member_name
            sentence['<kpi-title_' + str(index) + '>'] = element.kpi_title
            sentence['<aggregate-function_' + str(index) + '>'] = element.aggregate_function
            sentence['<filter-case_' + str(index) + '>'] = element.filter_case
            sentence['<filter-case-value_' + str(index) + '>'] = element.filter_case_value
            sentence['<date-period_' + str(index) + '>'] = element.date_period
            sentence['<data-value_' + str(index) + '>'] = element.data_value
            index += 1
            json_string += "{\"type\":\"" + Element.ElementType.Sentence.name + "\", \"fields\":" + json.dumps(sentence) + "},"

        for element in self.listElements:
            df_list = element.list.T.to_dict('dict')
            json_string += "{\"type\":\"" + Element.ElementType.List.name + "\", \"fields\":" + json.dumps(df_list) + "},"

        json_string = json_string[:-1]
        json_string += "]}"

        query = "INSERT INTO T1.dbo.FS_answers (answer_id, question_id, created_by, created_at, result)" \
                " VALUES('" + get_answer_id(self.question_id) + "', '" + self.question_id + "', '" + self.user_id + "','" + \
                FS_DateManager.get_today().strftime("%Y-%m-%d %H:%M:%S") + "', '" + json_string + "')"

        print ("@@FS_shared.save_result", query)

        FS_DatabaseManager.execute_query(query, True)

