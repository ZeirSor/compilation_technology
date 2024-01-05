# LR(0) Parsing Research - Course Project

## Project Overview

This project is a course project for compiler technology, focusing on the implementation and in-depth study of LR(0)
parsing. The main objectives and content of the project are outlined below:

1. **Grammar Definition:** Define the LR(0) grammar using production rules.

2. **Canonical Item Set Family:** Provide the canonical item set family for LR(0) parsing, representing all states.

3. **State Relationships:** Describe the relationships between different states in the canonical item set family.

4. **LR(0) Parsing Table:** Construct the LR(0) parsing table, showcasing the parsing actions and state transitions for
   the grammar.

5. **Symbol String Analysis:** Given a symbol string, determine whether it is a valid sentence in the grammar and print
   the analysis process using the parsing table.

## Project Structure

```
├── README.md
├── requirements.txt
├── run_lr0_console.py
├── run_lr0_ui.py
├── core
│   ├── canonical_item_set.py
│   ├── dfa.py
│   ├── grammar.py
│   ├── item.py
│   ├── lr0_parser.py
│   ├── production_formula.py
│   └── __init__.py
├── examples
│   ├── example1.txt
│   ├── example2.txt
│   └── ...
├── test-output
│   ├── example1.txt-dfa-to-graph.gv
│   └── ...
├── ui
│   ├── mainwindow.py
│   ├── mainwindow.ui
│   ├── my_graphics_view.py
│   ├── my_mainwindow.py
│   └── __init__.py
└── utils
    ├── init.py
    ├── print_tools.py
    └── __init__.py
```

## Usage Instructions

1. **Install Dependencies:** Ensure that the required dependencies for the project are installed in your Python
   environment. You can use the following command:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run Console Version:** Execute the following command to run the console version of the LR(0) parser:

   ```bash
   python run_lr0_console.py
   ```

   The console version will display information about the grammar, LR(0) items, DFA, action/goto tables, and the
   analysis process for a given symbol string.

3. **Run GUI Version:** Execute the following command to open the graphical user interface (GUI) version:

   ```bash
   python run_lr0_ui.py
   ```

   The GUI version allows interactive loading of grammars, visualization of DFA, and symbol string analysis.

4. **Example Grammars:** The `examples` directory contains example grammars for testing. Feel free to modify or add new
   grammars for testing purposes.

## Course Project Requirements

1. **Grammar Definition:** Define an LR(0) grammar using production rules.

2. **Canonical Item Set Family:** Provide the canonical item set family for LR(0) parsing, representing all states.

3. **State Relationships:** Describe the relationships between different states in the canonical item set family.

4. **LR(0) Parsing Table:** Construct the LR(0) parsing table, showcasing the parsing actions and state transitions for
   the grammar.

5. **Symbol String Analysis:** Given a symbol string, determine whether it is a valid sentence in the grammar and print
   the analysis process using the parsing table.

## Notes

- Ensure that project dependencies are installed.
- Check the console output and GUI interface for detailed parser information and results.
- For symbol string analysis, provide correct input for accurate analysis.