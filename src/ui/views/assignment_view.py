from datetime import datetime

import qtawesome as qta
from PyQt6.QtCore import QSize, Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.config.time import APP_TIMEZONE
from src.database.connection import SessionLocal
from src.database.repositories.assignment_repository import assignment_repo
from src.domain.types.assignment import AssignmentData
from src.ui.components.assignment_type_badge import assignmentType
from src.ui.styles.tokens import COLORS, FONT_SIZES
from src.utils.strip_datetime import strip_due


class AssignmentView(QWidget):

    # Emitted when user clicks "Back to assignments"
    back_requested = pyqtSignal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self._init_ui()
        self.apply_style()

    # =========================================================
    # UI
    # =========================================================

    def _init_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        # LMS Link

        self.lms_link = ""

        # =====================================
        # HEADER LAYOUT
        # =====================================

        header_layout = QHBoxLayout()

        # Back Button

        self.back_button = QPushButton()

        self.back_button.setObjectName("backButton")

        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.back_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.back_button.setIcon(
            qta.icon(
                "fa6s.arrow-left",
                color=COLORS.text_primary.name()
            )
        )

        self.back_button.setIconSize(
            QSize(
                FONT_SIZES.xl, 
                FONT_SIZES.xl
            )
        )

        self.back_button.setText(
            "Back to assignments"
        )

        self.back_button.clicked.connect(
            self.back_requested.emit
        )

        # LMS Button

        self.lms_button = QPushButton("Open LMS")

        self.lms_button.setObjectName("lmsButton")

        self.lms_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.lms_button.clicked.connect(
            self.open_lms_link
        )

        self.lms_button.setIcon(
            qta.icon(
                "fa5s.external-link-alt",
                color=COLORS.text_primary
            )
        )

        self.lms_button.setIconSize(
            QSize(
                FONT_SIZES.md, 
                FONT_SIZES.md
            )
        )

        header_layout.addWidget(
            self.back_button
        )

        header_layout.addStretch()

        header_layout.addWidget(
            self.lms_button
        )

        layout.addLayout(
            header_layout
        )

        # =====================================================
        # SCROLL AREA
        # =====================================================

        self.scroll_area = QScrollArea()

        self.scroll_area.setObjectName(
            "assignmentScrollArea"
        )

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_area.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # =====================================================
        # SCROLL CONTENT
        # =====================================================

        self.scroll_content = QWidget()

        self.scroll_content.setObjectName("scrollContent")

        self.scroll_layout = QHBoxLayout(
            self.scroll_content
        )

        self.scroll_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        self.scroll_layout.setSpacing(
            20
        )

        # =====================================================
        # LEFT SIDE
        # =====================================================

        self.left_content = QWidget()

        self.left_layout = QVBoxLayout(
            self.left_content
        )

        self.left_layout.setContentsMargins(
            0, 0, 0, 0
        )

        self.left_layout.setSpacing(20)

        # =====================================================
        # RIGHT SIDE
        # =====================================================
        
        self.right_content = QWidget()
        
        self.right_layout = QVBoxLayout(
            self.right_content
        )
        
        self.right_layout.setContentsMargins(
            0, 0, 0, 0
        )
        
        self.right_layout.setSpacing(20)

        # -----------------------------------------------------
        # Assignment Header Card
        # -----------------------------------------------------

        assignment_header = QFrame()

        assignment_header.setObjectName("assignmentHeader")

        assignment_header_layout = QVBoxLayout(
            assignment_header
        )

        assignment_header_layout.setContentsMargins(25, 25, 25, 25)

        assignment_header_layout.setSpacing(
            12
        )

        # Badge Layout

        self.badge_layout = QHBoxLayout()
        self.assignment_type_chip = assignmentType(
            assignment_type="unknown"
        )

        # Assignment title

        self.assignment_title = QLabel("")

        self.assignment_title.setObjectName(
            "assignmentTitle"
        )

        self.assignment_title.setWordWrap(True)

        # description

        self.assignment_description = QLabel("")

        self.assignment_description.setObjectName(
            "assignmentDescription"
        )

        self.assignment_description.setWordWrap(
            True
        )

        assignment_header_layout.addLayout(
            self.badge_layout
        )

        assignment_header_layout.addWidget(
            self.assignment_title
        )

        assignment_header_layout.addWidget(
            self.assignment_description
        )

        self.left_layout.addWidget(
            assignment_header
        )

        self.left_layout.addStretch()

        # =====================================================
        # DEADLINE CARD
        # =====================================================

        deadline_card = QFrame()
        deadline_card.setObjectName("deadlineCard")

        deadline_card_layout = QVBoxLayout(deadline_card)

        deadline_text = QLabel("Deadline")
        deadline_text.setObjectName("deadlineText")

        self.deadline_date = QLabel("")
        self.deadline_date.setObjectName("deadlineDate")

        self.deadline_time = QLabel("12:00AM")
        self.deadline_time.setObjectName("deadlineTime")

        deadline_card_layout.addWidget(deadline_text)
        deadline_card_layout.addWidget(self.deadline_date)
        deadline_card_layout.addWidget(self.deadline_time)
        deadline_card_layout.setSpacing(0)

        self.right_layout.addWidget(deadline_card)

        # ======================================================
        # TIME REMAINING CARD
        # ======================================================

        time_remaining_card = QFrame()
        time_remaining_card.setObjectName("timeRemainingCard")

        time_remaining_card_layout = QVBoxLayout(time_remaining_card)

        time_remaining_text = QLabel("Time Remaining")
        time_remaining_text.setObjectName("timeRemainingText")

        self.time_remaining = QLabel("")
        self.time_remaining.setObjectName("timeRemaining")

        time_remaining_card_layout.addWidget(time_remaining_text)
        time_remaining_card_layout.addWidget(self.time_remaining)

        self.right_layout.addWidget(time_remaining_card)

        # =====================================================
        # MARK AS COMPLETED BUTTON
        # =====================================================

        self.right_layout.addStretch()

        # =====================================================
        # MARK AS COMPLETED BUTTON
        # =====================================================

        mark_complete_button = QPushButton("Mark as Completed")
        mark_complete_button.setObjectName("markAsCompleted")

        self.right_layout.addWidget(mark_complete_button)


        self.scroll_layout.addWidget(self.left_content, 7)
        self.scroll_layout.addWidget(self.right_content, 3)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

    def set_assignment(self, assignment_id: str):

        db = SessionLocal()

        try:
            assignment = assignment_repo.get_by_id(
                db,
                assignment_id
            )

            if not assignment:
                return

            self.display_assignment(assignment)
            

        except Exception as e: # noqa: BLE001
            print(e)
        finally:
            db.close()


    def display_assignment(self, assignment: AssignmentData):

        due_date, due_time = strip_due(assignment.due)

        self.assignment_title.setText(
            assignment.name
        )

        self.deadline_date.setText(
            due_date
        )

        self.deadline_time.setText(
            due_time
        )

        self.lms_link = assignment.link

        self.assignment_description.setText(assignment.description)

        self.add_assginment_type(assignment)

        self.add_assginment_type(assignment)

        self.update_deadline(assignment.due)

    def open_lms_link(self):
        QDesktopServices.openUrl(QUrl(self.lms_link))


    def add_file_section(self, task: AssignmentData):
        # =====================================================
        # FILES CARD
        # =====================================================
        if task.file_count() > 0:
            
            files_card = QFrame()

            files_card.setObjectName("filesCard")

            files_layout = QVBoxLayout(
                files_card
            )

            files_layout.setContentsMargins(25, 25, 25, 25)

            files_layout.setSpacing(10)

            files_title = QLabel("Attached Files")

            files_title.setObjectName("filesTitle")

            files_layout.addWidget(
                files_title
            )

            file1 = QFrame()
            file1.setObjectName("fileButton")

            file1_layout = QHBoxLayout(file1)
            file1_layout.setContentsMargins(12, 8, 12, 8)
            file1_layout.setSpacing(10)

            # File icon
            file_icon = QLabel()
            file_icon.setPixmap(
                qta.icon(
                    "fa5.file",
                    color=COLORS.accent.name()
                ).pixmap(20, 20)
            )

            # file name 
            file_name = QLabel("Software Architecture.pdf")
            file_name.setObjectName("fileName")

            # Download Button
            download_button = QPushButton()
            download_button.setObjectName("downloadButton")
            download_button.setIcon(
                qta.icon(
                    "ph.download-simple-bold",
                    color=COLORS.text_secondary.name()
                )
            )

            download_button.setIconSize(QSize(20, 20))

            download_button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            file1_layout.addWidget(file_icon)
            file1_layout.addWidget(file_name)

            # Push download button to the right
            file1_layout.addStretch()

            file1_layout.addWidget(download_button)

            files_layout.addWidget(file1)

            self.left_layout.addWidget(files_card)

    def add_assginment_type(self, task: AssignmentData):

        if self.assignment_type_chip:
            self.assignment_type_chip.deleteLater()

        if task.type:
            assignment_type = task.type.lower()
        else:
            assignment_type = "unknown"

        self.assignment_type_chip  = assignmentType(
            assignment_type=assignment_type
        )
        
        self.badge_layout.addWidget(self.assignment_type_chip)

    def update_deadline(self, due: datetime):

        remaining_text = ""

        if not due:
            self.time_remaining.setText("No Deadline")

        remaining = due - datetime.now(APP_TIMEZONE)

        if remaining.total_seconds() <= 0:
            self.time_remaining.setText("Overdue")
            return

        days = remaining.days

        hours = remaining.seconds // 3600

        minutes = (remaining.seconds % 3600) // 60

        if days == 0:
            remaining_text = f"{hours} Hours {minutes} Mins"
        else:
            remaining_text = f"{days} Days, \n{hours} Hours {minutes} Mins"


        self.time_remaining.setText(
            remaining_text
        )

    def apply_style(self):
        self.setStyleSheet(f"""
            QWidget#scrollContent  {{
                background: {COLORS.window_bg.name()};
            }}

            QPushButton#backButton {{
                color: {COLORS.text_primary.name()};
                background: transparent;
                font-size: {FONT_SIZES.lg}px;
            }}

            QPushButton#lmsButton {{
                color: {COLORS.text_primary.name()};
                background: {COLORS.accent.name()};
                font-size: {FONT_SIZES.md}px;
                border-radius: 8px;
                font-weight: 600;
                outline: none;
                padding: 5px 10px;
            }}

            QPushButton#lmsButton:hover {{
                background-color: {COLORS.accent_hover.name()};
                border: 1px solid {COLORS.accent_hover.name()};
            }}

            QPushButton#lmsButton:pressed {{
                background-color: {COLORS.accent.name()};
            }}

            QPushButton#lmsButton:disabled {{
                background-color: {COLORS.border.name()};
                color: {COLORS.text_secondary.name()};
                border: 1px solid {COLORS.border.name()};
            }}
            QLabel#assignmentTitle {{
                color: {COLORS.text_primary.name()};
                font-size: {FONT_SIZES.xl}px;
                font-weight: 800;
            }}

            QLabel#assignmentDescription {{
                color: {COLORS.text_secondary.name()};
                font-size: {FONT_SIZES.md}px;
                font-weight: 600;
            }}

            QFrame#deadlineCard {{
                background: {COLORS.dark_bg.name()};
                border-radius: 8px;
            }}

            QFrame#timeRemainingCard {{
                background: {COLORS.accent.name()};
                border-radius: 8px;
            }}

            QLabel#deadlineText {{
                font-size: {FONT_SIZES.sm}px;
                letter-spacing: 4px;
                color: {COLORS.text_primary.name()};
            }}

            QLabel#timeRemainingText {{
                font-size: {FONT_SIZES.sm}px;
                letter-spacing: 4px;
                color: {COLORS.window_bg.name()};
            }}

            QLabel#timeRemaining {{
               color: {COLORS.window_bg.name()};
                font-size: {FONT_SIZES.xxl}px;
                font-weight: 800;
            }} 

            QLabel#deadlineDate  {{
               color: {COLORS.text_primary.name()};
                font-size: {FONT_SIZES.xxl}px;
                font-weight: 800;
            }} 

            QLabel#deadlineTime  {{
                font-size: {FONT_SIZES.xl}px;
                color: {COLORS.text_secondary.name()};
            }}

            QPushButton#markAsCompleted {{
                background-color: {COLORS.accent.name()};
                color: {COLORS.text_primary.name()};
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: 600;
            }}

            QFrame#filesCard {{
                background: {COLORS.card_bg.name()};
                border-radius: 8px;
            }}

            QFrame#fileButton {{
                background: {COLORS.dark_bg.name()};
                border-radius: 8px;
            }}

            QLabel#fileName{{
                color: {COLORS.text_primary.name()};
                font-weight: 800;
            }}

            QLabel#filesTitle{{
                color: {COLORS.text_primary.name()};
                font-size: {FONT_SIZES.xl}px;
                font-weight: 800;
            }}

            QPushButton#downloadButton {{
                background: transparent;
            }}

            QFrame#assignmentHeader {{
                background: {COLORS.card_bg.name()};
                border-radius: 8px;
            }}

        """)
