\echo 'Delete and recreate jobly db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE leagueOfTft;
CREATE DATABASE leagueOfTft;
\connect leagueOfTft

\i leagueOfTft-schema.sql
\i leagueOfTft-seed.sql

\echo 'Delete and recreate leagueOfTft_test db?'
\prompt 'Return for yes or control-C to cancel > ' foo

DROP DATABASE leagueOfTft_test;
CREATE DATABASE leagueOfTft_test;
\connect leagueOfTft_test

\i leagueOfTft-schema.sql