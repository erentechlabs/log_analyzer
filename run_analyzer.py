
from app.database import SessionLocal
from app.services import log_parser, analysis_engine, notification
from app import crud

# Log files to process and which parser function to use
LOG_FILES_TO_PROCESS = {
    "logs/auth.log": log_parser.parse_ssh_log,
    # In the future, when you add an Nginx parser, add it here:
    # "logs/nginx_access.log": log_parser.parse_nginx_log
}


def run_analysis():
    print("Starting log analysis...")
    db = SessionLocal()
    try:
        for file_path, parser_function in LOG_FILES_TO_PROCESS.items():
            print(f"Processing file '{file_path}'...")
            with open(file_path, 'r') as f:
                for line in f:
                    parsed_log = parser_function(line)

                    # If the line was successfully parsed
                    if parsed_log:
                        # 1. Save the log to the database
                        crud.create_log_entry(db, parsed_log)

                        # 2. Run the analysis engine
                        # For now, we only perform brute-force analysis
                        if parsed_log['type'] == 'ssh_failed_login':
                            alert = analysis_engine.analyze_for_brute_force(db, parsed_log)

                            # 3. If an alert was created, send a notification
                            if alert:
                                print(f"ALERT CREATED: {alert.reason} - IP: {alert.ip_address}")
                                # If your Email/SMS settings are correct, you can enable the line below
                                # notification.send_email_alert(alert)

        print("Analysis completed.")
    finally:
        db.close()
        print("Database connection closed.")


if __name__ == "__main__":
    run_analysis()