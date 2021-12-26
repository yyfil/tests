# TODO: handle 1/128 delta

def math_function(x: int):
    # handle delta:
    if x % (1 / 128) != 0.0:
        raise ValueError(f'Value increment step should equal to 1/128. '
                         f'Input value: {x}. x mod 1/128 = {x % (1 / 128)}')
    if -10 <= x <= -2:
        return -(x*x)
    elif (-2 < x < 8) and (x != -1):
        return (1 - x) / (1 + x)
    elif 8 < x <= 35:
        return abs(x - 12)
    else:
        raise ValueError(f'Function accepts values in ranges [-10, -2], (-2, 8), x!=1 and (8, 35]. '
                         f'Input value: {x}')

