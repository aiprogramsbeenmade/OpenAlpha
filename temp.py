from openalpha.web.app import _execute_with_params
result = _execute_with_params("limit", "sin(x)/x", {"point": "oo"})
print(result.exact, result.metadata)
