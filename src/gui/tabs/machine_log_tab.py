import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image as PILImage, ImageTk
import os
import sys

# Import resource_path function
try:
    from runtime_hook import resource_path
except ImportError:
    # Fallback for development
    def resource_path(relative_path):
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        base_path = getattr(sys, '_MEIPASS', current_dir)
        return os.path.join(base_path, relative_path)

# Setup module paths for both development and EXE
modules_path = resource_path('modules')

# Debug info
print(f"Machine Log - Running as {'EXE' if getattr(sys, 'frozen', False) else 'script'}")
print(f"Machine Log - Initial modules path: {modules_path}")

# If modules not found at expected path, try development structure
if not os.path.exists(modules_path):
    dev_modules_path = resource_path('src/modules')
    if os.path.exists(dev_modules_path):
        modules_path = dev_modules_path
        print(f"Machine Log - Using development modules path: {modules_path}")
    else:
        print(f"Machine Log - Modules directory not found: {modules_path}")

print(f"Final modules path: {modules_path}")

# Debug: List all files in modules directory
print("Machine Log - Contents of modules directory:")
if os.path.exists(modules_path):
    for root, dirs, files in os.walk(modules_path):
        level = root.replace(modules_path, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')
else:
    print(f"Machine Log - Modules directory does not exist: {modules_path}")

# Add modules path to ensure imports work
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)
    print(f"Machine Log - Added to sys.path: {modules_path}")

print(f"Machine Log Tab - sys.path: {sys.path}")
print(f"Machine Log Tab - Current dir: {os.getcwd()}")

try:
    from machine_log_validation.core.script_validator import ScriptValidator  # type: ignore
    print("SUCCESS: Imported ScriptValidator")
    
    # Fix for Pylance warning
    ScriptValidator = ScriptValidator  # type: ignore
    
except ImportError as e:
    print(f"Machine Log Import Error: {e}")
    
    # Debug: Check if file exists
    script_validator_path = os.path.join(modules_path, 'machine_log_validation', 'core', 'script_validator.py')
    print(f"Looking for file: {script_validator_path}")
    print(f"File exists: {os.path.exists(script_validator_path)}")
    
    # Show error dialog
    messagebox.showerror(
        "Import Error", 
        f"Cannot import ScriptValidator:\n{str(e)}\n\n"
        f"Looking for: {script_validator_path}\n\n"
        f"Please check the modules directory structure."
    )
    sys.exit(1)

