def get_overflow(sample: dict, obj: dict, all_sub=False) -> list:
    """Returns a list of all fields which exist in obj, but not in sample."""
    fields = []
    if hasattr(obj, "__iter__"):
        for field in obj:
            if field not in sample:
                fields.append(field)
            else:
                if all_sub and type(obj[field]) == dict:
                    fs = get_overflow(sample[field]["embedded_dict"], obj[field], all_sub)
                    fields.extend(fs)
        return fields
    else:
        return []


def check(sample: dict, obj: dict, parent=None, allow_overflow=False) -> (bool, list):
    """Performs type checking on obj against sample. Returns True or False if obj fits the sample. If obj does not fit, then return an array of errors."""
    # Check if there are other fields in obj, than in sample
    errors = []

    if parent:
        parent_key = parent + "."
    else:
        parent_key = ""

    overflows = get_overflow(sample, obj)
    if not allow_overflow and len(overflows) > 0:
        if len(overflows) == 1:
            errors.append(f"ERROR: Key '{parent_key + overflows[0]}' is not present in sample, but is present in supplied object.")
        else:
            errors.append(f"ERROR: Keys {[parent_key + o for o in overflows]} are not present in sample, but are present in supplied object.")

    for key in sample:

        if parent:
            parent_key = parent + "." + key
        else:
            parent_key = key

        key_req = sample[key]["required"]
        # Key is required and is absent.
        if key_req and key not in obj:
            errors.append(f"ERROR: Key '{parent_key}' is required, but was absent in supplied object.")
            continue
        elif key in obj:  # Key is present, required or not.
            # Type for this key in obj is not in allowed types
            if type(obj[key]) not in sample[key]["allowed_types"]:
                errors.append(f"ERROR: On key '{parent_key}'', expected one of {[t.__name__ for t in sample[key]['allowed_types']]}, got {type(obj[key]).__name__}")
                continue
            else:  # Type for this key in obj is in allowed types
                # If the obj-type is dict (implied from above if-statement, it is allowed), then we try to resursively check.
                if type(obj[key]) == dict:
                    embedded = sample[key]["embedded_dict"]
                    succ, err = check(embedded, obj[key], parent_key, allow_overflow)

                    if not succ:
                        errors.extend(err)
                        continue
                elif type(obj[key]) == list:
                    # Check all list elements somehow
                    l_ele = sample[key]["list_element"]

                    for i, ele in enumerate(obj[key]):
                        if type(ele) not in l_ele["allowed_types"]:
                            errors.append(f"ERROR: On key '{parent_key}[{i}]', expected one of {[t.__name__ for t in l_ele['allowed_types']]}, got {type(ele).__name__}")
                        # ele has to match l_ele.
                        if type(ele) == dict:
                            succ, err = check(l_ele["embedded_dict"], ele, parent_key + f"[{i}]", allow_overflow)
                            if not succ:
                                errors.extend(err)

                elif type(obj[key]) == tuple:
                    order = sample[key]["tuple_order"]
                    if len(order) != len(obj[key]):
                        errors.append(f"ERROR: On key '{parent_key}', expected tuple of length {len(order)}, got tuple of length {len(obj[key])}.")
                        continue

                    for i in range(len(order)):
                        if type(obj[key][i]) != order[i]:
                            errors.append(f"ERROR: On key '{parent_key}', expected tuple with order ({','.join([t.__name__ for t in order])}), got tuple with order ({','.join([type(t).__name__ for t in obj[key]])}).")
                            break
                    for i in range(len(order)):
                        if type(obj[key][i]) == dict:
                            succ, err = check(sample[key]["embedded_dict"], obj[key][i], parent_key + f"[{i}]", allow_overflow)
                            if not succ:
                                errors.extend(err)

                        if type(obj[key][i]) == list:
                            # Check all list elements somehow
                            l_ele = sample[key]["list_element"]

                            for i, ele in enumerate(obj[key][i]):
                                if type(ele) not in l_ele["allowed_types"]:
                                    errors.append(f"ERROR: On key '{parent_key}[{i}]', expected one of {[t.__name__ for t in l_ele['allowed_types']]}, got {type(ele).__name__}.")
                                # ele has to match l_ele.
                                if type(ele) == dict:
                                    succ, err = check(l_ele["embedded_dict"], ele, parent_key + f"[{i}]", allow_overflow)
                                    if not succ:
                                        errors.extend(err)
    return len(errors) == 0, errors
