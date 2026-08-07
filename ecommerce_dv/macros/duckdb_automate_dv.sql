-- Escape Characters
{%- macro duckdb__get_escape_characters() -%}
    {%- do return(['"', '"']) -%}
{%- endmacro -%}

{%- macro default__get_escape_characters() -%}
    {%- do return(['"', '"']) -%}
{%- endmacro -%}

-- Binary Hashing Type
{%- macro duckdb__type_binary(for_dbt_compare=false) -%}
    {%- do return('VARCHAR') -%}
{%- endmacro -%}

{%- macro default__type_binary(for_dbt_compare=false) -%}
    {%- do return('VARCHAR') -%}
{%- endmacro -%}

-- Datetime Casting
{%- macro duckdb__cast_datetime(column_str, as_string=false, date_format=none, timestamp_format=none) -%}
    {%- if as_string -%}
        CAST({{ column_str }} AS VARCHAR)
    {%- else -%}
        CAST({{ column_str }} AS TIMESTAMP)
    {%- endif -%}
{%- endmacro -%}

{%- macro default__cast_datetime(column_str, as_string=false, date_format=none, timestamp_format=none) -%}
    {%- if as_string -%}
        CAST({{ column_str }} AS VARCHAR)
    {%- else -%}
        CAST({{ column_str }} AS TIMESTAMP)
    {%- endif -%}
{%- endmacro -%}

-- Date Casting
{%- macro duckdb__cast_date(column_str, as_string=false, date_format=none) -%}
    {%- if as_string -%}
        CAST({{ column_str }} AS VARCHAR)
    {%- else -%}
        CAST({{ column_str }} AS DATE)
    {%- endif -%}
{%- endmacro -%}

{%- macro default__cast_date(column_str, as_string=false, date_format=none) -%}
    {%- if as_string -%}
        CAST({{ column_str }} AS VARCHAR)
    {%- else -%}
        CAST({{ column_str }} AS DATE)
    {%- endif -%}
{%- endmacro -%}