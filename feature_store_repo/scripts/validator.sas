%macro validate_data(data);
    proc sql;
        select count(*) as missing_values
        from &data
        where customer_id is null;
    quit;
%mend validate_data;