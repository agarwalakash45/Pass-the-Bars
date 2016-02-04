import cx_Freeze

executables=[cx_Freeze.Executable("PassBars.py")]

cx_Freeze.setup(
    name="Pass the Bars",
    options={"build_exe":{"packages":["pygame"]}},
    executables=executables
    )
