import sys
import subprocess
import os

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QPlainTextEdit,
)


class SimulationWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("OpenModelica Simulation Window")
        self.setMinimumWidth(450)
        self._build_ui()

    def _select_executable(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Executable", "", "Executable Files (*.exe);;All Files (*)"
        )
        if file_path:
            self.program_input.setText(file_path)

    def _get_valid_times(self):

        try:
            start = int(self.start_input.text())
            stop = int(self.stop_input.text())
        except ValueError:
            QMessageBox.warning(
                self, "Invalid Input", "Start and stop time must be whole numbers."
            )
            return None

        if not (0 <= start < stop < 5):
            QMessageBox.warning(
                self,
                "Invalid Range",
                "Times must satisfy: 0 <= start time < stop time < 5",
            )
            return None

        return start, stop

    def _run_simulation(self) -> None:
        exe_path = self.program_input.text()
        if not exe_path:
            QMessageBox.warning(
                self, "Missing Application", "Please select an executable first."
            )
            return

        times = self._get_valid_times()
        if times is None:
            return  # error already shown by _get_valid_times

        start, stop = times
        command = [exe_path, f"-startTime={start}", f"-stopTime={stop}"]
        exe_folder = os.path.dirname(exe_path)

        try:
            result = subprocess.run(
                command, capture_output=True, text=True, cwd=exe_folder
            )
        except FileNotFoundError:
            QMessageBox.critical(
                self, "Error", "Could not find or run the selected executable."
            )
            return

        combined_output = result.stdout + result.stderr
        self.output_box.setPlainText(combined_output)

        if result.returncode == 0:
            QMessageBox.information(
                self, "Success", "Simulation completed successfully."
            )
        else:
            QMessageBox.critical(
                self,
                "Simulation Failed",
                "The simulation exited with an error. See the output box for details.",
            )

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout()

        exe_row = QHBoxLayout()
        self.program_input = QLineEdit()
        self.program_input.setPlaceholderText("Select the executable to run...")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self._select_executable)
        exe_row.addWidget(QLabel("Application"))
        exe_row.addWidget(self.program_input)
        exe_row.addWidget(browse_button)

        start_row = QHBoxLayout()
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("e.g. 0")
        start_row.addWidget(QLabel("Start Time:"))
        start_row.addWidget(self.start_input)

        stop_row = QHBoxLayout()
        self.stop_input = QLineEdit()
        self.stop_input.setPlaceholderText("e.g. 2")
        stop_row.addWidget(QLabel("Stop Time:"))
        stop_row.addWidget(self.stop_input)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self._run_simulation)

        main_layout.addLayout(exe_row)
        main_layout.addLayout(start_row)
        main_layout.addLayout(stop_row)
        main_layout.addWidget(self.run_button)

        self.output_box = QPlainTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Simulation output will appear here...")
        main_layout.addWidget(QLabel("Output:"))
        main_layout.addWidget(self.output_box)

        self.setLayout(main_layout)


def main() -> None:
    app = QApplication(sys.argv)
    window = SimulationWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
