"""Splash screen for ACSC application."""

import sys
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QProgressBar, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class SplashScreen(QWidget):
    """Splash screen displayed during application startup."""

    def __init__(self):
        super().__init__()
        from acsc import __version__

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Container with sharp edges, modern dark theme
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #0d0d0d;
                border: none;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(0, 0, 0, 0)

        # Top accent line
        accent_line = QFrame()
        accent_line.setFixedHeight(3)
        accent_line.setStyleSheet("background-color: #00a8ff;")
        container_layout.addWidget(accent_line)

        # Content area
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(50, 40, 50, 30)

        # Logo and title row
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)

        # Logo
        logo_label = QLabel()
        logo_path = self._get_logo_path()
        if logo_path and os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            logo_label.setText("ACSC")
            logo_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #00a8ff;")
        logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo_label)

        # Title block
        title_block = QWidget()
        title_layout = QVBoxLayout(title_block)
        title_layout.setSpacing(5)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("ACSC")
        title_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: 4px;
        """)
        title_layout.addWidget(title_label)

        subtitle_label = QLabel("Axial Compressive Strength Calculator")
        subtitle_label.setStyleSheet("""
            font-size: 12px;
            font-weight: 400;
            color: #888888;
            letter-spacing: 1px;
        """)
        title_layout.addWidget(subtitle_label)

        header_layout.addWidget(title_block)
        header_layout.addStretch()

        content_layout.addLayout(header_layout)

        # Spacer
        content_layout.addStretch()

        # Version
        version_label = QLabel(f"v{__version__}")
        version_label.setStyleSheet("""
            font-size: 11px;
            font-weight: 500;
            color: #00a8ff;
            letter-spacing: 2px;
        """)
        version_label.setAlignment(Qt.AlignLeft)
        content_layout.addWidget(version_label)

        # Progress section
        progress_section = QWidget()
        progress_layout = QVBoxLayout(progress_section)
        progress_layout.setSpacing(8)
        progress_layout.setContentsMargins(0, 0, 0, 0)

        # Loading message
        self.loading_label = QLabel("INITIALIZING")
        self.loading_label.setStyleSheet("""
            font-size: 10px;
            font-weight: 500;
            color: #555555;
            letter-spacing: 3px;
        """)
        progress_layout.addWidget(self.loading_label)

        # Progress bar - thin line style
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #1a1a1a;
                height: 2px;
            }
            QProgressBar::chunk {
                background-color: #00a8ff;
            }
        """)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 0)
        progress_layout.addWidget(self.progress_bar)

        content_layout.addWidget(progress_section)

        container_layout.addWidget(content)

        # Bottom bar with copyright
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet("background-color: #0a0a0a;")
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(50, 12, 50, 12)

        copyright_label = QLabel("© 2025 Naruki Ichihara")
        copyright_label.setStyleSheet("""
            font-size: 9px;
            color: #444444;
            letter-spacing: 1px;
        """)
        bottom_layout.addWidget(copyright_label)
        bottom_layout.addStretch()

        container_layout.addWidget(bottom_bar)

        layout.addWidget(container)

        # Set size and center
        self.setFixedSize(480, 280)
        self._center_on_screen()

    def _get_logo_path(self):
        """Get path to logo file."""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'assets', 'acsc_logo.png'),
            os.path.join(os.path.dirname(__file__), 'assets', 'acsc_logo.png'),
            os.path.join(sys.prefix, 'assets', 'acsc_logo.png'),
        ]

        if getattr(sys, 'frozen', False):
            app_path = os.path.dirname(sys.executable)
            possible_paths.insert(0, os.path.join(app_path, '_internal', 'assets', 'acsc_logo.png'))
            possible_paths.insert(0, os.path.join(app_path, 'assets', 'acsc_logo.png'))

        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def _center_on_screen(self):
        """Center the splash screen on the primary screen."""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)

    def setMessage(self, message):
        """Update the loading message."""
        self.loading_label.setText(message.upper())
        QApplication.processEvents()
