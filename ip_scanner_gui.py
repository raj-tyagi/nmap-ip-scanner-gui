import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext, filedialog
import nmap

def scan_target():
    ip_address = entry_ip.get()
    scan_type = scan_types.get()

    # Define scan arguments based on the selected scan type
    scan_arguments = {
        "Ping Scan": "-sn",
        "Quick Scan": "-F -sV",
        "Intense Scan": "-T4 -A"
        # Add more scan types and associated arguments as needed
    }

    # Creating a PortScanner object
    nm = nmap.PortScanner()

    # Scanning the target IP address with selected arguments
    nm.scan(ip_address, arguments=scan_arguments.get(scan_type, ''))

    # Initialize a counter for vulnerabilities
    vulnerabilities_count = 0

    # Vulnerable services (you can modify or expand this list)
    vulnerable_services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        80: "HTTP",
        443: "HTTPS",
        3306: "MySQL",
        5432: "PostgreSQL",
        # Add more ports and associated services as needed
    }

    # Clear previous results if any
    text_area.delete('1.0', tk.END)

    # Iterating through scan results
    for host in nm.all_hosts():
        text_area.insert(tk.END, f"Host : {host} ({nm[host].hostname()})\n", "bold")
        text_area.insert(tk.END, f"State : {nm[host].state()}\n\n")

        # Iterating through each protocol (tcp, udp) and printing open ports
        for proto in nm[host].all_protocols():
            text_area.insert(tk.END, f"Protocol : {proto}\n")
            ports = nm[host][proto].keys()
            sorted_ports = sorted(ports)
            for port in sorted_ports:
                state = nm[host][proto][port]['state']
                text_area.insert(tk.END, f"Port : {port} \tState : {state}\n")

                # Check if the port is in the vulnerable services list
                if port in vulnerable_services:
                    vulnerabilities_count += 1
                    text_area.insert(tk.END, f"Potential vulnerability found on {vulnerable_services[port]} (Port {port})!\n", "vulnerability")

    text_area.insert(tk.END, f"\nTotal vulnerabilities found: {vulnerabilities_count}\n", "bold")

def save_results():
    scan_results = text_area.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(scan_results)
        messagebox.showinfo("Save", f"Scan results saved to '{file_path}'")

# Creating the GUI window
root = tk.Tk()
root.title("Advanced IP Scanner")

# Set background color
root.configure(bg='#f0f0f0')

# Define custom styles
root.option_add("*Font", "Arial 10")
root.option_add("*background", "#f0f0f0")
root.option_add("*foreground", "#333333")

root.option_add("*TLabel.Font", "Arial 10 bold")
root.option_add("*TButton.Font", "Arial 10")

root.option_add("*TButton.Background", "#4caf50")
root.option_add("*TButton.Foreground", "white")

root.option_add("*TCombobox*Listbox*Font", "Arial 10")
root.option_add("*TCombobox*Listbox.Background", "#f0f0f0")

# Label and Entry for IP Address input
label_ip = ttk.Label(root, text="Enter the IP address to scan:")
label_ip.pack()

entry_ip = ttk.Entry(root)
entry_ip.pack()

# Dropdown menu for selecting scan types
scan_types = ttk.Combobox(root, values=["Ping Scan", "Quick Scan", "Intense Scan"])
scan_types.set("Quick Scan")  # Set default scan type
scan_types.pack()

# Button to trigger the scan
scan_button = ttk.Button(root, text="Scan", command=scan_target)
scan_button.pack()

# Text area to display scan results
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
text_area.pack()

# Button to save scan results to a file
save_button = ttk.Button(root, text="Save Results", command=save_results)
save_button.pack()

# Tag configuration for text widget
text_area.tag_configure("bold", font="Arial 10 bold")
text_area.tag_configure("vulnerability", foreground="red")

# Running the GUI main loop
root.mainloop()
