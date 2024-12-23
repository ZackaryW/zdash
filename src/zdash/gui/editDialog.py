from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from qfluentwidgets import LineEdit, TextEdit
from .tagEdit import TagsEdit

class PathEditDialog(QDialog):
    def __init__(self, path_info, parent=None):
        super().__init__(parent)
        self.path_info = path_info
        self.setWindowTitle("Edit Path Details")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Name/Alias field
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:", self)
        self.name_edit = LineEdit(self)
        self.name_edit.setText(self.path_info.get("aname", ""))
        self.name_edit.setPlaceholderText("Custom name for this path")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Description field
        desc_label = QLabel("Description:", self)
        layout.addWidget(desc_label)
        self.desc_edit = TextEdit(self)
        self.desc_edit.setText(self.path_info.get("description", ""))
        self.desc_edit.setPlaceholderText("Add a description")
        layout.addWidget(self.desc_edit)

        # Tags field
        tags_label = QLabel("Tags:", self)
        layout.addWidget(tags_label)
        self.tags_edit = TagsEdit(self)
        current_tags = self.path_info.get("tags", [])
        if isinstance(current_tags, str):
            current_tags = current_tags.split(",")
        self.tags_edit.addTags(current_tags)
        layout.addWidget(self.tags_edit)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save", self)
        cancel_button = QPushButton("Cancel", self)
        
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Set dialog size
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

    def get_updated_info(self):
        """Return the updated path info dictionary"""
        updated_info = self.path_info.copy()
        
        # Update only if values are different from default/empty
        name = self.name_edit.text().strip()
        if name:
            updated_info["aname"] = name
            
        description = self.desc_edit.toPlainText().strip()
        if description:
            updated_info["description"] = description
            
        tags = self.tags_edit.getTags()
        if tags:
            updated_info["tags"] = tags
            
        return updated_info
