from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from qfluentwidgets import PushButton, FlowLayout, InfoBadge


class TagsEdit(QWidget):
    """A widget for editing tags with a fluent design"""
    
    tagsChanged = pyqtSignal(list)  # Signal emitted when tags are modified

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tags = []
        self.setup_ui()

    def setup_ui(self):
        """Initialize the UI components"""
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create flow layout for tags
        self.tagsLayout = FlowLayout()
        self.tagsLayout.setSpacing(4)
        self.tagsLayout.setContentsMargins(0, 0, 0, 0)

        # Create input area
        self.inputLayout = QHBoxLayout()
        self.tagInput = QLineEdit(self)
        self.tagInput.setPlaceholderText("Add tag...")
        self.addButton = PushButton("Add", self)
        self.addButton.setFixedWidth(60)
        
        self.inputLayout.addWidget(self.tagInput)
        self.inputLayout.addWidget(self.addButton)

        self.layout.addLayout(self.tagsLayout)
        self.layout.addLayout(self.inputLayout)

        # Connect signals
        self.addButton.clicked.connect(self._add_current_tag)
        self.tagInput.returnPressed.connect(self._add_current_tag)

    def _create_tag_badge(self, tag):
        """Create a badge widget for a tag"""
        badge = InfoBadge(tag, self)
        
        # Create remove button
        removeBtn = PushButton("×", self)
        removeBtn.setFixedSize(16, 16)
        removeBtn.clicked.connect(lambda: self._remove_tag(tag, badge))
        
        # Create container for badge and remove button
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        layout.addWidget(badge)
        layout.addWidget(removeBtn)
        
        return container

    def _add_current_tag(self):
        """Add the current tag from the input field"""
        tag = self.tagInput.text().strip()
        if tag and tag not in self.tags:
            self.addTag(tag)
            self.tagInput.clear()
            self.tagsChanged.emit(self.tags)

    def _remove_tag(self, tag, widget):
        """Remove a tag and its widget"""
        if tag in self.tags:
            self.tags.remove(tag)
            # Get the parent container widget
            container = widget.parent()
            # Remove the widget from the layout properly
            self.tagsLayout.removeWidget(container)
            container.deleteLater()
            self.tagsChanged.emit(self.tags)

    def addTag(self, tag):
        """Add a new tag to the widget"""
        if tag not in self.tags:
            self.tags.append(tag)
            badge = self._create_tag_badge(tag)
            self.tagsLayout.addWidget(badge)

    def addTags(self, tags):
        """Add multiple tags at once"""
        for tag in tags:
            self.addTag(tag)

    def getTags(self):
        """Return the current list of tags"""
        return self.tags.copy()

    def clear(self):
        """Remove all tags"""
        self.tags.clear()
        # Properly clear the layout
        while self.tagsLayout.count():
            item = self.tagsLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.tagsChanged.emit(self.tags) 