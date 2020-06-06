start_message = ("Вводите симптомы, я постараюсь оценить их, если будет "
                 "чего-то не хватать, я могу уточнить у Вас.\n\n"
                 "/result - как закончите")

node_not_found = "Признак не найден"

something_wrong = "Что-то пошло не так..."


def prediction_to_text(prediction):
    text_list = []
    for p in prediction:
        text = f"{p['name'].upper()}"
        for s, v in p['states'].items():
            text += f"\n{s}: "
            text += "{0:.0%}".format(v)
        text_list.append(text)
    return "\n\n".join(text_list)
