import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QGridLayout, QApplication
from qfluentwidgets import ElevatedCardWidget, ImageLabel, CaptionLabel

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
            self.show_edit_dialog()
        else:
            super().mousePressEvent(event)

class CardListWindow(QWidget):
    def __init_search_bar(self):
        from qfluentwidgets import SearchLineEdit
        self.search_bar = SearchLineEdit()
        self.search_bar.setPlaceholderText("Search paths...")
        self.search_bar.textChanged.connect(self.filter_cards)
        return self.search_bar

    def filter_cards(self, text):
        text = text.lower()
        
        # Check for field-specific searches
        field_searches = {}
        search_terms = []
        
        for term in text.split():
            if ":" in term:
                field, value = term.split(":", 1)
                if field in ["name", "path"]:
                    field_searches[field] = value
            else:
                search_terms.append(term)
                
        # Combine remaining terms
        general_search = " ".join(search_terms)
        
        for i in range(self.gridLayout.count()):
            widget = self.gridLayout.itemAt(i).widget()
            if widget:
                name = widget.nameLabel.text().lower()
                path = widget.pathLabel.text().lower()
                
                # Check field-specific searches first
                matches = True
                if "name" in field_searches:
                    matches = matches and field_searches["name"] in name
                if "path" in field_searches:
                    matches = matches and field_searches["path"] in path
                    
                # If no field searches or they all matched, check general search
                if matches and general_search:
                    matches = general_search in name or general_search in path
                    
                widget.setVisible(matches)


    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('ZDash Cards')
        self.resize(800, 600)
        self.search_bar = self.__init_search_bar()
        # Create main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.search_bar)
        # Create scroll area
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Create container widget for grid
        container = QWidget()
        self.gridLayout = QGridLayout(container)
        self.gridLayout.setSpacing(10)
        
        # Make columns stretch evenly
        container.setLayout(self.gridLayout)
        
        # Add cards to grid
        self.populate_cards()
        
        scrollArea.setWidget(container)
        mainLayout.addWidget(scrollArea)

    def populate_cards(self):
        row = 0
        col = 0
        available_width = self.width() - 40
        card_width = 250
        max_cols = max(1, available_width // card_width)

        for path_info in self.config.pathes:
            card = PathCard(path_info, parent=self)
            self.gridLayout.addWidget(card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Make columns stretch evenly
        for i in range(max_cols):
            self.gridLayout.setColumnStretch(i, 1)

def main():
    app = QApplication(sys.argv)
    from zdash import config
    window = CardListWindow(config)
    window.show()
    sys.exit(app.exec_())

