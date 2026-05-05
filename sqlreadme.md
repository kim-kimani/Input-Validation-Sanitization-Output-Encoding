# SQL Execution Modes Breakdown

Here is a clear breakdown of the differences between the three execution modes in the sandbox and how they handle the text you type into the input field:

### 1. Run Vulnerable Query (String Formatting)
In this mode, the server takes whatever you type and literally pastes it directly into the middle of a pre-written SQL template using string formatting.
- **Backend Code:** `f"SELECT ... WHERE name = '{your_input}'"`
- **How it behaves:** Because your input becomes part of the SQL logic itself, you can type characters like `'` or `;` to "break out" of the intended query. 
- **Example:** If you type `' OR '1'='1`, the server runs `SELECT ... WHERE name = '' OR '1'='1'`, treating your input as executable SQL logic rather than just a name to search for. This is classic SQL Injection.

### 2. Run Safe Query (Parameterized Queries)
This is the industry standard for defending against SQL Injection. Instead of pasting your input directly into the query, the server uses placeholders (`%s` or `?`) and sends the data to the database separately from the SQL command.
- **Backend Code:** `cursor.execute("SELECT ... WHERE name = %s", [your_input])`
- **How it behaves:** The database engine is told, "Run this exact SQL logic, and treat this separate piece of data strictly as a string literal." 
- **Example:** If you type `' OR '1'='1`, the database looks for a literal employee whose name is exactly `"' OR '1'='1"`. It completely ignores any SQL syntax hidden inside your input. It prevents injection entirely.

### 3. Run Raw SQL (Direct Execution)
This mode acts like a direct database client (like DBeaver or phpMyAdmin). It doesn't wrap your input in a `SELECT` statement at all; it takes exactly what you typed and executes it as the raw, primary command.
- **Backend Code:** `cursor.execute(your_input)`
- **How it behaves:** This is not an "injection" attack because there is no pre-existing query to manipulate. You are directly commanding the database.
- **Example:** You simply type `SELECT * FROM sandbox_employee;` and it runs exactly that. If you type just an employee's name like `Alice Smith`, it will throw a database syntax error because `Alice Smith` is not a valid SQL command.
