# Advanced Static File Analyzer
# - Open a file
# - Analyze hashes, indicators, metadata, PE structure, and certificate metadata
# - Report suspicious anomalies without executing the target
# - Save/export the analysis report

import datetime
import hashlib
import ipaddress
import math
import mimetypes
import os
import re
import tkinter as tk
from collections import Counter
from tkinter import filedialog, messagebox, scrolledtext

# Optional third-party dependencies. The GUI can still start if one is missing.
try:
    import pefile
except ImportError:
    pefile = None

try:
    import magic
except ImportError:
    magic = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import piexif
except ImportError:
    piexif = None

try:
    from oletools.olevba import VBA_Parser
except ImportError:
    VBA_Parser = None

try:
    from capstone import (
        Cs,
        CS_ARCH_ARM,
        CS_ARCH_ARM64,
        CS_ARCH_X86,
        CS_MODE_32,
        CS_MODE_64,
        CS_MODE_ARM,
    )
except ImportError:
    Cs = None

try:
    from cryptography.hazmat.primitives.serialization.pkcs7 import (
        load_der_pkcs7_certificates,
    )
except ImportError:
    load_der_pkcs7_certificates = None


selected_file_path = ""
analysis_report_text = ""


def extract_indicators(file_path):
    report = "=== [INDICATORS OF COMPROMISE & HASHES] ===\n"
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        md5 = hashlib.md5(data).hexdigest()
        sha256 = hashlib.sha256(data).hexdigest()
        report += f"MD5: {md5}\nSHA256: {sha256}\n"

        ip_pattern = rb"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        found_ips = set()
        for raw_ip in re.findall(ip_pattern, data):
            text_ip = raw_ip.decode("ascii", errors="ignore")
            try:
                found_ips.add(str(ipaddress.ip_address(text_ip)))
            except ValueError:
                pass

        if found_ips:
            report += "Found Potential IPv4 Addresses:\n"
            for ip in sorted(found_ips):
                report += f"  - {ip}\n"
        else:
            report += "No explicit hardcoded IPv4 addresses found.\n"
    except Exception as e:
        report += f"Failed to extract hashes/indicators: {e}\n"

    return report + "\n"


def check_extension(file_path):
    report = "=== [FILE SIGNATURE & EXTENSION CHECK] ===\n"

    if magic is None:
        return report + "Skipped: python-magic is not installed.\n\n"

    try:
        actual_mime = magic.from_file(file_path, mime=True)
        guessed_mime, guessed_encoding = mimetypes.guess_type(file_path)

        report += f"Actual MIME type: {actual_mime}\n"
        report += f"MIME type expected from extension: {guessed_mime or 'Unknown'}\n"
        if guessed_encoding:
            report += f"Guessed encoding: {guessed_encoding}\n"

        if guessed_mime is None:
            report += "INFO: The filename extension does not map to a known MIME type.\n"
        elif actual_mime != guessed_mime:
            report += (
                "WARNING: File extension/MIME mismatch. The file contents do not "
                "match the MIME type normally associated with its filename extension.\n"
            )
        else:
            report += "Extension is consistent with the detected MIME type.\n"
    except Exception as e:
        report += f"Extension validation failed: {e}\n"

    return report + "\n"


