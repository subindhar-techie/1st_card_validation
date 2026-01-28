import re
import cv2
import xml.etree.ElementTree as ET

def clean_xml_string(xml_str):
    xml_str = re.sub(r'<(/?)(\w+)\s+(\w+)>', r'<\1\2_\3>', xml_str)
    xml_str = re.sub(r'<\?xml.*?\?>', '', xml_str)
    xml_str = re.sub(r'<!--.*?-->', '', xml_str)
    xml_str = xml_str.strip()
    return f"<root>{xml_str}</root>"

def process_qr_code_wbiot(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Image not found or unreadable: {image_path}")
        return {}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(thresh)
    if not data:
        data, bbox, _ = detector.detectAndDecode(gray)
    if data:
        print("QR Code data found:", data)
        try:
            root = ET.fromstring(clean_xml_string(data))
            return {child.tag.upper(): child.text for child in root}
        except ET.ParseError as e:
            print(f"Error parsing QR XML: {e}")
            return {}
    else:
        print("No QR code found in image:", image_path)
        return {}

def process_qr_code_mob(image_path):
    try:
        image = cv2.imread(image_path)
        detector = cv2.QRCodeDetector()
        value, pts, _ = detector.detectAndDecode(image)

        if value:
            value = re.sub(r'^\s*<\?xml.*\?>\s*', '', value)
            value = re.sub(r'<!--.*?-->', '', value, flags=re.DOTALL)
            value = re.sub(r'<\\([^>]+)>', r'</\1>', value)

            extracted_data = {}
            for match in re.finditer(r'<([^>]+)>([^<]+)</\1>', value):
                field = match.group(1).strip()
                field_value = match.group(2).strip()
                extracted_data[field] = field_value

            for field, field_value in extracted_data.items():
                print(f"{field}: {field_value}")

            return extracted_data
        else:
            print(f"No QR code found in image: {image_path}")
            return {}

    except Exception as e:
        print(f"Error processing QR code in {image_path}: {e}")
        return {}