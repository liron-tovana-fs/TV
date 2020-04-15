import pandas as pd
import json
import sys
import FS_Shared
import FS_DatabaseManager


def get_answer_result(question_id):

    query = "select TOP 1 result, answer_id from fs_answers where question_id ='" + question_id + "' order by answer_index desc"

    print ("@@FS_DisplayInsight.get_answer_result", query)

    result = FS_DatabaseManager.execute_query(query)

    if result is not None:
        answer_result, answer_id = result
        return json.loads(answer_result), answer_id

    return [None, None]


def load_answer_language(answer_id):
    query = "select answer_text from FS_answers_languages where answer_id ='" + answer_id + "'"

    print ("@@FS_DisplayInsight.load_answer_language", query)

    answer_text = FS_DatabaseManager.execute_query(query)[0]

    return json.loads(answer_text)


def generate_bullet_list(output_string, df_fields):
    for row in df_fields:
        row_output_string = output_string
        for index in df_fields.index:
            token = "@@" + index + "@@"
            if token in row_output_string:
                row_output_string = row_output_string.replace(token, str(df_fields.loc[index][row]))
        print ('* ' + row_output_string)


def generate_sentence(fields, answer_language):
    language_sentence = ''
    for p in answer_language['tvml']:
        if 'type' in p:
            element_type = p['type']
            if element_type == FS_Shared.Element.ElementType.Sentence.name:
                language_sentence = p['value']

                for key in fields:
                    language_sentence = language_sentence.replace(key, str(fields[key]))

    return language_sentence


def generate_list(fields, answer_language):
    df_fields = pd.DataFrame(fields)
    output_string = ""
    for p in answer_language['tvml']:
        if 'type' in p:
            element_type = p['type']
            if element_type == FS_Shared.Element.ElementType.List.name:
                if FS_Shared.Element.SubElementType.Bullet.name in p['subtype']:
                    for column in p['columns']:
                        if 'field' in column:
                            if column['field'] in df_fields.index:
                                output_string += " @@" + column['field'] + "@@ "
                        else:
                            output_string += column['text']

                    generate_bullet_list(output_string, df_fields)

    '''
    idx = 0
    result_dict = {}
    for index in df_fields.index:
        if index in columns:
            row = []
            for element in df_fields.iloc[idx]:
                row.append(element)
            result_dict[columns[index]] = row

        idx += 1

    return pd.DataFrame(result_dict)
    '''


def display_answer(question_id):
    (answer_result, answer_id) = get_answer_result(question_id)
    if answer_result is None:
        print ("@@FS_DisplayInsight.display_answer could not load answer to question " + str(question_id))
    else:
        answer_language = load_answer_language(answer_id)
        if answer_language is None:
            print ("@@FS_DisplayInsight.display_answer could not load answer language to question " + str(question_id))
        else:
            for element in answer_result['result']:
                if 'type' in element:
                    (element_type, element_value) = element['type'], element['fields']
                    if element_type == FS_Shared.Element.ElementType.Sentence.name:
                        print (generate_sentence(element_value, answer_language))
                    elif element_type == FS_Shared.Element.ElementType.List.name:
                        generate_list(element_value, answer_language)


def main():
    num_of_arguments = len(sys.argv) - 1
    if num_of_arguments != 1:
        print ("@@FS_DisplayInsight:received wrong number of arguments:", num_of_arguments)
    else:

        question_id = sys.argv[1]

        print ("@@FS_DisplayInsight:received parameters:", question_id)

        display_answer(question_id)


if __name__ == "__main__":
    main()