class MachineLogTab:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
    
    def create_widgets(self):
        # Global variables for GUI components
        self.root = None
        self.script_entry = None
        self.machine_log_entry = None
        self.log_output = None
        
        self.launch_gui()

    def get_icon_path(self):
        """Get the absolute path to the application icon"""
        current_dir = os.path.dirname(__file__)
        project_root = os.path.join(current_dir, '..', '..', '..')
        icon_path = os.path.join(project_root, 'assets', 'icons', 'Reliance_Jio_Logo.ico')
        return os.path.abspath(icon_path)

    def browse_script_file(self):
        filename = filedialog.askopenfilename(
            title="Select Variable Script File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.script_entry.delete(0, tk.END)
            self.script_entry.insert(0, filename)

    def browse_machine_log_file(self):
        filename = filedialog.askopenfilename(
            title="Select Machine Log File", 
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.machine_log_entry.delete(0, tk.END)
            self.machine_log_entry.insert(0, filename)

    def validate_machine_log(self):
        """Main validation function with dynamic validation logic"""
        script_path = self.script_entry.get()
        machine_log_path = self.machine_log_entry.get()
        
        # Validation checks
        if not script_path or not machine_log_path:
            messagebox.showerror("Error", "Please select both Variable Script and Machine Log files.")
            return
        
        try:
            # Clear previous results
            self.log_output.delete(1.0, tk.END)
            self.log_output.insert(tk.END, "="*60 + "\n")
            self.log_output.insert(tk.END, "STARTING MACHINE LOG VALIDATION...\n")
            self.log_output.insert(tk.END, "="*60 + "\n\n")
            
            # Initialize validator
            validator = ScriptValidator()
            
            self.log_output.insert(tk.END, "📋 Validation Mode: Dynamic Validation\n")
            self.log_output.insert(tk.END, "   (No module type selection required)\n")
            self.log_output.insert(tk.END, "\n")
            
            # Parse files
            self.log_output.insert(tk.END, "📁 Parsing Variable Script file...\n")
            if not validator.parse_script_file(script_path):
                self.log_output.insert(tk.END, "❌ Failed to parse Variable Script file.\n")
                messagebox.showerror("Error", "Failed to parse Variable Script file.")
                return
            self.log_output.insert(tk.END, f"✅ Parsed {len(validator.script_commands)} script commands\n")
                
            self.log_output.insert(tk.END, "📁 Parsing Machine Log file...\n")
            if not validator.parse_machine_log(machine_log_path):
                self.log_output.insert(tk.END, "❌ Failed to parse Machine Log file.\n")
                messagebox.showerror("Error", "Failed to parse Machine Log file.")
                return
            self.log_output.insert(tk.END, f"✅ Parsed {len(validator.machine_logs)} machine log entries\n\n")
            
            # Run validation
            self.log_output.insert(tk.END, "🚀 Starting dynamic validation...\n")
            self.log_output.insert(tk.END, "   Step 0: Skipping irrelevant lines\n")
            self.log_output.insert(tk.END, "   Step 1: Aligning script and machine log\n")
            self.log_output.insert(tk.END, "   Step 2: Extracting and comparing SW values\n")
            self.log_output.insert(tk.END, "   Step 2.5: Checking for actual data in machine log\n")
            self.log_output.insert(tk.END, "   Step 3: Extracting and mapping placeholders\n")
            self.log_output.insert(tk.END, "\n")
            
            report = validator.validate_script_vs_machine_log()
            
            # Display results
            self.log_output.insert(tk.END, "\n" + "="*60 + "\n")
            self.log_output.insert(tk.END, "VALIDATION RESULTS\n")
            self.log_output.insert(tk.END, "="*60 + "\n\n")
            self.log_output.insert(tk.END, report + "\n")
            
            # Save report to machine log directory
            machine_log_dir = os.path.dirname(machine_log_path)
            iccid_swapped = validator.field_values.get("ICCID_CARD_SWAPPED")

            if iccid_swapped:
                report_filename = f"ICCID_{iccid_swapped}_validation_report.txt"
            else:
                log_filename = os.path.basename(machine_log_path)
                log_name = os.path.splitext(log_filename)[0]
                report_filename = f"{log_name}_validation_report.txt"

            report_path = os.path.join(machine_log_dir, report_filename)
            print(f"Report Will Be Saved To: {report_path}")        
            try:
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                self.log_output.insert(tk.END, f"\n✅ Report saved to: {report_path}\n")
                messagebox.showinfo("Success", f"Machine Log validation completed!\nReport saved to:\n{report_path}")
            except Exception as e:
                self.log_output.insert(tk.END, f"❌ Failed to save report: {str(e)}\n")
                messagebox.showwarning("Warning", f"Validation completed but failed to save report: {str(e)}")
            
        except Exception as e:
            error_msg = f"❌ Machine Log Validation Error: {str(e)}\n"
            self.log_output.insert(tk.END, error_msg)
            messagebox.showerror("Error", f"Machine Log validation failed:\n{str(e)}")

    def clear_all_fields(self):
        """Clear all input fields and log output"""
        self.script_entry.delete(0, tk.END)
        self.machine_log_entry.delete(0, tk.END)
        self.log_output.delete(1.0, tk.END)
        
        # Add initial instructions back
        self.log_output.insert(tk.END, "INSTRUCTIONS:\n")
        self.log_output.insert(tk.END, "1. Select Variable Script File and Machine Log File\n")
        self.log_output.insert(tk.END, "2. Click 'Validate Machine Log' to start validation\n")
        self.log_output.insert(tk.END, "3. No module type selection required - dynamic validation\n")
        self.log_output.insert(tk.END, "\n")
        self.log_output.insert(tk.END, "DYNAMIC VALIDATION LOGIC:\n")
        self.log_output.insert(tk.END, "- Step 0: Skip irrelevant lines (0012000000SW9000, PPS:, AES_)\n")
        self.log_output.insert(tk.END, "- Step 1: Define Source (Script) and Designation (Machine Log)\n")
        self.log_output.insert(tk.END, "- Step 2: Extract Actual SW and Compare for Success\n")
        self.log_output.insert(tk.END, "- Step 2.5: Check Machine Log for Actual Data (not placeholders)\n")
        self.log_output.insert(tk.END, "- Step 3: Extract and Map Placeholders (Only After SW Success)\n")
        self.log_output.insert(tk.END, "- Step 4: Construct Full APDU (After Placeholder Replacement)\n")
        self.log_output.insert(tk.END, "- Step 5: Summarize Data Comparison\n")
        self.log_output.insert(tk.END, "- Step 6: Ignore Structure/Formatting Differences\n")
        self.log_output.insert(tk.END, "\n")
        self.log_output.insert(tk.END, "Key Principle: SW determines success. Only extract data after SW=9000\n")
        self.log_output.insert(tk.END, "and machine log contains actual hex values (not placeholders).\n")
        self.log_output.insert(tk.END, "="*60 + "\n\n")

    def launch_gui(self):
        # Use the parent window passed from main launcher
        self.root = self.parent
        
        # Set icon
        try:
            icon_path = self.get_icon_path()
            img = PILImage.open(icon_path).resize((32, 32), PILImage.LANCZOS)
            icon = ImageTk.PhotoImage(img)
            self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Icon loading failed: {e}. Using default icon.")

        self.root.title("Machine Log Validation Tool - Dynamic Validation")
        self.root.geometry("1100x750")
        
        # PREVENT MAXIMIZING - Set min and max size to current size
        self.root.minsize(1100, 750)  # Minimum size = current size
        self.root.maxsize(1100, 750)  # Maximum size = current size
        self.root.configure(bg="#f5f6fa")
        
        # Make window NOT resizable (this should work now)
        self.root.resizable(False, False)

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern styles with smaller fonts
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background='#2c3e50', foreground='white')
        style.configure('Header.TLabel', font=('Arial', 9, 'bold'), background='#ffffff', foreground='#2c3e50')
        style.configure('TButton', font=('Arial', 9))
        style.configure('Accent.TButton', background='#3498db', foreground='white')
        style.configure('TEntry', font=('Arial', 9))
        style.configure('TCombobox', font=('Arial', 9))
        style.configure('TLabelframe', background='#ffffff', bordercolor='#bdc3c7')
        style.configure('TLabelframe.Label', background='#ffffff', foreground='#2c3e50', font=('Arial', 10, 'bold'))

        # Main container with reduced padding
        main_frame = tk.Frame(self.root, bg='#f5f6fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Header with reduced height
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#2c3e50')
        header_content.pack(fill=tk.BOTH, padx=20, pady=12)
        
        title_label = tk.Label(
            header_content,
            text="📊 Machine Log Validation Tool - Dynamic Validation",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(side=tk.LEFT)

        # Content area
        content_frame = tk.Frame(main_frame, bg='#f5f6fa')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel - Configuration with reduced width
        left_panel = tk.Frame(content_frame, bg='#ffffff', relief=tk.RAISED, bd=1, width=320)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        left_panel.pack_propagate(False)

        # Right panel - Results
        right_panel = tk.Frame(content_frame, bg='#ffffff', relief=tk.RAISED, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # === LEFT PANEL - CONFIGURATION ===
        left_content = tk.Frame(left_panel, bg='#ffffff', padx=15, pady=15)
        left_content.pack(fill=tk.BOTH, expand=True)

        # File Selection Frame
        file_frame = ttk.LabelFrame(left_content, text="📁 File Selection", padding=12)
        file_frame.pack(fill=tk.X, pady=(0, 12))

        # Variable Script File Selection
        ttk.Label(file_frame, text="Variable Script File:", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 6))
        
        script_frame = tk.Frame(file_frame, bg='#ffffff')
        script_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.script_entry = ttk.Entry(script_frame)
        self.script_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        
        script_btn = ttk.Button(script_frame, text="Browse", command=self.browse_script_file, width=8)
        script_btn.pack(side=tk.RIGHT)

        # Machine Log File Selection
        ttk.Label(file_frame, text="Machine Log File:", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 6))
        
        machine_frame = tk.Frame(file_frame, bg='#ffffff')
        machine_frame.pack(fill=tk.X)
        
        self.machine_log_entry = ttk.Entry(machine_frame)
        self.machine_log_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        
        machine_btn = ttk.Button(machine_frame, text="Browse", command=self.browse_machine_log_file, width=8)
        machine_btn.pack(side=tk.RIGHT)

        # Dynamic Validation Info Frame
        info_frame = ttk.LabelFrame(left_content, text="ℹ️ Dynamic Validation Info", padding=12)
        info_frame.pack(fill=tk.X, pady=(0, 12))
        
        info_text = """Validation Logic:
• Step 0: Skip irrelevant lines
• Step 1: Align script and machine log
• Step 2: Extract SW and compare
• Step 2.5: Check for actual data
• Step 3: Extract placeholders
• Step 4: Construct full APDU
• Step 5: Summarize comparison
• Step 6: Ignore formatting

Key: SW determines success.
Data only extracted after SW=9000
and actual values exist."""
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 9),
            bg='#ffffff',
            fg='#2c3e50',
            justify=tk.LEFT,
            anchor="w",
            wraplength=280
        )
        info_label.pack(fill=tk.BOTH, expand=True)

        # Actions Frame
        action_frame = ttk.LabelFrame(left_content, text="🚀 Actions", padding=12)
        action_frame.pack(fill=tk.X)

        # Validation Button
        validate_btn = tk.Button(
            action_frame,
            text="▶️ Validate Machine Log",
            command=self.validate_machine_log,
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor='hand2'
        )
        validate_btn.pack(fill=tk.X, pady=(0, 8))

        # Clear Button
        clear_btn = tk.Button(
            action_frame,
            text="🗑️ Clear All Fields",
            command=self.clear_all_fields,
            font=('Arial', 9),
            bg='#e74c3c',
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        clear_btn.pack(fill=tk.X)

        # === RIGHT PANEL - RESULTS ===
        right_content = tk.Frame(right_panel, bg='#ffffff')
        right_content.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # Results header
        results_header = tk.Frame(right_content, bg='#34495e', height=40)
        results_header.pack(fill=tk.X)
        results_header.pack_propagate(False)

        results_title = tk.Label(
            results_header,
            text="📋 Validation Results",
            font=('Arial', 11, 'bold'),
            bg='#34495e',
            fg='#ecf0f1'
        )
        results_title.pack(side=tk.LEFT, padx=15, pady=10)

        # Log Output Frame
        log_frame = ttk.LabelFrame(right_content, text="Validation Log", padding=8)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.log_output = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white',
            selectbackground='#3498db',
            relief=tk.FLAT,
            padx=12,
            pady=12
        )
        self.log_output.pack(fill=tk.BOTH, expand=True)

        # Configure text colors for better readability
        self.log_output.tag_configure("success", foreground="#27ae60")
        self.log_output.tag_configure("error", foreground="#e74c3c")
        self.log_output.tag_configure("warning", foreground="#f39c12")
        self.log_output.tag_configure("info", foreground="#3498db")

        # Add initial instructions
        self.clear_all_fields()