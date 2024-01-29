import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QApplication, QTableWidgetItem,
                             QMessageBox, QListWidgetItem)
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
        self.con.execute("PRAGMA foreign_keys = 1")
        self.showMovies()
        self.showDirectors()
        self.showGenres()
        self.tableWidget.itemSelectionChanged.connect(self.showDetails)
        self.addButton.clicked.connect(self.addMovie)
        self.deleteButton.clicked.connect(self.deleteMovie)
        self.editButton.clicked.connect(self.editMovie)

    def showMovies(self):
        result = self.con.execute('''
            SELECT movies.id, title, year, duration, name
            FROM movies
            LEFT JOIN directors
            ON movies.director_id = directors.id
        ''').fetchall()
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Год', 'Длительность', 'Режиссер'])
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem) if elem else '')
                )
        self.tableWidget.resizeColumnsToContents()

    def showDirectors(self):
        result = self.con.execute('''
            SELECT *
            FROM directors
        ''').fetchall()
        self.directorsDict = {None: None}
        self.directorsDict.update({d[1]: d[0] for d in result})
        for director in self.directorsDict:
            self.directorComboBox.addItem(director)

    def showGenres(self):
        result = self.con.execute('''
            SELECT *
            FROM genres
        ''')
        self.genresDict = {g[1]: g[0] for g in result}
        for genre in self.genresDict:
            item = QListWidgetItem(genre)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.listWidget.addItem(item)

    def showDetails(self):
        row = self.tableWidget.currentItem().row()
        movie_id = self.tableWidget.item(row, 0).text()
        title = self.tableWidget.item(row, 1).text()
        year = self.tableWidget.item(row, 2).text() or 0
        duration = self.tableWidget.item(row, 3).text() or 0
        director = self.tableWidget.item(row, 4).text()
        self.titleEdit.setText(title)
        self.yearSpinBox.setValue(int(year))
        self.durationSpinBox.setValue(int(duration))
        self.directorComboBox.setCurrentText(director)
        result = self.con.execute('''
            SELECT title
            FROM genres
            JOIN movies_genres
            ON genre_id = id
            WHERE movie_id = ?
        ''', (movie_id,))
        genres = [genre[0] for genre in result]
        for i in range(len(self.listWidget)):
            item = self.listWidget.item(i)
            if item.text() in genres:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)

    def addMovie(self):
        title = self.titleEdit.text()
        result = QMessageBox().question(
            self, 'Вы уверены?', f'Добавить фильм {title}?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        year = self.yearSpinBox.value() or None
        duration = self.durationSpinBox.value() or None
        director = self.directorComboBox.currentText() or None
        director_id = self.directorsDict[director]
        with self.con:
            movie_id = self.con.execute('''
                INSERT INTO movies(title, year, duration, director_id)
                VALUES (?, ?, ?, ?);
            ''', (title, year, duration, director_id)).lastrowid
        genres = []
        for i in range(len(self.listWidget)):
            item = self.listWidget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                genres.append((movie_id, self.genresDict[item.text()]))
        with self.con:
            self.con.executemany('''
                INSERT INTO movies_genres
                VALUES (?, ?);
            ''', genres)
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
        director = self.directorComboBox.currentText() or None
        director_id = self.directorsDict[director]
        genres = []
        for i in range(len(self.listWidget)):
            item = self.listWidget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                genres.append((movie_id, self.genresDict[item.text()]))
        with self.con:
            self.con.execute('''
                UPDATE movies
                SET title = ?, year = ?, duration = ?, director_id = ?
                WHERE id = ?
            ''', (title, year, duration, director_id, movie_id))
            self.con.execute('''
                DELETE FROM movies_genres
                WHERE movie_id = ?
            ''', (movie_id,))
            self.con.executemany('''
                INSERT INTO movies_genres
                VALUES (?, ?);
            ''', genres)
        self.showMovies()
        self.showDetails()


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
