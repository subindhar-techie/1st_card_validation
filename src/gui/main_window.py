import tkinter as tk
import os
import sys

from tkinter import ttk , messagebox

try:
    from runtime_hook import resource_path
except ImportError:
    # Fallback for development
    def resource_path(relative_path):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_root = os.path.dirname(current_dir)
        base_path = getattr(sys, '_MEIPASS', project_root)
        return os.path.join(base_path, relative_path)

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Validation Tool")
        self.root.geometry("500x600")
        
        # DISABLE ONLY MAXIMIZE BUTTON - Allow minimize and close
        self.root.resizable(False, False)
        self.root.configure(bg="#f8f9fa")
        
        # CENTER THE WINDOW ON SCREEN
        self.center_window()
        
        # Set icon
        try:
            icon_path = self.get_icon_path()
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon error: {e}")
        
        self.create_launcher_interface()
    
    def center_window(self):
        """
        Center the window on the screen
        """
        # Update the window to get the correct dimensions
        self.root.update_idletasks()
        
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Get window width and height
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Calculate position coordinates
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set the window position
        self.root.geometry(f"+{x}+{y}")
    
    def get_icon_path(self):
        """Get the absolute path to the application icon"""
        try:
            from runtime_hook import resource_path
            icon_path = resource_path('assets/icons/Reliance_Jio_Logo.ico')
            if os.path.exists(icon_path):
                return icon_path
            return None
        except Exception as e:
            print(f"Error finding icon: {e}")
            # Fallback to development path
            current_dir = os.path.dirname(__file__)
            project_root = os.path.join(current_dir, '..', '..')
            icon_path = os.path.join(project_root, 'assets', 'icons', 'Reliance_Jio_Logo.ico')
            return os.path.abspath(icon_path)
    
    def create_launcher_interface(self):
        # Main container
        main_container = tk.Frame(self.root, bg="#f8f9fa")
        main_container.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Header
        header_frame = tk.Frame(main_container, bg="#f8f9fa")
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Validation",
            font=('Segoe UI', 24, 'bold'),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Select a validation tool to launch",
            font=('Segoe UI', 12),
            bg="#f8f9fa",
            fg="#7f8c8d"
        )
        subtitle_label.pack()
        
        # Cards container
        cards_frame = tk.Frame(main_container, bg="#f8f9fa")
        cards_frame.pack(fill='both', expand=True)
        
        # Create tool cards
        self.create_tool_card(cards_frame, "First Card Validation", self.launch_first_card_tab)
        self.create_tool_card(cards_frame, "Machine Log Validation", self.launch_machine_log_tab)
        self.create_tool_card(cards_frame, "MNO File Validation", self.launch_mno_file_tab)
        
        # Status bar
        self.status_frame = tk.Frame(self.root, bg="#e9ecef", height=30)
        self.status_frame.pack(fill='x', side='bottom')
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready to launch validation tools",
            font=('Segoe UI', 9),
            bg="#e9ecef",
            fg="#6c757d"
        )
        self.status_label.pack(side='left', padx=10, pady=5)
    
    def create_tool_card(self, parent, title, command):
        """Simple modern rounded card style"""
        card = tk.Frame(
            parent,
            bg="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#d0d0d0"
        )
        card.pack(fill='x', pady=12, ipady=12)

        # Rounded corners effect (simulated using padding)
        inner = tk.Frame(card, bg="white")
        inner.pack(fill='x', padx=10, pady=10)

        title_label = tk.Label(
            inner,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2c3e50",
            anchor="w",
            pady=5
        )
        title_label.pack(side="left", padx=10)

        launch_btn = tk.Button(
            inner,
            text="Launch →",
            font=("Segoe UI", 10, "bold"),
            bg="#0078D4",
            fg="white",
            relief="flat",
            padx=20,
            pady=6,
            cursor="hand2",
            command=command
        )
        launch_btn.pack(side="right", padx=10)

        # Make full card clickable
        card.bind("<Button-1>", lambda e: command())
        inner.bind("<Button-1>", lambda e: command())
        title_label.bind("<Button-1>", lambda e: command())

        # Hover effect
        def hover(e):
            card.config(highlightbackground="#0078D4")
        def leave(e):
            card.config(highlightbackground="#d0d0d0")

        card.bind("<Enter>", hover)
        card.bind("<Leave>", leave)
    
    def launch_first_card_tab(self):
        """Launch First Card Validation in new window"""
        self.update_status("Launching First Card Validation...")

        try:
            from .tabs.first_card_tab import FirstCardTab
            
            # Hide main window
            self.root.withdraw()

            # Create child window
            new_window = tk.Toplevel(self.root)
            new_window.title("First Card Validation")
            new_window.geometry("820x750")
            
            # DISABLE ONLY MAXIMIZE BUTTON for child window
            new_window.resizable(False, False)
            
            # CENTER THE CHILD WINDOW
            self.center_child_window(new_window)

            # When child closes → show main window
            def on_close():
                new_window.destroy()
                self.root.deiconify()

            new_window.protocol("WM_DELETE_WINDOW", on_close)

            FirstCardTab(new_window)
            self.update_status("First Card Validation launched successfully")

        except Exception as e:
            self.update_status(f"Error launching First Card Validation: {str(e)}")

    def launch_machine_log_tab(self):
        """Launch Machine Log Validation in new window"""
        self.update_status("Launching Machine Log Validation...")

        try:
            from .tabs.machine_log_tab import MachineLogTab

            self.root.withdraw()

            new_window = tk.Toplevel(self.root)
            new_window.title("Machine Log Validation")
            new_window.geometry("800x700")
            
            # DISABLE ONLY MAXIMIZE BUTTON for child window
            new_window.resizable(False, False)
            
            # CENTER THE CHILD WINDOW
            self.center_child_window(new_window)

            def on_close():
                new_window.destroy()
                self.root.deiconify()

            new_window.protocol("WM_DELETE_WINDOW", on_close)

            MachineLogTab(new_window)
            self.update_status("Machine Log Validation launched successfully")

        except Exception as e:
            self.update_status(f"Error launching Machine Log Validation: {str(e)}")

    def launch_mno_file_tab(self):
        """Launch MNO File Validation in new window"""
        self.update_status("Launching MNO File Validation...")

        try:
            from .tabs.mno_file_tab import MNOFileTab
                
            self.root.withdraw()

            new_window = tk.Toplevel(self.root)
            new_window.title("MNO File Validation")
            new_window.geometry("900x800")
            
            # DISABLE ONLY MAXIMIZE BUTTON for child window
            new_window.resizable(False, False)
            
            # CENTER THE CHILD WINDOW
            self.center_child_window(new_window)

            def on_close():
                new_window.destroy()
                self.root.deiconify()
                self.update_status("Ready to launch validation tools")

            new_window.protocol("WM_DELETE_WINDOW", on_close)

            MNOFileTab(new_window)
            self.update_status("MNO File Validation launched successfully")

        except ImportError as e:
            self.update_status(f"Error importing MNOFileTab: {str(e)}")
            messagebox.showerror(
                "Import Error", 
                f"Cannot import MNOFileTab from tabs directory\n\n"
                f"Error: {str(e)}\n\n"
                f"Please ensure mno_file_tab.py exists in the tabs directory."
            )
        except Exception as e:
            self.update_status(f"Error launching MNO File Validation: {str(e)}")
            messagebox.showerror("Error", f"Failed to launch: {str(e)}")
    
    def center_child_window(self, window):
        """
        Center a child window on the screen
        """
        # Update the window to get the correct dimensions
        window.update_idletasks()
        
        # Get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Get window width and height
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        
        # Calculate position coordinates
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set the window position
        window.geometry(f"+{x}+{y}")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()