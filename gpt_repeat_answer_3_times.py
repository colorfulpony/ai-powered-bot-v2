async def repeat_gpt_answer_3_time(func, text, input):
    var = "-"
    i = 0
    while i < 3:
        var = await func(text, input)
        if "I don't know" in var or "This document does not" in var or "context does not provide" in var:
            i = i + 1
            var = "-"
        else:
            break

    return var
