import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout, QApplication
from qfluentwidgets import ScrollArea
from .card import PathCard

class CardListWindow(QWidget):
    def __init_search_bar(self):
        from qfluentwidgets import SearchLineEdit
        self.search_bar = SearchLineEdit()
        self.search_bar.setPlaceholderText("Search paths...")
        self.search_bar.textChanged.connect(self.filter_cards)
        self.current_filter = ""
        return self.search_bar

    def filter_cards(self, text):
        self.current_filter = text
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
        # Replace QScrollArea with FluentUI's ScrollArea
        scrollArea = ScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Create container widget for grid
        container = QWidget()
        self.gridLayout = QGridLayout(container)
        self.gridLayout.setSpacing(10)
        
        container.setLayout(self.gridLayout)
        
        # Add cards to grid
        self.populate_cards()
        
        scrollArea.setWidget(container)
        mainLayout.addWidget(scrollArea)

        # Add resize timer to prevent excessive updates
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.handle_resize)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Reset and start the timer
        self.resize_timer.start(150)  # 150ms delay

    def handle_resize(self):
        # Clear the grid layout
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            if item.widget():
                item.widget().hide()
        # Repopulate with new column count
        self.populate_cards()
        # Reapply the current filter
        if self.current_filter:
            self.filter_cards(self.current_filter)

    def populate_cards(self):
        row = 0
        col = 0
        # Calculate available width considering margins and spacing
        available_width = self.width() - (self.gridLayout.spacing() * 2) - 40
        card_width = 250
        spacing = self.gridLayout.spacing()
        
        # Calculate how many columns can fit while ensuring full card width
        # Include spacing between cards in the calculation
        max_cols = max(1, (available_width + spacing) // (card_width + spacing) -1)
        
        # Verify that each card will have its minimum width
        actual_card_width = (available_width - (spacing * (max_cols - 1))) / max_cols
        if actual_card_width < card_width and max_cols > 1:
            max_cols -= 1

        # Show all previously hidden widgets
        for path_info in self.config.pathes:
            card = None
            # Try to find existing card
            for i in range(self.gridLayout.count()):
                widget = self.gridLayout.itemAt(i).widget()
                if widget and widget._dict == path_info:
                    card = widget
                    break
            
            # Create new card if not found
            if not card:
                card = PathCard(path_info, parent=self)
            
            card.show()  # Make sure card is visible
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

