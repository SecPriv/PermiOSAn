import xml.etree.ElementTree as ET

# PATH of the AndroidManifest.xml downloaded from Android Code Search
XML_PATH = "./AndroidManifest.xml"

def read_android_manifest(xml_url):
    with open(XML_PATH, "r") as fp:
        return fp.read()

def parse_manifest_for_deprecated(xml_content):
    try:
        # Parse the XML content
        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
        root = ET.fromstring(xml_content, parser)
        namespace = {"android": "http://schemas.android.com/apk/res/android"}
        
        # Extract all comments
        deprecated_permissions = []#getnext()
        deprecated = False
        for node in root.iter():
            if "function Comment" in str(node.tag):
                if "@deprecated" in node.text:
                    deprecated = True
            else:
                if deprecated == True:
                    if str(node.tag) != "permission":
                        deprecated = False
                    else:
                        name = node.attrib.get("{http://schemas.android.com/apk/res/android}name")
                        #print(name)
                        deprecated_permissions.append(name)
                        deprecated = False
        
        return deprecated_permissions
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []

# Fetch and parse AndroidManifest.xml
xml_content = read_android_manifest(XML_PATH)

if xml_content:
    deprecated_permissions = parse_manifest_for_deprecated(xml_content)
    if deprecated_permissions:
        print(f"{len(deprecated_permissions)} Deprecated Permissions Found:")
        for perm in deprecated_permissions:
            print(perm)
    else:
        print("No deprecated permissions found.")
