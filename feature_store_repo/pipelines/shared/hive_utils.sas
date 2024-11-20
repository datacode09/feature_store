%macro hive_connect(config_path);
    %include "&config_path";
    libname hive hadoop server="&hive_server" schema="&hive_schema";
%mend hive_connect;

%macro hive_disconnect();
    libname hive clear;
%mend hive_disconnect;
