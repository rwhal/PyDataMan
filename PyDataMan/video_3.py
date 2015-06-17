import sys
import io
import urllib.request

from PyQt5.QtWidgets import *



class Form(QDialog):
    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        
        date = self.getData()
        rates = sorted(self.rates.keys())
        dateLabel = QLabel(date)

        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(rates)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 100000000.00)
        self.fromSpinBox.setValue(1.00)

        self.toComboBox = QComboBox()
        self.toComboBox.addItems(rates)

        self.toLabel = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)
        
        self.setWindowTitle("Currency Converter")
        
        self.setUpSignals()
    
    def setUpSignals(self):
        self.fromComboBox.currentIndexChanged[int].connect(self.updateUi)
        self.toComboBox.currentIndexChanged[int].connect(self.updateUi)
        self.fromSpinBox.valueChanged[float].connect(self.updateUi)
        
    def updateUi(self):
        to = self.toComboBox.currentText()
        from_ = self.fromComboBox.currentText()
        
        amount = (self.rates[from_] / self.rates[to]) * self.fromSpinBox.value()
        self.toLabel.setText("{0:.2}".format(amount))
    
    def getData(self):
        self.rates = {}
        
        try:
            date = "Unknown"
            resp = urllib.request.urlopen("http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv")
            fh = io.StringIO(resp.read().decode())
            data = [line.rstrip() for line in fh]
            for line in data:
                line = line.rstrip()
                if not line or line.startswith(("#", "Closing")):
                    continue
                fields = line.split(",")
                if line.startswith("Date"):
                    date = fields[-1]
                else:
                    try:
                        value = float(fields[-1])
                        self.rates[fields[0]] = value
                    except:
                        pass
            return "Exchange rates date: {0}".format(date)

        except Exception as err:
            return "Failed to download:\n\t{0}".format(err)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