def check_non_pe_metadata(file_path):
    report = "=== [NON-PE METADATA & MACRO AUDIT] ===\n"
    lower_path = file_path.lower()

    if lower_path.endswith(".pdf"):
        if PyPDF2 is None:
            return report + "Skipped PDF metadata scan: PyPDF2 is not installed.\n\n"

        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                info = reader.metadata

                if info:
                    report += "PDF Metadata Fields Found:\n"
                    for key, val in info.items():
                        report += f"  {key}: {val}\n"
                        if any(
                            x in str(val).lower()
                            for x in ["exploit", "metasploit", "payload", "bypass"]
                        ):
                            report += (
                                f"  WARNING: Suspicious text found in metadata field: {key}\n"
                            )
                else:
                    report += "No PDF metadata dictionary retrieved.\n"
        except Exception as e:
            report += f"Failed to parse PDF metadata: {e}\n"

    elif any(lower_path.endswith(ext) for ext in [".doc", ".xls", ".docm", ".xlsm"]):
        if VBA_Parser is None:
            return report + "Skipped Office macro scan: oletools is not installed.\n\n"

        vba_parser = None
        try:
            vba_parser = VBA_Parser(file_path)
            if vba_parser.detect_vba_macros():
                report += "WARNING: Embedded VBA macros detected.\n"
                indicators = vba_parser.analyze_macros() or []

                if indicators:
                    report += "Macro Analysis Indicators:\n"
                    for item in indicators:
                        if isinstance(item, (tuple, list)):
                            if len(item) >= 3:
                                indicator_type, keyword, description = item[:3]
                                report += (
                                    f"  - [{indicator_type}] {keyword}: {description}\n"
                                )
                            elif len(item) == 2:
                                keyword, description = item
                                report += f"  - {keyword}: {description}\n"
                            else:
                                report += f"  - {item[0]}\n"
                        else:
                            report += f"  - {item}\n"
                else:
                    report += "No suspicious macro-analysis keywords were returned.\n"
            else:
                report += "No embedded VBA macro streams detected.\n"
        except Exception as e:
            report += f"Office document analysis failed: {e}\n"
        finally:
            if vba_parser is not None:
                try:
                    vba_parser.close()
                except Exception:
                    pass

    elif any(lower_path.endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
        if piexif is None:
            return report + "Skipped EXIF scan: piexif is not installed.\n\n"

        try:
            exif_dict = piexif.load(file_path)
            suspicious_exif = False

            for ifd in ("0th", "Exif", "GPS", "1st"):
                if ifd not in exif_dict:
                    continue

                for tag, value in exif_dict[ifd].items():
                    tag_info = piexif.TAGS.get(ifd, {}).get(tag, {})
                    tag_name = tag_info.get("name", str(tag))
                    tag_value = str(value)

                    if any(
                        x in tag_value.lower()
                        for x in ["base64", "eval", "system", "cmd", "powershell", "http://", "https://"]
                    ):
                        report += (
                            "WARNING: Suspicious text found in EXIF field "
                            f"{tag_name}: {tag_value[:100]}\n"
                        )
                        suspicious_exif = True

            if not suspicious_exif:
                report += "No suspicious EXIF text indicators found.\n"
        except Exception as e:
            report += f"No parsable EXIF metadata extracted ({e}).\n"
    else:
        report += "Skipping metadata scan: no specialized parser configured for this file type.\n"

    return report + "\n"


def calculate_entropy(data):
    if not data:
        return 0.0

    length = len(data)
    entropy = 0.0
    for count in Counter(data).values():
        p_x = count / length
        entropy -= p_x * math.log2(p_x)
    return entropy


def check_pe_structure_and_composition(file_path):
    report = "=== [PORTABLE EXECUTABLE STRUCTURE & COMPOSITION AUDIT] ===\n"

    if pefile is None:
        return report + "Skipped: pefile is not installed.\n\n"

    try:
        pe = pefile.PE(file_path, fast_load=False)
    except pefile.PEFormatError:
        return report + "Skipping: File is not a Windows PE file.\n\n"
    except Exception as e:
        return report + f"Failed to process PE structure: {e}\n\n"

    standard_sections = {
        ".text", ".data", ".rsrc", ".reloc", ".pdata", ".idata",
        ".edata", ".rdata", ".bss", ".tls", ".CRT",
    }
    suspicious_packers = ["UPX", "THEMIDA", "ASPACK", "FSG", "MPRESS", "VMPROTECT"]

    try:
        import_api_count = 0
        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                import_api_count += len(entry.imports)

        report += f"Imported API count: {import_api_count}\n"
        if 0 < import_api_count < 10:
            report += (
                f"WARNING: Small Import Address Table ({import_api_count} imports). "
                "This can occur with dynamic API resolution, packed binaries, or small legitimate programs.\n"
            )

        for section in pe.sections:
            name = section.Name.decode("utf-8", errors="ignore").rstrip("\x00") or "<unnamed>"
            section_data = section.get_data()
            entropy = calculate_entropy(section_data)
            upper_name = name.upper()

            report += f"Section {name}: entropy={entropy:.2f}/8.00\n"

            if any(packer in upper_name for packer in suspicious_packers):
                report += f"WARNING: Known packer-like section name detected: [{name}]\n"

            if name not in standard_sections and not any(
                packer in upper_name for packer in suspicious_packers
            ):
                report += f"INFO: Non-standard PE section name: [{name}]\n"

            if entropy > 7.2:
                report += (
                    f"WARNING: High entropy in section [{name}] ({entropy:.2f}/8.00). "
                    "This may indicate compression, encryption, or packed/obfuscated data.\n"
                )

            is_writable = bool(section.Characteristics & 0x80000000)
            is_executable = bool(section.Characteristics & 0x20000000)
            if is_writable and is_executable:
                report += (
                    f"WARNING: Section [{name}] is both writable and executable (W+X).\n"
                )

            if section.SizeOfRawData > 0 and section.Misc_VirtualSize > section.SizeOfRawData * 10:
                report += (
                    f"WARNING: Section [{name}] virtual size is more than 10x its raw size.\n"
                )

        if pe.OPTIONAL_HEADER.NumberOfRvaAndSizes != 16:
            report += (
                "INFO: Non-standard NumberOfRvaAndSizes value: "
                f"{pe.OPTIONAL_HEADER.NumberOfRvaAndSizes}\n"
            )

        for index, entry in enumerate(pe.OPTIONAL_HEADER.DATA_DIRECTORY):
            security_index = pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
            if index != security_index and entry.VirtualAddress > pe.OPTIONAL_HEADER.SizeOfImage:
                report += f"WARNING: Data directory {index} starts outside SizeOfImage.\n"

        overlay_offset = pe.get_overlay_data_start_offset()
        if overlay_offset is not None:
            file_size = os.path.getsize(file_path)
            if 0 <= overlay_offset < file_size:
                overlay_size = file_size - overlay_offset
                if overlay_size > 0:
                    report += (
                        f"INFO: Appended overlay data detected: {overlay_size} bytes. "
                        "Overlays can be legitimate but are worth reviewing.\n"
                    )

        report += "PE structural evaluation finished.\n"
    except Exception as e:
        report += f"PE analysis error: {e}\n"
    finally:
        try:
            pe.close()
        except Exception:
            pass

    return report + "\n"


def check_inflated_headers(file_path):
    report = "=== [HEADER PADDING DETECTION] ===\n"

    if pefile is None:
        return report + "Skipped: pefile is not installed.\n\n"

    try:
        pe = pefile.PE(file_path, fast_load=True)
    except Exception:
        return report + "Skipping: File is not a Windows PE file.\n\n"

    try:
        size_of_headers = pe.OPTIONAL_HEADER.SizeOfHeaders
        first_section_offset = pe.sections[0].PointerToRawData if pe.sections else 0
        report += f"Declared size of headers: {size_of_headers} bytes\n"
        report += f"First section raw offset: {first_section_offset} bytes\n"

        if size_of_headers > 65536 or first_section_offset > 65536:
            report += "WARNING: Unusually large PE header/section offset (>64 KiB).\n"
        else:
            report += "Header sizing is within the configured threshold.\n"
    finally:
        try:
            pe.close()
        except Exception:
            pass

    return report + "\n"


def check_architecture(file_path):
    report = "=== [ARCHITECTURE VALIDATION] ===\n"

    if pefile is None:
        return report + "Skipped: pefile is not installed.\n\n"

    try:
        pe = pefile.PE(file_path, fast_load=True)
    except Exception:
        return report + "Skipping: File is not a Windows PE file.\n\n"

    try:
        machine = pe.FILE_HEADER.Machine
        entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint

        architectures = {
            0x014C: ("x86", CS_ARCH_X86 if Cs else None, CS_MODE_32 if Cs else None),
            0x8664: ("x86-64", CS_ARCH_X86 if Cs else None, CS_MODE_64 if Cs else None),
            0x01C0: ("ARM", CS_ARCH_ARM if Cs else None, CS_MODE_ARM if Cs else None),
            0xAA64: ("ARM64", CS_ARCH_ARM64 if Cs else None, CS_MODE_ARM if Cs else None),
        }

        arch_name, cs_arch, cs_mode = architectures.get(machine, (f"Unknown (0x{machine:04X})", None, None))
        report += f"PE machine architecture: {arch_name}\n"
        report += f"Address of entry point: 0x{entry_point:X}\n"

        if entry_point == 0:
            report += "INFO: Entry point is zero. This can be normal for some PE file types, such as resource-only DLLs.\n"
            return report + "\n"

        if Cs is None:
            report += "Disassembly skipped: capstone is not installed.\n"
            return report + "\n"

        if cs_arch is None:
            report += "Disassembly skipped: unsupported/unknown PE machine type.\n"
            return report + "\n"

        try:
            code_bytes = pe.get_data(entry_point, 32)
            md = Cs(cs_arch, cs_mode)
            instructions = list(md.disasm(code_bytes, entry_point))

            if instructions:
                report += "Entry-point disassembly preview:\n"
                for insn in instructions[:5]:
                    report += f"  0x{insn.address:X}: {insn.mnemonic} {insn.op_str}\n"
            else:
                report += "WARNING: No instructions decoded at the declared entry point.\n"
        except Exception as e:
            report += f"Disassembler failed: {e}\n"
    finally:
        try:
            pe.close()
        except Exception:
            pass

    return report + "\n"


def check_signature(file_path):
    report = "=== [DIGITAL CERTIFICATE INSPECTION] ===\n"

    if pefile is None:
        return report + "Skipped: pefile is not installed.\n\n"

    try:
        pe = pefile.PE(file_path, fast_load=True)
    except pefile.PEFormatError:
        return report + "Skipping: File is not a Windows PE file.\n\n"
    except Exception as e:
        return report + f"Failed to inspect PE certificate table: {e}\n\n"

    try:
        security_index = pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
        security_dir = pe.OPTIONAL_HEADER.DATA_DIRECTORY[security_index]
        address = security_dir.VirtualAddress
        size = security_dir.Size

        if address == 0 or size < 8:
            return report + "Result: No Authenticode certificate table is present.\n\n"

        report += f"Certificate table offset: {address}\n"
        report += f"Certificate table size: {size} bytes\n"

        if load_der_pkcs7_certificates is None:
            report += (
                "Certificate table is present, but certificate metadata parsing was skipped "
                "because the cryptography package is unavailable.\n"
            )
            return report + "\n"

        with open(file_path, "rb") as f:
            f.seek(address)
            win_certificate = f.read(size)

        if len(win_certificate) < 8:
            return report + "WARNING: Certificate table is truncated.\n\n"

        declared_length = int.from_bytes(win_certificate[0:4], "little")
        revision = int.from_bytes(win_certificate[4:6], "little")
        cert_type = int.from_bytes(win_certificate[6:8], "little")
        report += f"WIN_CERTIFICATE declared length: {declared_length}\n"
        report += f"WIN_CERTIFICATE revision: 0x{revision:04X}\n"
        report += f"WIN_CERTIFICATE type: 0x{cert_type:04X}\n"

        available_length = min(declared_length, len(win_certificate))
        der_data = win_certificate[8:available_length]
        certs = load_der_pkcs7_certificates(der_data)

        if not certs:
            report += "WARNING: Certificate table exists, but no X.509 certificates were parsed.\n"
            return report + "\n"

        for index, cert in enumerate(certs, start=1):
            report += f"Certificate #{index}:\n"
            report += f"  Subject: {cert.subject.rfc4514_string()}\n"
            report += f"  Issuer: {cert.issuer.rfc4514_string()}\n"
            report += f"  Serial: {cert.serial_number}\n"
            not_before = getattr(cert, "not_valid_before_utc", cert.not_valid_before)
            not_after = getattr(cert, "not_valid_after_utc", cert.not_valid_after)
            report += f"  Valid From: {not_before}\n"
            report += f"  Valid Until: {not_after}\n"

        report += (
            "NOTE: Certificate metadata was parsed, but this function does not perform "
            "full Windows Authenticode trust-chain or signature verification.\n"
        )
    except Exception as e:
        report += f"Error processing certificate data: {e}\n"
    finally:
        try:
            pe.close()
        except Exception:
            pass

    return report + "\n"


def select_file(label_widget):
    global selected_file_path

    file_path = filedialog.askopenfilename(title="Select File for Static Analysis")
    if file_path:
        selected_file_path = file_path
        label_widget.config(
            text=f"Target: {os.path.basename(file_path)}",
            fg="green",
        )


def run_analysis(text_area_widget):
    global selected_file_path, analysis_report_text

    if not selected_file_path:
        messagebox.showwarning("File Missing", "Please select a target file first!")
        return

    text_area_widget.delete("1.0", tk.END)
    text_area_widget.insert(
        tk.END,
        f"[*] Initializing static analysis on: {selected_file_path}\n\n",
    )
    text_area_widget.update_idletasks()

    final_report = (
        "STATIC ANALYSIS REPORT\n"
        f"Generated: {datetime.datetime.now().isoformat(sep=' ', timespec='seconds')}\n"
        f"Target File: {selected_file_path}\n"
        + "=" * 60
        + "\n\n"
    )

    checks = [
        extract_indicators,
        check_extension,
        check_non_pe_metadata,
        check_pe_structure_and_composition,
        check_inflated_headers,
        check_architecture,
        check_signature,
    ]

    for check in checks:
        try:
            final_report += check(selected_file_path)
        except Exception as e:
            final_report += f"=== [{check.__name__}] ===\nUnexpected error: {e}\n\n"

    final_report += "=== [MITIGATION RECOMMENDATIONS] ===\n"
    if "WARNING:" in final_report:
        final_report += "- One or more anomalies were detected. Treat the file as untrusted until reviewed.\n"
        final_report += "- If execution is necessary, use an isolated sandbox or disposable VM.\n"
        final_report += "- Correlate the hashes and indicators with trusted threat-intelligence sources.\n"
    else:
        final_report += "- No configured high-risk structural anomalies were detected.\n"
        final_report += "- A clean static-analysis result does not prove that a file is safe.\n"

    analysis_report_text = final_report
    text_area_widget.insert(tk.END, final_report)


def save_report():
    global analysis_report_text

    if not analysis_report_text:
        messagebox.showwarning(
            "Empty Report",
            "There is no analysis report to export yet.",
        )
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )

    if save_path:
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(analysis_report_text)
            messagebox.showinfo("Success", "Report exported successfully.")
        except OSError as e:
            messagebox.showerror("Save Failed", f"Could not save report:\n{e}")


