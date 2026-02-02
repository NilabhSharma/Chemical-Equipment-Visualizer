import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QGroupBox,
    QDialog, QLineEdit, QScrollArea, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


API_UPLOAD = "http://127.0.0.1:8000/api/upload/"
API_HISTORY = "http://127.0.0.1:8000/api/history/"

class MainWindow(QMainWindow):
    def add_shadow(self, widget, blur=25, x=0, y=4, alpha=60):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setOffset(x, y)
        shadow.setColor(QColor(0, 0, 0, alpha))
        widget.setGraphicsEffect(shadow)

    def __init__(self, username, password):
        super().__init__()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ICON_PATH = os.path.join(BASE_DIR, "app_icon.ico")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.auth = HTTPBasicAuth(username, password)

        self.setWindowTitle("Chemical Equipment Visualizer")
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        header_bar = QWidget()
        header_bar.setStyleSheet("""
        background-color: #1f2937;
        border-radius: 10px;
        """)

        header_layout = QHBoxLayout(header_bar)
        header_layout.setContentsMargins(20, 30, 20, 30)
        self.add_shadow(header_bar, blur=30, y=6, alpha=90)

        title = QLabel("Chemical Equipment Visualizer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
        color: white;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 0.5px;
        """)
        logout_btn = QPushButton("Logout")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.logout)

        logout_btn.setStyleSheet("""
        QPushButton {
            background:#dc2626;
            color:white;
            padding:8px 16px;
            border-radius:8px;
            font-weight:600;
        }
        QPushButton:hover { background:#b91c1c; }
        QPushButton:pressed { background:#991b1b; }
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(logout_btn)

        title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        main_layout.addWidget(header_bar)


        grid = QGridLayout()
        grid.setSpacing(30)
        grid.setContentsMargins(24, 40, 24, 24)
        
        main_layout.addLayout(grid)

        self.setStyleSheet("""
        QMainWindow { background:#eef2f7; }

        QGroupBox {
            background:white;
            border:1px solid #d0d7e2;
            border-radius:14px;
            margin-top:28px;
            padding:22px;
            font-size:18px;
            font-weight:700;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left:18px;
            top:0px;
            padding:6px 14px;
            background:#eef2f7;
            border-radius:8px;
        }

        QPushButton {
            
            background:#2563eb;
            color:white;
            border-radius:8px;
            padding:18px 16px;
            font-size:16px;
            font-weight:700;
        }

        QPushButton:hover { background:#1d4ed8; }
        QPushButton:pressed { background:#1e40af; }
        """)

        upload_box = QGroupBox("Upload Dataset")
        ul = QVBoxLayout()
        ul.setContentsMargins(18, 30, 18, 18)

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        self.add_shadow(self.upload_btn, blur=15, y=2, alpha=40)


        self.upload_status = QLabel("No file uploaded")

        ul.addWidget(self.upload_btn)
        ul.addWidget(self.upload_status)
        upload_box.setLayout(ul)
        self.add_shadow(upload_box)

        grid.addWidget(upload_box, 0, 0)

        history_box = QGroupBox("History")
        hl = QVBoxLayout()

        self.history_scroll = QScrollArea()
        self.history_scroll.setWidgetResizable(True)

        self.history_content = QWidget()
        self.history_container = QVBoxLayout(self.history_content)
        self.history_container.setSpacing(8)

        self.history_scroll.setWidget(self.history_content)
        hl.addWidget(self.history_scroll)

        history_box.setLayout(hl)
        self.add_shadow(history_box)

        grid.addWidget(history_box, 0, 1)

        summary_box = QGroupBox("Summary")
        sl = QVBoxLayout()
        sl.setContentsMargins(18, 30, 18, 18)

        self.summary_label = QLabel("No dataset loaded")
        self.summary_label.setWordWrap(True)

        self.pdf_btn = QPushButton("Download PDF Report")
        self.pdf_btn.clicked.connect(self.download_latest_pdf)
        self.add_shadow(self.pdf_btn, blur=15, y=2, alpha=40)

        sl.addWidget(self.summary_label)
        sl.addWidget(self.pdf_btn)
        summary_box.setLayout(sl)
        self.add_shadow(summary_box)

        grid.addWidget(summary_box, 1, 0)

        chart_box = QGroupBox("Equipment Distribution")
        cl = QVBoxLayout()
        cl.setContentsMargins(18, 30, 18, 18)

        self.figure = Figure(figsize=(5,4))
        self.canvas = FigureCanvas(self.figure)

        cl.addWidget(self.canvas)
        chart_box.setLayout(cl)
        self.add_shadow(chart_box)

        grid.addWidget(chart_box, 1, 1)

        grid.setColumnStretch(0,1)
        grid.setColumnStretch(1,1)

        self.load_history()

    def update_summary_and_chart(self, summary):

    
        total = summary["total_equipment"]
        a = summary["averages"]

        text = (
            f"Total Equipment: {total}\n\n"
            f"Avg Flowrate: {a['flowrate']:.2f}\n"
            f"Avg Pressure: {a['pressure']:.2f}\n"
            f"Avg Temperature: {a['temperature']:.2f}"
        )

        self.summary_label.setText(text)

        chart = summary["type_distribution"]["chart"]
        labels = chart["labels"]
        values = chart["values"]

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.bar(labels, values)
        ax.set_title("Equipment Type Distribution")

        self.canvas.draw()


    def load_history(self):

        r = requests.get(API_HISTORY, auth=self.auth)
        datasets = r.json()

        while self.history_container.count():
            item = self.history_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for ds in datasets[:5]:

            row = QWidget()
            rl = QHBoxLayout(row)

            name = ds["filename"]
            summary = ds["summary"]
            did = ds["id"]

            label = QLabel(name)

            view_btn = QPushButton("View")
            self.add_shadow(view_btn, blur=15, y=2, alpha=40)

            pdf_btn = QPushButton("PDF")
            self.add_shadow(pdf_btn, blur=15, y=2, alpha=40)

            view_btn.clicked.connect(
                lambda _, s=summary: self.update_summary_and_chart(s)
            )

            pdf_btn.clicked.connect(
                lambda _, i=did: self.download_pdf_by_id(i)
            )

            rl.addWidget(label)
            rl.addStretch()
            rl.addWidget(view_btn)
            rl.addWidget(pdf_btn)

            self.history_container.addWidget(row)

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            filename = file_path.split("/")[-1].split("\\")[-1]

            with open(file_path, "rb") as f:
                response = requests.post(
                    API_UPLOAD,
                    files={"file": f},
                    auth=self.auth
                )

            if response.status_code not in (200, 201):
                raise Exception(f"Upload failed ({response.status_code})")

            data = response.json()
            self.upload_status.setText(f"✅ Uploaded: {filename}")
            self.upload_status.setStyleSheet("color: #16a34a; font-weight: 600;")

            if "summary" in data:
                self.update_summary_and_chart(data["summary"])

            self.load_history()

            self.statusBar().showMessage(f"Uploaded {filename}")

        except Exception as e:
            QMessageBox.critical(self, "Upload Error", str(e))

    def download_latest_pdf(self):
        r = requests.get(API_HISTORY, auth=self.auth)
        self.download_pdf_by_id(r.json()[0]["id"])

    def download_pdf_by_id(self, did):

        r = requests.get(
            f"http://127.0.0.1:8000/api/report/{did}/",
            auth=self.auth
        )

        path,_ = QFileDialog.getSaveFileName(self,"Save PDF","report.pdf")
        if path:
            open(path,"wb").write(r.content)
    def logout(self):
        self.close()

        login = LoginDialog()

        while True:
            if login.exec_() == QDialog.Accepted:

                new_window = MainWindow(login.username, login.password)
                new_window.show()
                new_window.showMaximized()
                break

            else:
                QApplication.quit()
                break

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setFixedSize(320, 180)

        layout = QVBoxLayout(self)

        self.user_edit = QLineEdit()
        self.user_edit.setPlaceholderText("Username")

        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText("Password")
        self.pass_edit.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")

        layout.addWidget(QLabel("Enter credentials"))
        layout.addWidget(self.user_edit)
        layout.addWidget(self.pass_edit)
        layout.addWidget(self.login_btn)
        
        self.login_btn.clicked.connect(self.try_login)
        self.pass_edit.returnPressed.connect(self.try_login)    
    def try_login(self):
        username = self.user_edit.text().strip()
        password = self.pass_edit.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Enter username and password")
            return

        try:
            r = requests.get(
                "http://127.0.0.1:8000/api/history/",
                auth=HTTPBasicAuth(username, password),
                timeout=4
            )

            if r.status_code == 200:
                self.username = username
                self.password = password
                self.accept()  

            elif r.status_code == 401:
                QMessageBox.critical(self, "Login Failed", "Invalid credentials")

            else:
                QMessageBox.warning(self, "Server Error", f"Status: {r.status_code}")

        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))

def main():
    app = QApplication(sys.argv)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ICON_PATH = os.path.join(BASE_DIR, "app_icon.ico")
    app.setWindowIcon(QIcon(ICON_PATH))
    app.setStyle("Fusion")

    font = app.font()
    font.setPointSize(14)
    app.setFont(font)

    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        window = MainWindow(login.username, login.password)
        window.show()
        window.showMaximized()
        window.setWindowIcon(QIcon(ICON_PATH))
        sys.exit(app.exec_())
    else:
        sys.exit()


if __name__ == "__main__":
    main()
#background:#2563eb;