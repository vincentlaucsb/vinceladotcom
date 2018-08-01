from vinceladotcom import application

if __name__ == "__main__":
    from vinceladotcom.database import db_init
    db_init()

    application.run(host='0.0.0.0')