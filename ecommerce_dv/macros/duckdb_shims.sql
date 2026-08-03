{% macro duckdb__get_escape_characters() %}
    {{ return(('"', '"')) }}
{% endmacro %}

{% macro duckdb__cast_date(column_str, as_string=false, alias=none) %}
    {%- if as_string -%}
        CAST('{{ column_str }}' AS DATE)
    {%- else -%}
        CAST({{ column_str }} AS DATE)
    {%- endif -%}
    {%- if alias %} AS {{ alias }} {%- endif %}
{% endmacro %}

{% macro duckdb__cast_datetime(column_str, as_string=false, alias=none) %}
    {%- if as_string -%}
        CAST('{{ column_str }}' AS TIMESTAMP)
    {%- else -%}
        CAST({{ column_str }} AS TIMESTAMP)
    {%- endif -%}
    {%- if alias %} AS {{ alias }} {%- endif %}
{% endmacro %}

{% macro duckdb__type_binary(for_dbt_compare=false) %}
    {{ return('VARCHAR') }}
{% endmacro %}