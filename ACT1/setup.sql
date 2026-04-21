-- Initialize TME_DB database
CREATE DATABASE IF NOT EXISTS TME_DB;

-- Initialize ACT1 schema
CREATE SCHEMA IF NOT EXISTS TME_DB.ACT1;

-- Create stages in ACT1
CREATE STAGE IF NOT EXISTS TME_DB.ACT1.ACT1_LORE
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'This stage documents the storyline behind what happened in ACT 1, with txt files.';

CREATE STAGE IF NOT EXISTS TME_DB.ACT1.ACT1_LORE_SSE
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'This stage documents the storyline behind what happened in ACT 1, with txt files. SSE version.';

CREATE STAGE IF NOT EXISTS TME_DB.ACT1.NAGOROFILES
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'After the Nagoro Battle, the Snowflakers uploaded their files about the Kinito Collective and why are they hunting down for the Onozawa children.';
