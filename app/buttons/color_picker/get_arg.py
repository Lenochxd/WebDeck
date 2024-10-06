def getarg(message, arg):
    return next(
        (
            x.split(f"{arg}:", 1)[1].strip()
            for x in message.split()
            if x.startswith(f"{arg}:")
        ),
        None,
    )