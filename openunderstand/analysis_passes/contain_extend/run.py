import subprocess
from pathlib import Path

import db.api
import db.fill


def run():
    ound_exec = Path('C:/Users/babak/Desktop/source/OpenUnderstand-master/openunderstand').resolve().as_posix()
    prj_dir = Path('C:/Users/babak/Desktop/source/OpenUnderstand-master/openunderstand').resolve().as_posix()
    db_path = Path('C:/Users/babak/Desktop/source/OpenUnderstand-master/openunderstand').resolve().as_posix()
    refs = ['Java Contain', 'Java Containin', 'Java Extend Couple', 'Java Extend Coupleby']

    db.api.create_db(db_path, project_dir=prj_dir)
    db.fill.main()

    subprocess.call([ound_exec, prj_dir, db_path] + refs)


if __name__ == '__main__':
    run()
