
def camel_case_to_snake_case(input_str: str) -> str:
    """
    >>> camel_case_to_snake_case("SomeSDK")
    'some_sdk'
    >>> camel_case_to_snake_case("RServoDrive")
    'r_servo_drive'
    >>> camel_case_to_snake_case("SDKDemo")
    'sdk_demo'
    :param input_str:
    :return:
    """
    chars = []
    for c_idx, char in enumerate(input_str):
        if c_idx and char.isupper():
            next_idx = c_idx + 1
            flag = next_idx >= len(input_str) or input_str[next_idx].isupper()
            prev_char = input_str[c_idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)
