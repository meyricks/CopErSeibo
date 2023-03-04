""""
file: main.py
"""

import sys
import frontstuff
from frontstuff import Map

if __name__ == '__main__':
    app = frontstuff.QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 25px;
        }
    ''')

    map = Map()
    map.show()

    app.exec()