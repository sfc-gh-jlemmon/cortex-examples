USE ROLE SYSADMIN;
CREATE DATABASE GIT;
CREATE SCHEMA GIT.GIT_UTILS;

-- This technically isn't necessary for a public repo, but including for completeness
CREATE OR REPLACE SECRET git_secret
  TYPE = password
  USERNAME = 'sfc-gh-user'
  PASSWORD = 'token_goes_here';

CREATE OR REPLACE API INTEGRATION git_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/sfc-gh-user')
  -- ALLOWED_AUTHENTICATION_SECRETS = (git_secret)
  ENABLED = TRUE;

USE ROLE SECURITYADMIN;
CREATE ROLE git_admin;
GRANT ROLE git_admin TO ROLE ACCOUNTADMIN;

GRANT USAGE ON DATABASE GIT TO ROLE git_admin;
GRANT ALL ON ALL SCHEMAS IN DATABASE git TO ROLE git_admin;
GRANT CREATE GIT REPOSITORY ON SCHEMA GIT.GIT_UTILS TO ROLE git_admin;

USE ROLE ACCOUNTADMIN;
GRANT USAGE ON WAREHOUSE compute_wh TO ROLE git_admin;


USE ROLE git_admin;
USE DATABASE GIT;
USE SCHEMA GIT_UTILS;

-- Create the repo, using a simple Cortex example
CREATE OR REPLACE GIT REPOSITORY user_streamlit
  API_INTEGRATION = git_api_integration
  -- GIT_CREDENTIALS = git_secret
  ORIGIN = 'https://github.com/sfc-gh-jlemmon/cortex-examples.git';
  
ALTER GIT REPOSITORY user_streamlit FETCH;

SHOW GIT BRANCHES in user_streamlit;
LS @user_streamlit/branches/main/sis-cortex;


-- CREATE A STREAMLIT!
USE ROLE GIT_ADMIN;
USE DATABASE GIT;
USE SCHEMA GIT.GIT_UTILS;

-- NOTE:  The name you give it is what shows up in the UI
CREATE STREAMLIT Cortex_Functions
    ROOT_LOCATION = '@user_streamlit/branches/main/sis-cortex'
    MAIN_FILE = '/cortex-sis.py'
    QUERY_WAREHOUSE = COMPUTE_WH;


-- Grant access to other roles (doc_admin is an example`)
GRANT USAGE ON STREAMLIT Cortex_Functions TO ROLE doc_admin;


USE ROLE SECURITYADMIN;
GRANT USAGE ON DATABASE GIT TO ROLE doc_admin;
GRANT USAGE ON SCHEMA GIT.GIT_UTILS TO ROLE doc_admin;
GRANT READ ON GIT REPOSITORY GIT.GIT_UTILS.USER_STREAMLIT TO ROLE doc_admin;


  
  