import os.path
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

# main class
class MainWindow(QMainWindow):
    # constructor
    def __init__(self):
        super(MainWindow, self).__init__()

        # creating a QWebEngineView
        # self.browser = QWebEngineView()
        # # set default url
        # self.browser.setUrl(QUrl('http://google.com'))
        # # adding action when url get changed
        # self.browser.urlChanged.connect(self.update_url)
        # self.browser.loadFinished.connect(self.update_title)
        # # set this browser as central widget or main window
        # self.setWindowIcon(QIcon('image/icon - 01.png/'))
        # self.setCentralWidget(self.browser)
        # self.showMaximized()

        self.tab = QTabWidget()
        self.tab.setDocumentMode(True)
        self.tab.setTabsClosable(True)
        self.setCentralWidget(self.tab)
        self.showMaximized()

        self.tab.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tab.tabCloseRequested.connect(self.close_tab)
        self.tab.currentChanged.connect(self.current_tab_changed)


        # navigation tool bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # creating a action for back
        back_btn = QAction('Back', self)
        back_btn.setStatusTip('Back to previous page')
        back_btn.triggered.connect(lambda: self.tab.currentWidget().back())
        navbar.addAction(back_btn)

        # creating a action for forward
        forward_btn = QAction('Forward', self)
        forward_btn.setStatusTip('Forward to next page')
        forward_btn.triggered.connect(lambda: self.tab.currentWidget().forward())
        navbar.addAction(forward_btn)

        # creating a action for reload
        reload_btn = QAction('Reload', self)
        reload_btn.setStatusTip('Reload')
        reload_btn.triggered.connect(lambda: self.tab.currentWidget().reload())
        navbar.addAction(reload_btn)

        # creating a action for home
        home_btn = QAction('Home', self)
        home_btn.setStatusTip('Go home')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # adding a separator in the toolbar
        navbar.addSeparator()
        # add url box
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        navbar.addSeparator()


        # add icon
        self.setWindowIcon(QIcon('image/icon - 01.png/'))
        # set default Homre page
        self.open_new_tab(QUrl('http://google.com'),'Home')


        self.show()

    def open_new_tab(self,qurl=None,label='New Tab'):
        if qurl is None:
            qurl = QUrl('http://google.com')

        # creating a QWebEngineView & set url
        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tab.addTab(browser,label)
        self.tab.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl,browser = browser: self.update_url(qurl,browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tab.setTabText(i,browser.page().title()))



    def tab_open_doubleclick(self,i):
        if i == -1:
            self.open_new_tab()
    def close_tab(self,i):
        if self.tab.count() < 2:
            return
        self.tab.removeTab(i)

    # method called by the home action
    def navigate_home(self):
        self.tab.currentWidget().setUrl(QUrl('http://google.com'))

    # method called by the line edit when return key is pressed
    def navigate_to_url(self):
        url = QUrl(self.url_bar.text())
        if url.scheme() == '':
            url.setScheme('http')
        self.tab.currentWidget().setUrl(url)
        self.tab.currentChanged.connect(self.current_tab_changed)

    def current_tab_changed(self, i):
        qurl = self.tab.currentWidget().url()
        self.update_url(qurl,self.tab.currentWidget())
        self.update_title(self.tab.currentWidget())

    # method for updating url
    def update_url(self, q, browser=None):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    # method for updating the title of the window
    def update_title(self, browser):
        if browser != self.tab.currentWidget():
            return

        title = self.tab.currentWidget().page().title()
        self.setWindowTitle(title)

if __name__ == '__main__':
    # creating a pyQt5 application
    app = QApplication(sys.argv)
    # setting name to the application
    QApplication.setApplicationName('My Browser')
    # creating a main window object
    window = MainWindow()
    app.exec_()
