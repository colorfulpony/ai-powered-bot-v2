def repeat_gpt_answer_5_time(func, url_or_text, schema, question):
    var = ""
    i = 0
    while i < 5:
        var = func(url_or_text, schema, question)
        if var != "-":
            break
        i = i + 1
    return var