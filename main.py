import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

# main class
class MainWindow(QMainWindow):
    # constructor
    def __init__(self):
        super(MainWindow, self).__init__()

        # creating a QWebEngineView
        self.browser = QWebEngineView()
        # set default url
        self.browser.setUrl(QUrl('http://google.com'))
        # adding action when url get changed
        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadFinished.connect(self.update_title)
        # set this browser as central widget or main window
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # navigation tool bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # creating a action for back
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # creating a action for forward
        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # creating a action for reload
        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # creating a action for home
        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # adding a separator in the toolbar
        navbar.addSeparator()
        # add url box
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

    # method called by the home action
    def navigate_home(self):
        self.browser.setUrl(QUrl('http://google.com'))

    # method called by the line edit when return key is pressed
    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    # method for updating url
    def update_url(self, q):
        self.url_bar.setText(q.toString())

    # method for updating the title of the window
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle('{} - My Browser'.format(title))

if __name__ == '__main__':
    # creating a pyQt5 application
    app = QApplication(sys.argv)
    # setting name to the application
    QApplication.setApplicationName('My Browser')
    # creating a main window object
    window = MainWindow()
    app.exec_()
