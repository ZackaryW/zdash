from qfluentwidgets import ElevatedCardWidget, ImageLabel, CaptionLabel
from PyQt5.QtWidgets import QVBoxLayout, QDialog
from PyQt5.QtCore import Qt
from .editDialog import PathEditDialog

class PathCard(ElevatedCardWidget):
    def __init__(self, path_info, parent=None):
        from zdash import config
        super().__init__(parent)
        self.path = path_info.get("path")
        self._mod = config.mods[path_info.get("type")]
        self.name = path_info.get("aname", self._mod.get_name(self.path))
        self.icon = path_info.get("icon") or self._mod.get_icon()
        self.description = path_info.get("description")
        self._dict = path_info

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignLeft)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)
        
        # Set minimum and maximum widths for the card
        self.setMinimumWidth(200)
        self.setMaximumWidth(400)
        
        # Icon and name in horizontal layout at top
        self.iconWidget = ImageLabel(self.icon, self)
        self.iconWidget.scaledToHeight(32)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignLeft)
            
        self.nameLabel = CaptionLabel(self.name, self)
        self.nameLabel.setStyleSheet("font-size: 16pt; font-weight: bold;")
        self.nameLabel.setWordWrap(True)
        self.vBoxLayout.addWidget(self.nameLabel)
        
        # Path below name
        self.pathLabel = CaptionLabel(self.path, self)
        self.pathLabel.setWordWrap(True)
        self.pathLabel.setMaximumWidth(380)
        self.vBoxLayout.addWidget(self.pathLabel)
        
        # Description at bottom if provided
        if self.description:
            self.descLabel = CaptionLabel(self.description, self)
            self.descLabel.setWordWrap(True)
            self.descLabel.setMaximumWidth(380)
            self.vBoxLayout.addWidget(self.descLabel)

        # Set fixed size for the card
        self.setFixedSize(400, 200)

    def mousePressEvent(self, event):
        # if left click, open the path
        if event.button() == Qt.LeftButton:
            self._mod.on_path_click(self.path)
        elif event.button() == Qt.RightButton:
            # Show edit dialog
            dialog = PathEditDialog(self._dict, self)
            from zdash import config
            if dialog.exec_() == QDialog.Accepted:
                # Update the card with new information
                updated_info = dialog.get_updated_info()
                self._dict.update(updated_info)
                config.save_config()
                # Update display
                self.name = updated_info.get("aname", self._mod.get_name(self.path))
                self.description = updated_info.get("description")
                
                # Update labels
                self.nameLabel.setText(self.name)
                if self.description:
                    if hasattr(self, 'descLabel'):
                        self.descLabel.setText(self.description)
                    else:
                        self.descLabel = CaptionLabel(self.description, self)
                        self.descLabel.setWordWrap(True)
                        self.descLabel.setMaximumWidth(380)
                        self.vBoxLayout.addWidget(self.descLabel)
        else:
            super().mousePressEvent(event)