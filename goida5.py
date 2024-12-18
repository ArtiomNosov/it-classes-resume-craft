from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog,
    QMessageBox, QStackedWidget, QComboBox, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from langchain.chains import LLMChain
from langchain_community.llms import YandexGPT
from langchain_core.prompts import PromptTemplate
from fpdf import FPDF
import json
import os

# Настройка Yandex GPT
YANDEX_API_KEY = "AQVNwMtQuYCxw7qWvucFkUmdQX-mx9SnqJgLGu6Z"
YANDEX_FOLDER_ID = "b1gq9a2kgl1lgavlghge"
llm = YandexGPT(api_key=YANDEX_API_KEY, folder_id=YANDEX_FOLDER_ID)
template = "{question}"
prompt = PromptTemplate.from_template(template)

llm_chain = prompt | llm
SAVE_FILE = "resume_data.json"

class ResumeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор резюме RESUMECRAFT")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #f0f8ff;")
        self.resume_data = {}
        self.load_data()

        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.init_main_menu()
        self.init_full_resume_form()
        self.init_block_generation()
        self.init_generated_resume_view()

    def styled_button(self, text, action):
        button = QPushButton(text)
        button.setFont(QFont("Verdana", max(self.width() // 50, 14)))
        button.setStyleSheet("""
            QPushButton {
                background-color: #4682b4;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #5a9bd3;
            }
        """)
        button.clicked.connect(action)
        return button

    def styled_input(self, placeholder):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFont(QFont("Verdana", 12))
        input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4682b4;
                border-radius: 10px;
                padding: 10px;
                background-color: #ffffff;
                color: #333333;
            }
            QLineEdit:focus {
                border-color: #5a9bd3;
            }
        """)
        return input_field

    def init_main_menu(self):
        main_menu = QWidget()
        layout = QVBoxLayout(main_menu)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Давайте начнем генерировать ваше резюме!")
        title.setFont(QFont("Verdana", 24))
        title.setStyleSheet("color: #333333; font-weight: bold;")
        layout.addWidget(title)

        generate_full_button = self.styled_button("Генерировать полное резюме", self.start_full_resume_form)
        layout.addWidget(generate_full_button)

        generate_block_button = self.styled_button("Генерировать отдельный блок", lambda: self.stacked_widget.setCurrentWidget(self.block_gen_page))
        layout.addWidget(generate_block_button)

        exit_button = self.styled_button("Выход", self.close)
        layout.addWidget(exit_button)

        self.stacked_widget.addWidget(main_menu)

    def init_full_resume_form(self):
        self.form_pages = QStackedWidget()
        self.stacked_widget.addWidget(self.form_pages)

        self.init_personal_info_page()
        self.init_professional_info_page()
        self.init_skills_and_hobbies_page()

    def init_personal_info_page(self):
        personal_info_page = QWidget()
        layout = QVBoxLayout(personal_info_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Личная информация")
        title.setFont(QFont("Verdana", 18))
        title.setStyleSheet("color: #333333; font-weight: bold;")
        layout.addWidget(title)

        self.personal_fields = {}
        fields = {
            "Имя": "Иван Иванов",
            "Телефон": "+7 (999) 123-45-67",
            "Электронная почта": "ivan.ivanov@example.com",
            "Город проживания": "Москва",
            "Ссылки на профили (LinkedIn, GitHub)": "linkedin.com/in/ivanov, github.com/ivanov"
        }

        for field, placeholder in fields.items():
            field_label = QLabel(field)
            field_label.setFont(QFont("Verdana", 12))
            field_label.setStyleSheet("color: #000000;")
            layout.addWidget(field_label)

            input_field = self.styled_input(placeholder)
            layout.addWidget(input_field)
            self.personal_fields[field] = input_field

        navigation_layout = QHBoxLayout()

        back_button = self.styled_button("Назад", lambda: self.stacked_widget.setCurrentIndex(0))
        navigation_layout.addWidget(back_button)

        next_button = self.styled_button("Далее", lambda: self.form_pages.setCurrentIndex(1))
        navigation_layout.addWidget(next_button)

        layout.addLayout(navigation_layout)
        self.form_pages.addWidget(personal_info_page)

    def init_professional_info_page(self):
        professional_info_page = QWidget()
        layout = QVBoxLayout(professional_info_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Профессиональная информация")
        title.setFont(QFont("Verdana", 18))
        title.setStyleSheet("color: #333333; font-weight: bold;")
        layout.addWidget(title)

        self.professional_fields = {}
        fields = {
            "Название компании": "ООО Пример",
            "Должность": "Разработчик",
            "Период работы": "2019-2023",
            "Обязанности": "Разработка программного обеспечения",
            "Образование": "МГУ, факультет информатики, 2015-2019"
        }

        for field, placeholder in fields.items():
            field_label = QLabel(field)
            field_label.setFont(QFont("Verdana", 12))
            field_label.setStyleSheet("color: #000000;")
            layout.addWidget(field_label)

            input_field = self.styled_input(placeholder)
            layout.addWidget(input_field)
            self.professional_fields[field] = input_field

        navigation_layout = QHBoxLayout()

        back_button = self.styled_button("Назад", lambda: self.form_pages.setCurrentIndex(0))
        navigation_layout.addWidget(back_button)

        next_button = self.styled_button("Далее", lambda: self.form_pages.setCurrentIndex(2))
        navigation_layout.addWidget(next_button)

        layout.addLayout(navigation_layout)
        self.form_pages.addWidget(professional_info_page)

    def init_skills_and_hobbies_page(self):
        skills_hobbies_page = QWidget()
        layout = QVBoxLayout(skills_hobbies_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Навыки и хобби")
        title.setFont(QFont("Verdana", 18))
        title.setStyleSheet("color: #333333; font-weight: bold;")
        layout.addWidget(title)

        self.skills_hobbies_fields = {}
        fields = {
            "Навыки": "Python, Django, SQL",
            "Хобби": "Чтение, путешествия, программирование"
        }

        for field, placeholder in fields.items():
            field_label = QLabel(field)
            field_label.setFont(QFont("Verdana", 12))
            field_label.setStyleSheet("color: #000000;")
            layout.addWidget(field_label)

            input_field = self.styled_input(placeholder)
            layout.addWidget(input_field)
            self.skills_hobbies_fields[field] = input_field

        navigation_layout = QHBoxLayout()

        back_button = self.styled_button("Назад", lambda: self.form_pages.setCurrentIndex(1))
        navigation_layout.addWidget(back_button)

        submit_button = self.styled_button("Сгенерировать", self.generate_full_resume)
        navigation_layout.addWidget(submit_button)

        layout.addLayout(navigation_layout)
        self.form_pages.addWidget(skills_hobbies_page)

    def start_full_resume_form(self):
        self.form_pages.setCurrentIndex(0)
        self.stacked_widget.setCurrentWidget(self.form_pages)

    def generate_full_resume(self):
        input_data = {}
        input_data.update({field: input.text() for field, input in self.personal_fields.items()})
        input_data.update({field: input.text() for field, input in self.professional_fields.items()})
        input_data.update({field: input.text() for field, input in self.skills_hobbies_fields.items()})

        prompt_text = (
            "Составьте профессиональное, современное и соответствующее требованиям рынка вакансий полное резюме. "
            "Все блоки должны быть структурированы и содержать сильные стороны кандидата, подчеркивая его опыт, достижения и навыки. "
            "Используйте следующие данные для подготовки резюме:\n"
            f"{json.dumps(input_data, ensure_ascii=False)}"
        )
        result = llm_chain.invoke({"question": prompt_text})
        self.resume_data["full_resume"] = result
        self.show_generated_resume(result)

    def init_block_generation(self):
        self.block_gen_page = QWidget()
        layout = QVBoxLayout(self.block_gen_page)

        title_label = QLabel("Выберите блок для генерации")
        title_label.setFont(QFont("Verdana", 16))
        title_label.setStyleSheet("color: #333333;")
        layout.addWidget(title_label)

        self.block_selection = QComboBox()
        self.block_selection.setFont(QFont("Verdana", 12))
        self.block_selection.addItems([
            "Цель", "Опыт работы", "Образование", "Навыки",
            "Достижения", "Проекты", "Личностные качества", "Хобби", "Рекомендации"
        ])
        self.block_selection.setStyleSheet("color: #333333; background-color: #ffffff;")
        layout.addWidget(self.block_selection)

        self.block_input = QTextEdit()
        self.block_input.setFont(QFont("Verdana", 12))
        self.block_input.setPlaceholderText("Введите данные для генерации блока, например, 'Проекты: Разработка CRM...'")
        self.block_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #4682b4;
                border-radius: 10px;
                padding: 10px;
                background-color: #ffffff;
                color: #333333;
            }
        """)
        layout.addWidget(self.block_input)

        generate_block_button = self.styled_button("Сгенерировать блок", self.generate_block)
        layout.addWidget(generate_block_button)

        back_button = self.styled_button("Назад", lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button)

        self.stacked_widget.addWidget(self.block_gen_page)

    def generate_block(self):
        block_name = self.block_selection.currentText()
        block_input = self.block_input.toPlainText()
        prompt_text = (
            f"Составьте профессиональный текст для раздела резюме '{block_name}'. "
            "Текст должен быть качественным, структурированным и соответствовать современным требованиям рынка. "
            "Укажите достижения, опыт и навыки, которые максимально подчеркнут ценность кандидата. Используйте следующие данные:\n"
            f"{block_input}"
        )
        result = llm_chain.invoke({"question": prompt_text})
        self.resume_data[block_name] = result
        self.show_generated_resume(result)

    def init_generated_resume_view(self):
        self.generated_view = QWidget()
        self.generated_layout = QVBoxLayout(self.generated_view)
        self.generated_text = QTextEdit()
        self.generated_text.setReadOnly(True)
        self.generated_text.setFont(QFont("Verdana", 12))
        self.generated_layout.addWidget(self.generated_text)

        save_button = self.styled_button("Сохранить в PDF", self.save_to_pdf)
        self.generated_layout.addWidget(save_button)

        back_button = self.styled_button("Назад", lambda: self.stacked_widget.setCurrentIndex(0))
        self.generated_layout.addWidget(back_button)

        self.stacked_widget.addWidget(self.generated_view)

    def show_generated_resume(self, text):
        cleaned_text = text.replace("*", "")  
        self.generated_text.setStyleSheet("color: black;")
        self.generated_text.setText(cleaned_text)
        self.stacked_widget.setCurrentWidget(self.generated_view)

    def save_to_pdf(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(filter="PDF Files (*.pdf)")
        if file_path:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font("ArialUnicode", "", "C:/Windows/Fonts/arial.ttf", uni=True)
                pdf.set_font("ArialUnicode", size=12)
                # Удаляем звездочки перед сохранением в PDF
                cleaned_text = self.generated_text.toPlainText().replace("*", "")
                pdf.multi_cell(0, 10, cleaned_text)
                pdf.output(file_path)

                # Создаём сообщение об успешном сохранении
                success_message = QMessageBox(self)
                success_message.setText(f"Резюме сохранено в {file_path}")
                success_message.setStyleSheet("color: black; background-color: white;")
                success_message.exec()
            except Exception as e:
                error_box = QMessageBox()
                error_box.setText(f"Не удалось сохранить PDF: {str(e)}")
                error_box.setStyleSheet("color: black; background-color: white;")
                error_box.exec()

    def save_data(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.resume_data, f)

    def load_data(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                self.resume_data = json.load(f)

if __name__ == "__main__":
    app = QApplication([])
    main_app = ResumeApp()
    main_app.show()
    app.exec()
