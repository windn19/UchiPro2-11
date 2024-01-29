import sqlite3
import sys

from PyQt6.QtWidgets import (QWidget, QApplication, QTableWidgetItem,
                             QMessageBox)
from movies import Ui_Form

DATABASE_NAME = 'movies_db.db'


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def connectDB():
    try:
        return sqlite3.connect(f'file:{DATABASE_NAME}?mode=rw', uri=True)
    except sqlite3.DatabaseError as e:
        print(f'{e.__class__.__name__}: {e}')
        sys.exit(-1)


class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = connectDB()
        self.showMovies()
        self.showDirectors()
        self.tableWidget.itemSelectionChanged.connect(self.showDetails)
        self.addButton.clicked.connect(self.addMovie)
        self.deleteButton.clicked.connect(self.deleteMovie)
        self.editButton.clicked.connect(self.editMovie)

    def showMovies(self):
        result = self.con.execute('''
            SELECT *
            FROM movies;
        ''').fetchall()
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Год', 'Длительность', 'ID режиссера'])
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(
                    str(elem) if elem else ''))
        self.tableWidget.resizeColumnsToContents()

    def showDirectors(self):
        result = self.con.execute('''
            SELECT *
            FROM directors;
        ''').fetchall()
        self.directorComboBox.addItems(
            [None] + [row[1] for row in result])

    def showDetails(self):
        row = self.tableWidget.currentItem().row()
        title = self.tableWidget.item(row, 1).text()
        year = self.tableWidget.item(row, 2).text() or 0
        duration = self.tableWidget.item(row, 3).text() or 0
        director_id = self.tableWidget.item(row, 4).text()
        self.titleEdit.setText(title)
        self.yearSpinBox.setValue(int(year) or 0)
        self.durationSpinBox.setValue(int(duration) or 0)
        result = self.con.execute('''
            SELECT name
            FROM directors
            WHERE id = ?;
        ''', (director_id,)).fetchone()
        if result:
            self.directorComboBox.setCurrentText(result[0])
        else:
            self.directorComboBox.setCurrentText('')

    def addMovie(self):
        title = self.titleEdit.text()
        result = QMessageBox().question(
            self, 'Вы уверены?', f'Добавить фильм {title}?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        year = self.yearSpinBox.value() or None
        duration = self.durationSpinBox.value() or None
        director = self.directorComboBox.currentText()
        result = self.con.execute('''
            SELECT id
            FROM directors
            WHERE name = ?;
        ''', (director,)).fetchone()
        if result:
            director_id = result[0]
        else:
            director_id = None
        with self.con:
            self.con.execute('''
                INSERT INTO movies(title, year, duration, director_id)
                VALUES (?, ?, ?, ?);
            ''', (title, year, duration, director_id))
        self.showMovies()

    def deleteMovie(self):
        row = self.tableWidget.currentItem().row()
        movie_id = self.tableWidget.item(row, 0).text()
        title = self.tableWidget.item(row, 1).text()
        result = QMessageBox().question(
            self, 'Вы уверены?', f'Удалить фильм {title} (id={movie_id})?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        with self.con:
            self.con.execute('''
                DELETE from movies
                WHERE id = (?);
            ''', (movie_id,))
        self.showMovies()

    def editMovie(self):
        row = self.tableWidget.currentItem().row()
        now_title = self.tableWidget.item(row, 1).text()
        movie_id = self.tableWidget.item(row, 0).text()
        result = QMessageBox().question(
            self, 'Вы уверены?', f'Изменить фильм {now_title} (id={movie_id})?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        title = self.titleEdit.text()
        year = self.yearSpinBox.value() or None
        duration = self.durationSpinBox.value() or None
        director = self.directorComboBox.currentText()
        result = self.con.execute('''
            SELECT id
            FROM directors
            WHERE name = ?;
        ''', (director,)).fetchone()
        if result:
            director_id = result[0]
        else:
            director_id = None
        with self.con:
            self.con.execute('''
                UPDATE movies
                SET title = ?, year = ?, duration = ?, director_id = ?
                WHERE id = ?;
            ''', (title, year, duration, director_id, movie_id))
        self.showMovies()


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
