import base64
from e2b_code_interpreter import Sandbox

code_to_run = """
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()
"""

sandbox = Sandbox()

# Run the code inside the sandbox
execution = sandbox.run_code(code_to_run)

# There's only one result in this case - the plot displayed with `plt.show()`
first_result = execution.results[0]

if first_result.png:
    # Save the png to a file. The png is in base64 format.
    with open("chart.png", "wb") as f:
        f.write(base64.b64decode(first_result.png))
    print("Chart saved as chart.png")
