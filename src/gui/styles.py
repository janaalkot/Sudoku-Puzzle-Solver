"""
Custom styling module for the Sudoku Solver application.
Provides modern, professional styling for all GUI components.
"""

import tkinter as tk
from tkinter import ttk

class SudokuStyles:
    """
    Manages all styling for the Sudoku Solver application.
    Provides a modern, cohesive color scheme and professional appearance.
    """
    
    # Color Palette - Modern Blue Theme
    COLORS = {
        # Primary colors
        'primary': '#1976D2',           # Deep blue
        'primary_dark': '#1565C0',      # Darker blue
        'primary_light': '#42A5F5',     # Light blue
        'accent': '#FF9800',            # Orange accent
        'accent_dark': '#F57C00',       # Dark orange
        
        # Background colors
        'bg_main': '#F5F5F5',           # Light gray background
        'bg_panel': '#FFFFFF',          # White panels
        'bg_grid': '#FAFAFA',           # Very light gray for grid
        'bg_fixed': '#E3F2FD',          # Light blue for fixed cells
        
        # Cell state colors
        'cell_attempt': '#FFF9C4',      # Yellow - attempting
        'cell_reject': '#F44336',       # Red - rejected
        'cell_place': '#4CAF50',        # Green - placed
        'cell_backtrack': '#FFCDD2',    # Light red - backtracking
        'cell_solution': '#2196F3',     # Blue - solution
        'cell_cultural': '#FF9800',     # Orange - cultural algo
        
        # Text colors
        'text_primary': '#212121',      # Dark gray
        'text_secondary': '#757575',    # Medium gray
        'text_light': '#FFFFFF',        # White
        'text_fixed': '#0D47A1',        # Dark blue for fixed
        
        # Border colors
        'border_light': '#E0E0E0',      # Light border
        'border_dark': '#9E9E9E',       # Dark border
        'border_accent': '#1976D2',     # Accent border
        
        # Status colors
        'success': '#4CAF50',           # Green
        'warning': '#FF9800',           # Orange
        'error': '#F44336',             # Red
        'info': '#2196F3',              # Blue
    }
    
    # Fonts
    FONTS = {
        'title': ('Segoe UI', 16, 'bold'),
        'heading': ('Segoe UI', 12, 'bold'),
        'subheading': ('Segoe UI', 10, 'bold'),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 8),
        'cell_large': ('Arial', 20, 'bold'),      # Increased from 16
        'cell_normal': ('Arial', 18, 'bold'),     # Increased from 14
        'cell_small': ('Arial', 16, 'bold'),      # Increased from 12
    }
    
    def __init__(self, root):
        """
        Initialize the styling system.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.style = ttk.Style(root)
        
        # Set theme base
        try:
            self.style.theme_use('clam')  # Modern looking theme
        except:
            self.style.theme_use('default')
        
        self._configure_styles()
        self._configure_root()
    
    def _configure_root(self):
        """Configure the root window appearance."""
        self.root.configure(bg=self.COLORS['bg_main'])
    
    def _configure_styles(self):
        """Configure all ttk widget styles."""
        
        # Frame styles
        self.style.configure('Main.TFrame',
                           background=self.COLORS['bg_main'])
        
        self.style.configure('Panel.TFrame',
                           background=self.COLORS['bg_panel'],
                           relief='flat')
        
        self.style.configure('Grid.TFrame',
                           background=self.COLORS['bg_grid'],
                           relief='solid',
                           borderwidth=2,
                           bordercolor=self.COLORS['border_accent'])
        
        # Label styles
        self.style.configure('Title.TLabel',
                           background=self.COLORS['bg_panel'],
                           foreground=self.COLORS['primary'],
                           font=self.FONTS['title'],
                           padding=5)
        
        self.style.configure('Heading.TLabel',
                           background=self.COLORS['bg_panel'],
                           foreground=self.COLORS['text_primary'],
                           font=self.FONTS['heading'],
                           padding=3)
        
        self.style.configure('Body.TLabel',
                           background=self.COLORS['bg_panel'],
                           foreground=self.COLORS['text_secondary'],
                           font=self.FONTS['body'])
        
        self.style.configure('Hint.TLabel',
                           background=self.COLORS['bg_panel'],
                           foreground=self.COLORS['text_secondary'],
                           font=self.FONTS['small'])
        
        # Button styles
        self.style.configure('Primary.TButton',
                           background=self.COLORS['primary'],
                           foreground=self.COLORS['text_light'],
                           font=self.FONTS['subheading'],
                           padding=(10, 5),
                           relief='flat')
        
        self.style.map('Primary.TButton',
                      background=[('active', self.COLORS['primary_light']),
                                ('pressed', self.COLORS['primary_dark'])])
        
        self.style.configure('Secondary.TButton',
                           background=self.COLORS['bg_panel'],
                           foreground=self.COLORS['text_primary'],
                           font=self.FONTS['body'],
                           padding=(8, 4),
                           relief='solid',
                           borderwidth=1)
        
        self.style.map('Secondary.TButton',
                      background=[('active', self.COLORS['bg_main'])])
        
        self.style.configure('Accent.TButton',
                           background=self.COLORS['accent'],
                           foreground=self.COLORS['text_light'],
                           font=self.FONTS['subheading'],
                           padding=(10, 5),
                           relief='flat')
        
        self.style.map('Accent.TButton',
                      background=[('active', self.COLORS['accent_dark'])])
        
        # Combobox styles
        self.style.configure('TCombobox',
                           fieldbackground=self.COLORS['bg_panel'],
                           background=self.COLORS['primary'],
                           foreground=self.COLORS['text_primary'],
                           arrowcolor=self.COLORS['primary'],
                           borderwidth=1,
                           relief='solid')
        
        # Radiobutton styles
        self.style.configure('TRadiobutton',
                           background=self.COLORS['bg_panel'],
                           foreground=self.COLORS['text_primary'],
                           font=self.FONTS['body'])
        
        # Checkbutton styles
        self.style.configure('TCheckbutton',
                           background=self.COLORS['bg_panel'],
                           foreground=self.COLORS['text_primary'],
                           font=self.FONTS['body'])
        
        # LabelFrame styles
        self.style.configure('Card.TLabelframe',
                           background=self.COLORS['bg_panel'],
                           relief='flat',
                           borderwidth=0)
        
        self.style.configure('Card.TLabelframe.Label',
                           background=self.COLORS['bg_panel'],
                           foreground=self.COLORS['primary'],
                           font=self.FONTS['heading'])
        
        # Scale (slider) styles
        self.style.configure('TScale',
                           background=self.COLORS['bg_panel'],
                           troughcolor=self.COLORS['bg_main'],
                           borderwidth=0,
                           relief='flat')
    
    def create_cell_style(self, cell_widget, state='normal', is_fixed=False):
        """
        Apply styling to a Sudoku grid cell.
        
        Args:
            cell_widget: The Entry widget to style
            state: The cell state ('normal', 'attempt', 'reject', 'place', 'backtrack', 'solution')
            is_fixed: Whether this is a fixed (original) cell
        """
        if is_fixed:
            cell_widget.configure(
                bg=self.COLORS['bg_fixed'],
                fg=self.COLORS['text_fixed'],
                font=self.FONTS['cell_normal'],  # Using larger font
                relief='flat',
                borderwidth=0,
                highlightthickness=0,
                disabledbackground=self.COLORS['bg_fixed'],
                disabledforeground=self.COLORS['text_fixed']
            )
        else:
            # State-based coloring
            state_colors = {
                'normal': (self.COLORS['bg_panel'], self.COLORS['text_primary']),
                'attempt': (self.COLORS['cell_attempt'], self.COLORS['text_primary']),
                'reject': (self.COLORS['cell_reject'], self.COLORS['text_light']),
                'place': (self.COLORS['cell_place'], self.COLORS['text_light']),
                'backtrack': (self.COLORS['cell_backtrack'], self.COLORS['text_primary']),
                'solution': (self.COLORS['bg_panel'], self.COLORS['cell_solution']),
                'cultural': (self.COLORS['bg_panel'], self.COLORS['cell_cultural']),
            }
            
            bg_color, fg_color = state_colors.get(state, state_colors['normal'])
            
            cell_widget.configure(
                bg=bg_color,
                fg=fg_color,
                font=self.FONTS['cell_normal'],  # Using larger font
                relief='flat',
                borderwidth=0,
                highlightthickness=0,
                insertbackground=self.COLORS['primary']
            )
    
    def create_text_widget_style(self, text_widget):
        """
        Apply styling to a Text widget.
        
        Args:
            text_widget: The Text widget to style
        """
        text_widget.configure(
            bg=self.COLORS['bg_panel'],
            fg=self.COLORS['text_primary'],
            font=self.FONTS['body'],
            relief='flat',
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.COLORS['border_light'],
            highlightcolor=self.COLORS['border_accent'],
            insertbackground=self.COLORS['primary'],
            selectbackground=self.COLORS['primary_light'],
            selectforeground=self.COLORS['text_light'],
            padx=10,
            pady=10
        )
    
    def create_status_bar_style(self, label_widget):
        """
        Apply styling to the status bar.
        
        Args:
            label_widget: The status bar label widget
        """
        label_widget.configure(
            background=self.COLORS['bg_panel'],
            foreground=self.COLORS['text_secondary'],
            font=self.FONTS['body'],
            relief='flat',
            borderwidth=1,
            anchor='w',
            padding=5
        )
