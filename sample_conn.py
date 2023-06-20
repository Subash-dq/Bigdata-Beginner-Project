DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;
DROP TABLE IF TABLE admin;



create table application
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table asset
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table asset_schedule
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table attribute
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table attribute_metadata
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table attribute_metadata_tags
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table banner
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table base_measure
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table channels
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table connection
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table custom_field_group_user_setting
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table datatypes
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table dimension
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table drift_alert
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table drift_threshold
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table favourites
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table features
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table general
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table glossary
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table integrated_channels
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table issue_attachment
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table issue_comments
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table issue_watch
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table issues
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table issues_application
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table issues_domain
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table issues_users
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table measure
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table metrics
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table notification_logs
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table notifications_attachments
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table notifications_channel
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table notifications_priority
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table notifications_status
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table notifications_users
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table request_queue
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table rewuest_queue_detail
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));


create table roles_permission
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table scores
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table sub_tags
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table templates
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table terms
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table terms_approval
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table terms_category
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table theme
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table usage_queries
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table user_session_track
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table users
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table users_applications
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table users_domains
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table users_groups
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table users_user_permission
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table versions
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table versions_application
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table versions_domains
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table versions_history
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table versions_report_mapping
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table versions_stewards
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table widget
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));

create table work_log
( id int,
domain varchar(50),
credentials varchar(50),
organisation varchar(50),
default_connection_id varchar(50),
created_date varchar(50),
connectors varchar(50),
license_end_date varchar(50),
license_start_date varchar(50));


