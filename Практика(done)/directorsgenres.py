from PyQt6.QtWidgets import (QDialog, QTableWidgetItem, QMessageBox)

from directors import Ui_Form as directorsDesign
from genres import Ui_Form as genresDesign


class Directors(QDialog, directorsDesign):
    def __init__(self, con):
        super().__init__()
        self.setupUi(self)
        self.con = con
        self.showDirectors()
        self.tableWidget.itemSelectionChanged.connect(self.showDetails)
        self.addButton.clicked.connect(self.addDirector)
        self.deleteButton.clicked.connect(self.deleteDirector)
        self.editButton.clicked.connect(self.editDirector)

    def showDirectors(self):
        result = self.con.execute('''
            SELECT *
            FROM directors;
        ''').fetchall()
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Имя'])
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem) if elem else '')
                )
        self.tableWidget.resizeColumnsToContents()

    def showDetails(self):
        row = self.tableWidget.currentItem().row()
        name = self.tableWidget.item(row, 1).text()
        self.nameEdit.setText(name)

    def addDirector(self):
        name = self.nameEdit.text()
        result = QMessageBox().question(
            self, 'Вы уверены?', f'Добавить режиссера {name}?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        with self.con:
            self.con.execute('''
                INSERT INTO directors(name)
                VALUES (?);
            ''', (name,))
        self.showDirectors()

    def deleteDirector(self):
        row = self.tableWidget.currentItem().row()
        director_id = self.tableWidget.item(row, 0).text()
        name = self.tableWidget.item(row, 1).text()
        result = QMessageBox().question(
            self, 'Вы уверены?',
            f'Удалить режиссера {name} (id={director_id})?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        with self.con:
            self.con.execute('''
                DELETE from directors
                WHERE id = (?);
            ''', (director_id,))
        self.showDirectors()

    def editDirector(self):
        row = self.tableWidget.currentItem().row()
        now_name = self.tableWidget.item(row, 1).text()
        director_id = self.tableWidget.item(row, 0).text()
        result = QMessageBox().question(
            self, 'Вы уверены?',
            f'Изменить жанр {now_name} (id={director_id})?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        name = self.nameEdit.text()
        with self.con:
            self.con.execute('''
                UPDATE directors
                SET name = ?
                WHERE id = ?;
            ''', (name, director_id))
        self.showDirectors()


class Genres(QDialog, genresDesign):
    def __init__(self, con):
        super().__init__()
        self.setupUi(self)
        self.con = con
        self.showGenres()
        self.tableWidget.itemSelectionChanged.connect(self.showDetails)
        self.addButton.clicked.connect(self.addGenre)
        self.deleteButton.clicked.connect(self.deleteGenre)
        self.editButton.clicked.connect(self.editGenre)

    def showGenres(self):
        result = self.con.execute('''
            SELECT *
            FROM genres;
        ''').fetchall()
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название'])
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem) if elem else '')
                )
        self.tableWidget.resizeColumnsToContents()

    def showDetails(self):
        row = self.tableWidget.currentItem().row()
        title = self.tableWidget.item(row, 1).text()
        self.titleEdit.setText(title)

    def addGenre(self):
        title = self.titleEdit.text()
        result = QMessageBox().question(
            self, 'Вы уверены?', f'Добавить жанр {title}?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        with self.con:
            self.con.execute('''
                INSERT INTO genres(title)
                VALUES (?);
            ''', (title,))
        self.showGenres()

    def deleteGenre(self):
        row = self.tableWidget.currentItem().row()
        genre_id = self.tableWidget.item(row, 0).text()
        title = self.tableWidget.item(row, 1).text()
        result = QMessageBox().question(
            self, 'Вы уверены?', f'Удалить жанр {title} (id={genre_id})?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        with self.con:
            self.con.execute('''
                DELETE from genres
                WHERE id = (?);
            ''', (genre_id,))
        self.showGenres()

    def editGenre(self):
        row = self.tableWidget.currentItem().row()
        now_title = self.tableWidget.item(row, 1).text()
        genre_id = self.tableWidget.item(row, 0).text()
        result = QMessageBox().question(
            self, 'Вы уверены?', f'Изменить жанр {now_title} (id={genre_id})?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return
        title = self.titleEdit.text()
        with self.con:
            self.con.execute('''
                UPDATE genres
                SET title = ?
                WHERE id = ?;
            ''', (title, genre_id))
        self.showGenres()
