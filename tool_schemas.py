"""Shared tool schemas reused across chapters 4 and 5."""

get_current_datetime_schema = {
    "name": "get_current_datetime",
    "description": "Return the current date and time formatted according to the specified format string. Uses Python's strftime format codes. The default format returns the complete timestamp in ISO-like form (YYYY-MM-DD HH:MM:SS).",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "A string specifying the format of the returned datetime using Python's strftime codes. For example, '%Y-%m-%d' returns just the date, '%H:%M:%S' returns just the time, '%B %d, %Y' returns a date like 'May 07, 2025'. Default: '%Y-%m-%d %H:%M:%S'.",
                "default": "%Y-%m-%d %H:%M:%S",
            },
        },
        "required": [],
    },
}

add_duration_to_datetime_schema = {
    "name": "add_duration_to_datetime",
    "description": "Add a specified duration to a datetime string and return the resulting datetime formatted as 'Weekday, Month Day, Year HH:MM:SS AM/PM'. Supports seconds, minutes, hours, days, weeks, months, and years, with special handling for month and year calculations to account for varying month lengths and leap years.",
    "input_schema": {
        "type": "object",
        "properties": {
            "datetime_str": {"type": "string", "description": "The input datetime string, formatted per input_format."},
            "duration": {
                "type": "number",
                "description": "The amount of time to add. Can be positive (for future dates) or negative (for past dates). Defaults to 0.",
            },
            "unit": {
                "type": "string",
                "description": "The unit of time for the duration. Must be one of: 'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', or 'years'. Defaults to 'days'.",
            },
            "input_format": {
                "type": "string",
                "description": "The format string for parsing the input datetime_str, using Python's strptime format codes. For example, '%Y-%m-%d' for ISO format dates. Defaults to '%Y-%m-%d'.",
            },
        },
        "required": ["datetime_str"],
    },
}

set_reminder_schema = {
    "name": "set_reminder",
    "description": "Create a timed reminder that will notify the user at the specified time with the provided content. The reminder system stores the content and timestamp, then triggers a notification through the user's preferred channels (mobile alerts, email, etc.) when the time arrives. Reminders are persisted across restarts, so this is suitable for time-sensitive events such as meetings, tasks, medication, or any time-bound activity.",
    "input_schema": {
        "type": "object",
        "properties": {
            "content": {"type": "string", "description": "The message text displayed in the reminder notification."},
            "timestamp": {
                "type": "string",
                "description": "The exact date and time when the reminder should fire, formatted as an ISO 8601 timestamp (YYYY-MM-DDTHH:MM:SS) or a Unix timestamp. The system handles all timezone processing internally.",
            },
        },
        "required": ["content", "timestamp"],
    },
}

# db_query_schema has no handler and no real demo: it is token filler for `6-features/5_prompt_caching`,
# where the schema stack must cross the 1024-token minimum for ephemeral cache hits.
db_query_schema = {
    "name": "db_query",
    "description": "Execute SQL queries against a SQLite database and return results. Supports SELECT, INSERT, UPDATE, DELETE, and other SQL statements. For SELECT queries, returns the results as structured data. For other query types, returns metadata about the operation (number of rows affected). Complex queries are supported including joins, aggregations, subqueries, and transactions. Results can be returned as dict, list, or ASCII table.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The SQL query to execute. Can be any valid SQLite SQL statement.",
            },
            "database_path": {
                "type": "string",
                "description": "Path to the SQLite database file. If not provided, uses the default database.",
            },
            "params": {
                "type": "object",
                "description": "Named parameters to bind for parameterized queries (e.g., {'user_id': 123} for a query containing ':user_id'). Strongly recommended to prevent SQL injection.",
            },
            "result_format": {
                "type": "string",
                "description": "Format of the results. One of 'dict' (list of dicts), 'list' (list of lists with headers in first row), or 'table' (ASCII table).",
                "enum": ["dict", "list", "table"],
                "default": "dict",
            },
            "max_rows": {
                "type": "integer",
                "description": "Maximum rows to return for SELECT queries. 0 means no limit. Default: 1000.",
                "default": 1000,
            },
            "transaction": {
                "type": "boolean",
                "description": "Wrap the query in a BEGIN/COMMIT transaction. Defaults to false for SELECT, true for others.",
                "default": False,
            },
        },
        "required": ["query"],
    },
}