def main():
    root = tk.Tk()
    root.title("Advanced Static File Analyzer")
    root.geometry("900x700")
    root.minsize(760, 520)

    label = tk.Label(
        root,
        text="Static File Analyzer",
        font=("Arial", 20, "bold"),
    )
    label.pack(pady=10)

    file_label = tk.Label(
        root,
        text="No file selected",
        font=("Arial", 11, "italic"),
        fg="gray",
    )
    file_label.pack(pady=5)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    report_box = scrolledtext.ScrolledText(
        root,
        width=105,
        height=28,
        font=("Consolas", 10),
        wrap=tk.WORD,
    )

    open_button = tk.Button(
        btn_frame,
        text="Open File",
        width=15,
        command=lambda: select_file(file_label),
    )
    open_button.grid(row=0, column=0, padx=5)

    analyze_button = tk.Button(
        btn_frame,
        text="Analyze File",
        width=15,
        command=lambda: run_analysis(report_box),
    )
    analyze_button.grid(row=0, column=1, padx=5)

    save_button = tk.Button(
        btn_frame,
        text="Save Report",
        width=15,
        command=save_report,
    )
    save_button.grid(row=0, column=2, padx=5)

    exit_button = tk.Button(
        btn_frame,
        text="Exit",
        width=15,
        command=root.destroy,
    )
    exit_button.grid(row=0, column=3, padx=5)

    report_box.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Application error: {e}")
