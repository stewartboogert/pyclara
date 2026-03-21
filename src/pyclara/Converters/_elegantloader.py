import re as _re
from collections import defaultdict as _defaultdict

def elegant_lte_loader(filename):
    with open(filename) as f:
        content = f.read()

    # Remove comments (! and %)
    content = _re.sub(r'[!%].*', '', content)

    # Join continuation lines
    content = _re.sub(r'&\s*\n', ' ', content)

    # Find all name&type blocks: NAME: TYPE, key=val, key=val ...
    pattern = _re.compile(
        r'([\w-]+)\s*:\s*(\w+)\s*,?\s*([^;]*)',
        _re.IGNORECASE
    )

    elements = _defaultdict(list)

    for match in pattern.finditer(content):
        name, etype, params_str = match.groups()
        params = {"NAME": name.upper()}

        for kv in _re.findall(r'(\w+)\s*=\s*([^,\n]+)', params_str):
            key, val = kv
            val = val.strip().strip('"')
            try:
                params[key.upper()] = float(val)
            except ValueError:
                params[key.upper()] = val

        if etype.upper() == "LINE" :
            val = _re.findall(r'=\((.+)\)',params_str)
            elist = []
            for eval  in val[0].split(","):
                elist.append(eval.strip())
            params["LINE"] = elist

        params['TYPE'] = etype.upper()
        elements[name] = params

    return dict(elements)